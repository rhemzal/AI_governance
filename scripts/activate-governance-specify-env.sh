#!/usr/bin/env bash
# Add Spec Kit CLI from the opt-in stack venv to PATH for this shell.
root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
export PATH="${root}/.tools/specify-venv/bin:${HOME}/.local/bin:${PATH}"
