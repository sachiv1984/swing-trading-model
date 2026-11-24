// knownFailing: a unit test that records a known bug (ST-19, BLG-QA-262, v9.18).
//
// react-scripts 5 ships Jest 27, which has no `test.failing` (added in Jest 28).
// This helper has the same meaning: the test passes while its body fails, and
// fails as soon as the body passes, naming the backlog items. Whoever fixes the
// bug must then turn the case into a plain `test`. Every use names at least one
// backlog ID, so no known failure is left untracked.

// Only a failed expect() counts as the bug still being there. Any other error
// (a TypeError from a renamed helper, a failed import) is rethrown, so a broken
// test body cannot pass for ever. Jest's assertion errors carry matcherResult.
export async function runKnownFailing(fn, ids) {
  try {
    await fn();
  } catch (error) {
    if (error && error.matcherResult) return error;
    throw error;
  }
  throw new Error(
    `Known failure (${ids.join(", ")}) now passes: change knownFailing to test and update the backlog item.`
  );
}

export function knownFailing(name, ids, fn) {
  if (!Array.isArray(ids) || ids.length === 0 || ids.some((id) => !/^BLG-[A-Z]+-\d+$/.test(id))) {
    throw new Error(`knownFailing("${name}") needs one or more backlog IDs such as "BLG-FE-289"`);
  }
  test(`[known failing: ${ids.join(", ")}] ${name}`, () => runKnownFailing(fn, ids));
}
