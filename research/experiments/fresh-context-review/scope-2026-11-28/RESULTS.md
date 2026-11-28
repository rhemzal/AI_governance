# Scope screening for a separated review packet (2026-11-28)

This is one screening of the separated-packet pattern. It is not an Elephant
Goldfish Model install and it does not run that skill's review stages.

Each review was a fresh `agent --print --mode ask --model grok-4.7` process.
Its workspace contained only `PACKET.md`. The eight packets in this directory
are those files. B0 includes an author "ship it" sentence. B1 does not. The
review instructions are otherwise the same. Stderr was empty and each process
exited 0.

A counted finding is an issue the report places under FINDINGS. Lines under
DECLINED are not findings.

| Pair | What a correct report does | B0 | B1 |
| --- | --- | --- | --- |
| Hidden edge | Name that empty or whitespace-only input returns `""` instead of `ValueError` with message `empty`. | Found | Found |
| Edge already covered | FINDINGS NONE. The implementation and tests meet both requirements. | NONE | NONE |
| Gate already fails | The missing numbered ADR is the same fact `.github/workflows/adr-required.yml` fails for an `architecture/` change with no ADR. A reviewer who only restates it adds no finding. | Restated the missing ADR | Restated the missing ADR |
| Wording only | FINDINGS NONE. The added word `that` does not change the completion-claim sentence. | NONE | NONE |

B1 repeated B0 on every pair. The author sentence did not hide the broken
requirement or the missing ADR. The two quiet pairs produced no counted
finding. Declined notes on the covered pair were extra edges the requirements
do not demand.

Scope from this screening:

- A separated packet did not add a verified finding beyond the same reviewer
  who could see the author sentence.
- A wording edit and a requirement that already has a test stayed quiet.
- An `architecture/` change without a numbered ADR is already a failing gate.
  Both reviewers restated that requirement because the packet included it.

The full product stays uninstalled. A later attempt would have to show a
verified miss by the author-context arm that the separated packet finds,
with the quiet pairs still quiet. One model and one pass are a screening,
not a measure of model variability.
