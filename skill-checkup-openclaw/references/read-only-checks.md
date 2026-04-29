# Read-only checks


Priorize evidência. Use somente leituras e comandos não destrutivos.

Comandos típicos locais:

```bash
pwd
hostname
openclaw status
openclaw doctor --non-interactive
openclaw security audit --deep
openclaw health --json
openclaw memory status --deep
git status --short
git remote -v
git log --oneline -1
find skills -name SKILL.md | wc -l
find . -maxdepth 2 -name MEMORY.md -o -name HEARTBEAT.md -o -name AGENTS.md -o -name TOOLS.md
find . -path '*/skills/*/SKILL.md' -print
```

Performance:

```bash
find ~/.openclaw -type f \( -name 'sessions.json' -o -name '*.jsonl' -o -name '*.sqlite' -o -name '*.db' -o -name '*.log' \) \
  -printf '%s %p\n' 2>/dev/null | sort -nr | head -30
du -sh ~/.openclaw ~/.openclaw/media ~/.openclaw/logs ~/.openclaw/agents 2>/dev/null
```

Access:

```bash
openclaw sandbox explain --json
command -v gh && gh auth status
command -v op && op account list
command -v gog && gog status
```

Host Linux remoto, quando autorizado:

```bash
hostnamectl || uname -a
ss -ltnup
ufw status || true
systemctl status fail2ban --no-pager || true
systemctl status openclaw --no-pager || true
tailscale status || true
```

Crons:
- use `cron list` quando disponível;
- marcar `consecutiveErrors > 0` como finding;
- só destacar no topo se bloquear operação, segurança, backup ou entrega.

Segredos:

```bash
grep -RInE 'sk-|ghp_|xoxb-|xapp-|AKIA|tskey-|OPENAI_API_KEY|ANTHROPIC_API_KEY' \
  --exclude-dir=.git --exclude-dir=node_modules . | head -50
find . -name '.env' -not -path './.git/*'
```

Não revelar valores de segredos no relatório. Registrar só path/tipo de risco.

