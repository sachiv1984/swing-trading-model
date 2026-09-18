"""
Unit tests for scripts/check_contract_example_freshness.py (ST-17,
BLG-QA-166, EPIC-03, v9.5).

Covers the pure-logic functions the script's drift detection depends on:
$ref resolution, schema key flattening (including allOf/oneOf/anyOf
combinators, nested objects, and array-of-object items), example JSON key
flattening, response-schema lookup (direct and templated-path matching),
and the heading/JSON-fence example extraction regexes. No filesystem or
network I/O -- every test constructs its own in-memory openapi.yaml-shaped
dict or markdown string, per this repo's established convention for
scripts/*.py checker tests (see test_api_performance_baseline_drift_check.py).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import check_contract_example_freshness as freshness  # noqa: E402


class TestResolveRef:
    def test_no_ref_returns_node_unchanged(self):
        node = {"type": "object", "properties": {}}
        assert freshness.resolve_ref(node, {}) is node

    def test_single_ref_resolves(self):
        root = {"components": {"schemas": {"Foo": {"type": "object", "properties": {"a": {}}}}}}
        node = {"$ref": "#/components/schemas/Foo"}
        resolved = freshness.resolve_ref(node, root)
        assert resolved == {"type": "object", "properties": {"a": {}}}

    def test_chained_ref_resolves(self):
        root = {
            "components": {
                "schemas": {
                    "A": {"$ref": "#/components/schemas/B"},
                    "B": {"type": "object", "properties": {"x": {}}},
                }
            }
        }
        node = {"$ref": "#/components/schemas/A"}
        resolved = freshness.resolve_ref(node, root)
        assert resolved == {"type": "object", "properties": {"x": {}}}

    def test_non_dict_node_returned_as_is(self):
        assert freshness.resolve_ref("not-a-schema", {}) == "not-a-schema"

    def test_external_ref_raises(self):
        node = {"$ref": "external.yaml#/Foo"}
        try:
            freshness.resolve_ref(node, {})
            assert False, "expected AssertionError"
        except AssertionError:
            pass


class TestSchemaTopKeys:
    def test_flat_object_properties(self):
        schema = {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}}}
        assert freshness.schema_top_keys(schema, {}) == {"id", "name"}

    def test_nested_object_descends_one_level(self):
        schema = {
            "type": "object",
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {"id": {"type": "string"}, "amount": {"type": "number"}},
                }
            },
        }
        keys = freshness.schema_top_keys(schema, {})
        assert keys == {"data", "data.id", "data.amount"}

    def test_array_of_objects_uses_bracket_notation(self):
        schema = {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {"type": "object", "properties": {"sku": {"type": "string"}}},
                }
            },
        }
        keys = freshness.schema_top_keys(schema, {})
        assert keys == {"items", "items[].sku"}

    def test_ref_inside_properties_is_resolved(self):
        root = {"components": {"schemas": {"Item": {"type": "object", "properties": {"sku": {}}}}}}
        schema = {"type": "object", "properties": {"item": {"$ref": "#/components/schemas/Item"}}}
        keys = freshness.schema_top_keys(schema, root)
        assert keys == {"item", "item.sku"}

    def test_allof_combinator_merges_keys(self):
        schema = {
            "allOf": [
                {"type": "object", "properties": {"status": {}}},
                {"type": "object", "properties": {"data": {"type": "object", "properties": {"id": {}}}}},
            ]
        }
        keys = freshness.schema_top_keys(schema, {})
        assert keys == {"status", "data", "data.id"}

    def test_oneof_combinator_merges_keys(self):
        schema = {"oneOf": [{"type": "object", "properties": {"a": {}}}, {"type": "object", "properties": {"b": {}}}]}
        assert freshness.schema_top_keys(schema, {}) == {"a", "b"}

    def test_depth_limits_nesting(self):
        schema = {
            "type": "object",
            "properties": {
                "a": {"type": "object", "properties": {"b": {"type": "object", "properties": {"c": {}}}}}
            },
        }
        # depth=1: only top-level property names, no descent.
        assert freshness.schema_top_keys(schema, {}, depth=1) == {"a"}

    def test_non_dict_schema_returns_empty_set(self):
        assert freshness.schema_top_keys(None, {}) == set()
        assert freshness.schema_top_keys("string", {}) == set()

    def test_empty_properties_returns_empty_set(self):
        assert freshness.schema_top_keys({"type": "object"}, {}) == set()


class TestJsonFlattenKeys:
    def test_flat_dict(self):
        assert freshness.json_flatten_keys({"id": 1, "name": "x"}) == {"id", "name"}

    def test_nested_dict_uses_dot_notation(self):
        obj = {"data": {"id": 1, "amount": 2.5}}
        assert freshness.json_flatten_keys(obj) == {"data", "data.id", "data.amount"}

    def test_list_of_dicts_uses_bracket_notation_on_first_element(self):
        obj = {"items": [{"sku": "A"}, {"sku": "B"}]}
        assert freshness.json_flatten_keys(obj) == {"items", "items[].sku"}

    def test_list_of_non_dicts_contributes_no_nested_keys(self):
        obj = {"tags": ["a", "b", "c"]}
        assert freshness.json_flatten_keys(obj) == {"tags"}

    def test_empty_list_contributes_no_nested_keys(self):
        assert freshness.json_flatten_keys({"items": []}) == {"items"}

    def test_non_dict_top_level_returns_empty_set(self):
        assert freshness.json_flatten_keys([1, 2, 3]) == set()

    def test_depth_zero_returns_empty_set(self):
        assert freshness.json_flatten_keys({"a": 1}, depth=0) == set()

    def test_depth_limits_nesting(self):
        obj = {"a": {"b": {"c": 1}}}
        # depth=2: descend into 'a' (depth 2->1), then into 'b' would need
        # depth 1->0 which is disallowed by the depth<=0 guard on entry.
        keys = freshness.json_flatten_keys(obj, depth=2)
        assert keys == {"a", "a.b"}


class TestResponseSchemaFor:
    def _root(self):
        return {
            "paths": {
                "/widgets": {
                    "get": {
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "object", "properties": {"status": {}, "data": {}}}
                                    }
                                }
                            }
                        }
                    }
                },
                "/widgets/{widget_id}": {
                    "get": {
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "object", "properties": {"id": {}}}
                                    }
                                }
                            }
                        }
                    }
                },
                "/orders": {
                    "post": {
                        "responses": {
                            "201": {
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "object", "properties": {"order_id": {}}}
                                    }
                                }
                            }
                        }
                    }
                },
            }
        }

    def test_direct_path_match(self):
        keys = freshness.response_schema_for(self._root(), "GET", "/widgets")
        assert keys == {"status", "data"}

    def test_templated_path_match(self):
        keys = freshness.response_schema_for(self._root(), "GET", "/widgets/abc-123")
        assert keys == {"id"}

    def test_201_response_code_used_when_no_200(self):
        keys = freshness.response_schema_for(self._root(), "POST", "/orders")
        assert keys == {"order_id"}

    def test_no_matching_path_returns_none(self):
        assert freshness.response_schema_for(self._root(), "GET", "/nonexistent") is None

    def test_matching_path_wrong_method_returns_none(self):
        assert freshness.response_schema_for(self._root(), "DELETE", "/widgets") is None

    def test_no_json_content_returns_none(self):
        root = {"paths": {"/x": {"get": {"responses": {"200": {"content": {}}}}}}}
        assert freshness.response_schema_for(root, "GET", "/x") is None

    def test_ref_response_is_resolved(self):
        root = {
            "components": {
                "responses": {
                    "Ok": {
                        "content": {
                            "application/json": {"schema": {"type": "object", "properties": {"a": {}}}}
                        }
                    }
                }
            },
            "paths": {"/x": {"get": {"responses": {"200": {"$ref": "#/components/responses/Ok"}}}}},
        }
        assert freshness.response_schema_for(root, "GET", "/x") == {"a"}


class TestFindExamples:
    def test_extracts_example_near_response_marker(self):
        text = (
            "## GET /widgets\n\n"
            "### Response — 200 OK\n\n"
            '```json\n{"status": "ok", "data": []}\n```\n'
        )
        found = list(freshness.find_examples(text))
        assert found == [("GET", "/widgets", {"status": "ok", "data": []})]

    def test_ignores_fence_with_no_response_marker_nearby(self):
        text = (
            "## GET /widgets\n\n"
            "### Request body\n\n"
            '```json\n{"filter": "active"}\n```\n'
        )
        assert list(freshness.find_examples(text)) == []

    def test_picks_last_response_fence_in_section(self):
        text = (
            "## POST /widgets\n\n"
            "### Response — 200 OK\n\n"
            '```json\n{"a": 1}\n```\n\n'
            "### Response — 201 Created (schema variant)\n\n"
            '```json\n{"b": 2}\n```\n'
        )
        found = list(freshness.find_examples(text))
        assert found == [("POST", "/widgets", {"b": 2})]

    def test_multiple_headings_scoped_correctly(self):
        text = (
            "## GET /a\n\n### Response\n```json\n{\"x\": 1}\n```\n\n"
            "## GET /b\n\n### Response\n```json\n{\"y\": 2}\n```\n"
        )
        found = list(freshness.find_examples(text))
        assert found == [("GET", "/a", {"x": 1}), ("GET", "/b", {"y": 2})]

    def test_invalid_json_fence_is_skipped(self):
        text = "## GET /a\n\n### Response\n```json\n{not valid json}\n```\n"
        assert list(freshness.find_examples(text)) == []

    def test_non_object_json_fence_is_skipped(self):
        text = "## GET /a\n\n### Response\n```json\n[1, 2, 3]\n```\n"
        assert list(freshness.find_examples(text)) == []

    def test_no_heading_yields_nothing(self):
        assert list(freshness.find_examples("no headings here at all")) == []


class TestHeadingAndFenceRegexes:
    def test_heading_regex_matches_standard_form(self):
        m = freshness.HEADING_RE.search("## GET /portfolio/history\n")
        assert m is not None
        assert m.group(1) == "GET"
        assert m.group(2) == "/portfolio/history"

    def test_heading_regex_rejects_h3(self):
        assert freshness.HEADING_RE.search("### GET /portfolio/history\n") is None

    def test_json_fence_regex_extracts_body(self):
        text = '```json\n{"a": 1}\n```'
        m = freshness.JSON_FENCE_RE.search(text)
        assert m is not None
        assert m.group(1) == '{"a": 1}'

    def test_response_marker_regex_case_insensitive(self):
        assert freshness.RESPONSE_MARKER_RE.search("### Response Schema") is not None
        assert freshness.RESPONSE_MARKER_RE.search("### response body") is not None
        assert freshness.RESPONSE_MARKER_RE.search("### Request body") is None


class TestMainIntegration:
    """End-to-end: main() against a real temp contract dir + openapi.yaml,
    covering the 'unwrapped data.* convention' comparison logic (main()'s
    own inline logic, not a standalone helper) and the exit-code contract."""

    def _write_repo(self, tmp_path, openapi_dict, contract_files):
        import yaml as _yaml

        contracts_dir = tmp_path / "docs" / "specs" / "api_contracts"
        contracts_dir.mkdir(parents=True)
        for name, text in contract_files.items():
            (contracts_dir / name).write_text(text)

        reference_dir = tmp_path / "docs" / "reference"
        reference_dir.mkdir(parents=True)
        (reference_dir / "openapi.yaml").write_text(_yaml.safe_dump(openapi_dict))

        return contracts_dir, reference_dir / "openapi.yaml"

    def test_matching_example_exits_zero(self, tmp_path, monkeypatch, capsys):
        openapi_dict = {
            "paths": {
                "/widgets": {
                    "get": {
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {"status": {}, "data": {}},
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        contract_text = (
            "## GET /widgets\n\n### Response — 200 OK\n\n"
            '```json\n{"status": "ok", "data": []}\n```\n'
        )
        contracts_dir, openapi_file = self._write_repo(
            tmp_path, openapi_dict, {"widgets_endpoints.md": contract_text}
        )
        monkeypatch.setattr(freshness, "CONTRACTS_DIR", contracts_dir)
        monkeypatch.setattr(freshness, "OPENAPI_FILE", openapi_file)

        assert freshness.main() == 0
        out = capsys.readouterr().out
        assert "No drift detected" in out

    def test_extra_key_in_example_flags_drift(self, tmp_path, monkeypatch, capsys):
        openapi_dict = {
            "paths": {
                "/widgets": {
                    "get": {
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "object", "properties": {"status": {}}}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        contract_text = (
            "## GET /widgets\n\n### Response — 200 OK\n\n"
            '```json\n{"status": "ok", "stale_renamed_field": true}\n```\n'
        )
        contracts_dir, openapi_file = self._write_repo(
            tmp_path, openapi_dict, {"widgets_endpoints.md": contract_text}
        )
        monkeypatch.setattr(freshness, "CONTRACTS_DIR", contracts_dir)
        monkeypatch.setattr(freshness, "OPENAPI_FILE", openapi_file)

        assert freshness.main() == 1
        out = capsys.readouterr().out
        assert "POSSIBLE DRIFT" in out
        assert "stale_renamed_field" in out

    def test_unwrapped_data_convention_does_not_flag_drift(self, tmp_path, monkeypatch, capsys):
        """Contract docs show the *contents* of the envelope's `data` field
        directly (unwrapped), not re-wrapped in another `data:` layer -- a
        schema key of `data.foo` must match a bare example key `foo`."""
        openapi_dict = {
            "paths": {
                "/cash/summary": {
                    "get": {
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "status": {},
                                                "data": {
                                                    "type": "object",
                                                    "properties": {"current_cash": {}},
                                                },
                                            },
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        contract_text = (
            "## GET /cash/summary\n\n### Response — 200 OK\n\n"
            "#### `data` schema\n\n"
            '```json\n{"current_cash": 1000.0}\n```\n'
        )
        contracts_dir, openapi_file = self._write_repo(
            tmp_path, openapi_dict, {"cash_endpoints.md": contract_text}
        )
        monkeypatch.setattr(freshness, "CONTRACTS_DIR", contracts_dir)
        monkeypatch.setattr(freshness, "OPENAPI_FILE", openapi_file)

        assert freshness.main() == 0

    def test_unresolvable_endpoint_is_skipped_not_failed(self, tmp_path, monkeypatch, capsys):
        openapi_dict = {"paths": {}}
        contract_text = (
            "## GET /nowhere\n\n### Response — 200 OK\n\n"
            '```json\n{"status": "ok"}\n```\n'
        )
        contracts_dir, openapi_file = self._write_repo(
            tmp_path, openapi_dict, {"nowhere_endpoints.md": contract_text}
        )
        monkeypatch.setattr(freshness, "CONTRACTS_DIR", contracts_dir)
        monkeypatch.setattr(freshness, "OPENAPI_FILE", openapi_file)

        assert freshness.main() == 0
        out = capsys.readouterr().out
        assert "SKIPPED (1)" in out
        assert "Checked 0 contract response examples" in out

    def test_missing_contracts_dir_returns_1(self, tmp_path, monkeypatch):
        monkeypatch.setattr(freshness, "CONTRACTS_DIR", tmp_path / "does_not_exist")
        monkeypatch.setattr(freshness, "OPENAPI_FILE", tmp_path / "also_missing.yaml")
        assert freshness.main() == 1
