# Evals

Small behavior checks for Skill Checkup OpenClaw.

- `evals/evals.json` defines minimum behavior cases.
- `fixtures-src/` stores synthetic fixture files.

Fixture skills are named `SKILL.fixture.md` on purpose so OpenClaw skill scanners do not register fake test skills when the repo is copied or inspected. Test harnesses that need real `SKILL.md` files should copy fixtures to a temp directory and rename them there.

## multi-workspace-root

Synthetic workspace with:

- root/global `skills/`
- `patients-agent/skills/`
- `sidecar/skills/`
- intentionally broken/cross-workspace path references

Used to validate the path integrity scanner and the multi-workspace audit logic.
