# Review packet

You are a senior code reviewer. Review the completed change below against its requirements and identify issues before they cascade.

The requirements say what the software must do. For behavior the requirements are silent on, judge by what a reasonable person using this software would expect. A requirement's silence is not permission.

Read only this packet. Do not modify files and do not look outside it.

## Report

FINDINGS: each item is one issue. Say what is wrong and which requirement it breaks. If there is no issue, write NONE.

DECLINED: behaviors you considered and set aside, one line each, or NONE.

## What was implemented

One sentence in a maintainer note.

## Requirements

1. The sentence still says that evidence is recorded before a completion claim.
2. The change adds no behavior and no command.

## Change

```diff
-Record evidence before claiming the work is complete.
+Record evidence before claiming that the work is complete.
```
