import { knownFailing, runKnownFailing } from "./knownFailing";

describe("runKnownFailing", () => {
  test("resolves with the error while the body still fails", async () => {
    const error = await runKnownFailing(() => expect(1).toBe(2), ["BLG-FE-1"]);
    expect(error).toBeInstanceOf(Error);
  });

  test("resolves for an asynchronous body whose assertion fails", async () => {
    const body = async () => { await Promise.resolve(); expect(1).toBe(2); };
    await expect(runKnownFailing(body, ["BLG-FE-1"])).resolves.toBeInstanceOf(Error);
  });

  test.each([
    ["a TypeError", () => { const helper = undefined; helper(); }],
    ["a plain Error", () => { throw new Error("import failed"); }],
  ])("rethrows %s instead of counting it as the known failure", async (_label, body) => {
    await expect(runKnownFailing(body, ["BLG-FE-1"])).rejects.not.toHaveProperty("matcherResult");
  });

  test("rejects, naming the IDs, once the body passes", async () => {
    await expect(runKnownFailing(() => expect(1).toBe(1), ["BLG-FE-1", "BLG-QA-2"])).rejects.toThrow(
      "Known failure (BLG-FE-1, BLG-QA-2) now passes"
    );
  });
});

describe("knownFailing", () => {
  test.each([[undefined], [[]], [["FE-289"]], [["see BLG-FE-289"]]])("rejects IDs %p", (ids) => {
    expect(() => knownFailing("x", ids, () => {})).toThrow("needs one or more backlog IDs");
  });
});
