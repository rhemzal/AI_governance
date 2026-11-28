# Review packet

You are a senior code reviewer. Review the completed change below against its requirements and identify issues before they cascade.

The requirements say what the software must do. For behavior the requirements are silent on, judge by what a reasonable person using this software would expect. A requirement's silence is not permission.

Read only this packet. Do not modify files and do not look outside it.

## Report

FINDINGS: each item is one issue. Say what is wrong and which requirement it breaks. If there is no issue, write NONE.

DECLINED: behaviors you considered and set aside, one line each, or NONE.

## What was implemented

A function `normalize_token` and one test.

## Requirements

1. A token with surrounding whitespace and mixed case is returned as stripped lowercase.
2. A token that is empty or whitespace-only is not returned as a token. The function raises `ValueError` and the message is `empty`.

## Change

```python
def normalize_token(value: str) -> str:
    """Return the token in stripped lowercase form."""
    return value.strip().lower()


def test_strips_and_lowercases():
    assert normalize_token("  AbC ") == "abc"
```
