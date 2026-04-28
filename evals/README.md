# Evals

Small fixtures used to test Skill Checkup OpenClaw behavior.

## multi-workspace-root

Synthetic workspace with:

- root/global `skills/`
- `patients-agent/skills/`
- `sidecar/skills/`
- intentionally broken/cross-workspace path references

Used to validate the path integrity scanner and the multi-workspace audit logic.
