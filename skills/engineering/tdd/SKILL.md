---
name: tdd
description: >-
  Test-driven development with a red-green-refactor loop, building one vertical
  slice at a time. Use when the user asks for TDD, implements a new feature,
  fixes a bug, or modifies core business logic where automated regression tests
  provide fast feedback.
---

# Test-Driven Development

Build behavior in tight red-green-refactor cycles, one vertical slice at a time.

## Workflow

1. **Agree on the seam**: Identify the public interface (function, endpoint, component, or CLI behavior) to exercise. Test behavior through public boundaries, not internal private helpers.
2. **Red**: Write one failing test describing the next small slice of expected behavior. Run the test suite and confirm it fails for the right reason (missing/incorrect behavior, not a syntax or setup error).
3. **Green**: Write the minimal production code needed to make the test pass. Do not anticipate future slices prematurely. Re-run tests to confirm green.
4. **Refactor**: While tests remain green, clean up duplication, unclear names, and unnecessary complexity in both production and test code. Re-run tests after refactoring.
5. **Repeat**: Move to the next vertical slice (next requirement or edge case) until complete.

## Test Quality Guidelines

- Avoid brittle mocks of internal collaborators; prefer real objects or boundary fakes where practical.
- Each test should fail if and only if the behavior it specifies breaks.
- Never write all tests upfront before any implementation (horizontal slicing); interleave Red -> Green -> Refactor per slice.
