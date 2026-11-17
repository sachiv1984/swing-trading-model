"""Page colour token sweep check (ST-08, EPIC-03, v9.17, BLG-FE-265).

Acceptance criterion: no bare `text-white` remains in `src/pages/` outside
coloured fills. A bare `text-white` renders white text in both themes, so on
the light theme's white cards and slate-100 page it disappears
(design_system.md §Semantic Colour Tokens; primary text is `text-app-fg`).

`text-white` is allowed in a class string only when one of these holds:
- the same string has a solid coloured fill (`bg-<hue>-500..900` or a
  `from-<hue>-500..900` gradient) that the text sits on;
- the string has a `dark:text-...` partner, so it is a light/dark pair;
- the fill is supplied from elsewhere on the same line (a `bg:` key in a
  config object, or a `cfg.bg`-style variable passed to `cn()`), by an inline
  `style={{ backgroundColor }}` on the next two lines, or by a
  template-literal expression in the same string.

Also checks, across `src/pages/` and the components the sweep converted, that
every class string with a dark-only surface or text class (`bg-slate-800/900`,
`text-slate-300/400`, a solid `bg-<hue>-900` without white text, 300/400-shade
hue text) has its light partner in the same string. Limits: single-line string
literals only, and literals containing `${` are skipped; the light-theme axe
scans in `tests/e2e/accessibility-axe-scan.spec.js` are the rendered check.
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = sorted((ROOT / "src" / "pages").glob("*.js"))
# Components the sweep converted (design_system.md §Page Colour Token Sweep,
# Scope). Components outside this list are tracked by BLG-FE-288.
SWEPT_COMPONENT_DIRS = ["analytics", "risk", "journal", "signals", "performance", "reports", "watchlist"]
SWEPT_COMPONENT_FILES = [
    "notifications/NotificationRow.js", "notifications/AlertThresholdsSection.js",
    "notifications/CustomPriceAlertsSection.js", "shared/BulkActionToolbar.js",
    "shared/DownloadCsvButton.js", "ui/EmptyStateAction.js", "ui/DataState.js",
    "trades/SavedFiltersControl.js", "trades/EntryChecklist.js", "trades/SignalContextPanel.js",
    "trades/SetupQualityScorePanel.js", "positions/PositionCard.js", "positions/PaperAccountPanel.js",
    "positions/StrategyCompliancePanel.js", "positions/ComplianceRecheckModal.js",
]
COMPONENTS = ROOT / "src" / "components"
SWEPT = PAGES + sorted(
    {f for d in SWEPT_COMPONENT_DIRS for f in (COMPONENTS / d).glob("*.js")}
    | {COMPONENTS / f for f in SWEPT_COMPONENT_FILES}
)

STRING = re.compile(r"""(["'`])((?:(?!\1)[^\n\\]|\\.)*?)\1""")
HUES = "emerald|green|rose|red|amber|yellow|cyan|blue|violet|purple|orange|sky|teal|indigo|pink|fuchsia|gray|slate"
FILL = re.compile(r"(?<![:\w-])(?:bg|from)-(?:" + HUES + r")-[5-9]00(?!/)")
FILL_ON_LINE = re.compile(r"""bg:\s*["']|\.bg\b|backgroundColor""")
BARE_TEXT_WHITE = re.compile(r"(?<![:\w-])text-white(?![\w-])")

# Dark-only values that need a light partner in the same string: dark slate
# surfaces, light slate text, solid dark hue fills (unless they carry white
# text, i.e. a coloured fill), and 300/400-shade hue text.
HUE = "emerald|green|rose|red|amber|yellow|cyan|blue|violet|purple|orange|sky|teal|indigo|pink|lime|fuchsia"
DARK_ONLY = re.compile(
    r"(?<![:\w/-])(?P<prop>text|bg|border|divide)-"
    r"(?P<val>slate-(?:[7-9]00|950)(?:/\d+)?|slate-[2-4]00|(?:" + HUE + r")-(?:[89]00|950|[34]00))(?![\w/-])"
)


def _line(src, pos):
    """The literal's line plus the two after it (an inline `style` fill sits there)."""
    start = src.rfind("\n", 0, pos) + 1
    end = pos
    for _ in range(3):
        nxt = src.find("\n", end + 1)
        end = len(src) if nxt == -1 else nxt
    return src[start:end]


def _strings(path):
    src = path.read_text()
    for m in STRING.finditer(src):
        yield src.count("\n", 0, m.start()) + 1, m.group(2), _line(src, m.start())


def test_pages_exist():
    assert len(PAGES) >= 20, "expected the routed pages under src/pages/"


def test_no_bare_text_white_outside_coloured_fills():
    offenders = []
    for path in PAGES:
        for lineno, s, line in _strings(path):
            if not BARE_TEXT_WHITE.search(s):
                continue
            if FILL.search(s) or "dark:text-" in s or "${" in s or FILL_ON_LINE.search(line):
                continue
            offenders.append(f"{path.relative_to(ROOT)}:{lineno}: {s.strip()[:100]}")
    assert not offenders, (
        "Bare text-white outside a coloured fill (use text-app-fg, or a "
        "light/dark pair):\n" + "\n".join(offenders)
    )


def test_dark_only_classes_have_a_light_partner():
    offenders = []
    for path in SWEPT:
        for lineno, s, _ in _strings(path):
            toks = s.split()
            if len(toks) < 1 or "${" in s:
                continue
            dark_props = {
                re.sub(r"^dark:(?:[a-z-]+:)*", "", t).split("-")[0]
                for t in toks
                if t.startswith("dark:") and not re.match(r"^dark:[a-z-]+:", t)
            }
            for t in toks:
                m = DARK_ONLY.fullmatch(t)
                if not m or m.group("prop") in dark_props:
                    continue
                # Mid-tone text and fills that pass in both themes are not dark-only.
                if m.group("prop") == "text" and m.group("val").startswith("slate-") and m.group("val") >= "slate-700":
                    continue
                if m.group("prop") == "bg" and m.group("val") in {"slate-200", "slate-300", "slate-400"}:
                    continue
                if m.group("prop") in {"border", "divide"} and m.group("val") in {"slate-200", "slate-300", "slate-400"}:
                    continue
                hue_val = m.group("val").split("-")
                if hue_val[0] != "slate":
                    shade = int(hue_val[1])
                    if m.group("prop") == "bg" and (shade <= 400 or BARE_TEXT_WHITE.search(s) or len(toks) == 1):
                        continue  # light hue fills are not dark-only; a dark fill with white text, or a fill-only value (heatmap tile), is a coloured fill
                    if m.group("prop") == "text" and shade >= 800:
                        continue  # dark hue text is the light-theme half
                    if m.group("prop") in {"border", "divide"}:
                        continue  # hue borders are decorative, not text contrast
                offenders.append(f"{path.relative_to(ROOT)}:{lineno}: {t} in '{s.strip()[:90]}'")
    assert not offenders, (
        "Dark-only colour class without a light partner in a swept file (design_system.md "
        "§Light-Theme Colour Tokens rule 1):\n" + "\n".join(offenders)
    )
