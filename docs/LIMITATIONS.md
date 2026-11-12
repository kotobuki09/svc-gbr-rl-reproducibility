# Limitations and interpretation guardrails

## Internal benchmark

The training and evaluation records share parent SCADA records through the
augmentation and preprocessing workflow. Reported performance is therefore an
internal benchmark. It does not establish independent out-of-sample
generalization to unseen SCADA operations.

## Public sample

The public sample is synthetic-only. It is designed to make the schema and
public code runnable, not to reproduce the empirical distribution of the
restricted data.

## Edge deployment

Any edge-feasibility results should be read as simulation or benchmark results
unless the release includes an independently documented physical deployment.

## Future validation

An independent validation study should split original operational records
before augmentation, preprocessing, calibration, and model selection. The
current public release does not claim that this analysis has been completed.
