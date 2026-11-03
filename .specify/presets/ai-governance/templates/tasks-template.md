## Proportional execution

For each task, name the verification command and whether the task changes
behavior.

- Behavior or bug fix: write the test, run it, and see the expected failure
  before implementation. Follow `test-driven-development` from the pin.
- Documentation or registry wording only: do not require that red-green
  cycle. Check the diff and the existing doc or registry command.
- Do not ask the operator to continue after a task when the mandate already
  covers it. Record progress in the feature ledger so a later session can
  resume without repeating completed edits.
