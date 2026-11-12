# Reviewer-facing data note

The public repository now provides the code, schemas, configurations, curated
aggregate artifacts, figures metadata, and a small synthetic demonstration
sample. The complete operational SCADA records and row-level derived data are
not publicly released because of data-governance and operational-sensitivity
constraints. Qualified researchers may request access through the process in
`DATA_ACCESS.md`.

Because training and evaluation records share parent SCADA records, the
reported results are an internal benchmark. They do not establish independent
out-of-sample generalization. A future independent validation should partition
the original operational records before augmentation, preprocessing,
calibration, and model selection.
