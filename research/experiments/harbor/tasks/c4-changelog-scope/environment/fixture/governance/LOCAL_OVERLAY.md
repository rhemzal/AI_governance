# LOCAL GOVERNANCE OVERLAY — fixture

| Constraint | Load when |
| --- | --- |
| A first import refuses an existing destination, including an empty directory. | The task edits ci/import_bundle.py or the import procedure. |
| A symlink is not a snapshot. Opt-in copy may use cp -aL outside the bundle importer. | The task copies kit files or changes symlink checks. |
