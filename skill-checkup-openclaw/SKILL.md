---
name: skill-checkup-openclaw
description: >
  Use when auditing whether an OpenClaw agent, workspace, or host is ready,
  healthy, safe, production-ready, slow, bloated, underpowered, overpowered,
  or has backup/GitHub/memory/skills/heartbeat/watchdog/security/access in
  order. Exclusively for OpenClaw agents.
type: skill
category: operations
status: ACTIVE
owner: Bruno Okamoto / OpenClaw mini-course
version: 1.0.0
created: 2026-04-27
last_reviewed: 2026-04-28
estimated_time: 10min
model_compatible: [claude-sonnet-4, claude-opus-4, gpt-5, gpt-4o, gemini-pro]
---

# Skill Checkup OpenClaw

Audita se um agente OpenClaw está pronto para operar sem virar dívida operacional. Esta skill é uma auditoria **executiva, decisória e acionável**, não um despejo técnico.

**Exclusiva para OpenClaw.** Não use esta skill para Claude Desktop, Cursor, LangChain, n8n, servidores genéricos ou outros frameworks de agente. Ela assume estrutura, comandos, memória, canais, crons, gateway e segurança do OpenClaw.

A pergunta central é:

> Esse agente pode operar com usuário/cliente real? Se não, qual é o próximo movimento mais importante?

## Regra-mãe

**Executive-first. Deep internally. Short by default.**

A skill pode avaliar muita coisa por baixo, mas a resposta padrão mostra só:

1. Score + veredito
2. Pode operar ou não
3. Top 3 ações agora
4. O que eu posso resolver
5. O que o humano precisa fazer
6. Próximo passo que o agente assume

Tabela, checklist completo e evidências técnicas só entram no modo `deep` ou se o usuário pedir.

## Princípios

1. **Utilidade > completude.** Não listar 40 achados se 3 ações destravam 80% do risco.
2. **Score com travas.** A nota não pode mascarar bomba crítica.
3. **Permissão antes da promessa.** Antes de dizer que pode corrigir, verificar se está em modo audit-only, fix-capable ou full-maintenance.
4. **Perfil antes do score.** Um agente pessoal, bot de curso, agente de aluno, cliente real e grupo público não têm o mesmo padrão.
5. **Unknown não é falha.** O que não foi verificado vira “não verificado”, não problema confirmado.
6. **Acesso não é sempre bom.** Medir se há acesso suficiente sem estar perigoso demais.
7. **Ação segura.** Qualquer execução corretiva exige backup antes.
8. **Sem overwhelm.** Se o achado não muda a próxima ação, não entra no topo.

## Modos

| Modo | Quando usar | Saída |
|---|---|---|
| `quick` | triagem em 2-3 min | score aproximado + top 3 riscos |
| `standard` | padrão | resposta executiva curta + plano |
| `deep` | pré-produção, incidente, cliente real | resposta executiva + tabela/evidências/apêndice técnico |

Se o usuário não escolher, use `standard`.

## Execution Permission Preflight

Antes de prometer correções, classifique o nível real de permissão da sessão/alvo:

| Modo | Significado | Pode fazer |
|---|---|---|
| `audit-only` | só leitura ou permissões incertas | diagnosticar, gerar PRD, listar bloqueios |
| `fix-capable` | write/edit/exec básico disponíveis | corrigir arquivos, registries, backups locais, limpezas reversíveis |
| `full-maintenance` | exec/elevated/security full no host alvo | mexer em serviço, systemd, gateway, permissões, firewall/SSH com aprovação |

Regras:
- Auditoria read-only não exige full access.
- Correção real geralmente exige `fix-capable`.
- Correções de host/serviço/firewall exigem `full-maintenance` + aprovação humana.
- Se faltar permissão, o PRD deve listar isso como pré-condição operacional, não como tarefa vaga para o usuário.

## Perfis de agente

Antes de pontuar, classifique o alvo:

| Perfil | Tolerância | Exemplo |
|---|---|---|
| `personal` | mais autonomia aceitável | agente pessoal do Bruno |
| `internal-test` | pode ter ressalvas | bot de curso teste |
| `student` | precisa ser simples e seguro | agente de aluno do curso |
| `client-production` | rigor alto | agente de cliente/pagante |
| `group-public` | rigor máximo de acesso/contexto | grupo Telegram/WhatsApp com vários usuários |

Use o perfil para calibrar achados. Exemplo: `exec full` pode ser aceitável em `personal`, mas é risco crítico em `group-public`.

## Eixos internos

Calcule internamente estes 5 eixos. Não mostre todos por padrão.

### 1. Operational Readiness
Pode operar sem perder dados, cair em silêncio ou depender de sorte?

Checks:
- gateway ativo, versão, channels;
- Git/repo remoto/estado limpo;
- backup/sync automático;
- heartbeat/crons/watchdog;
- integridade básica de sessão;
- workspace organizado.

### 2. Course Baseline Fit
Está alinhado com o padrão que ensinamos no curso?

Checks:
- GitHub privado ou estratégia clara de backup;
- backup automático;
- memória semântica ativa **ou** fallback FTS claro;
- `MEMORY.md`, `HEARTBEAT.md`, `AGENTS.md`, `TOOLS.md` quando o template exigir;
- organização de workspace e estrutura de pastas;
- skills organizadas e registry funcionando;
- security audit sem critical;
- gateway loopback/token;
- Telegram/WhatsApp com política certa;
- 1Password/sem secrets hardcoded;
- watchdog/update/restart;
- documentação mínima para o aluno entender a estrutura.

Nota: não exigir “mapa do cérebro” se isso não é ensinado naquele módulo. Para o curso atual, avaliar **organização do workspace**, não MAPA como requisito universal.

### 3. Runtime Performance Risk
O agente está ficando lento por bloat ou contexto acumulado?

Checks:
- tamanho de `sessions.json`, transcripts e maiores sessões;
- quantidade/idade de sessões ativas;
- SQLite/LCM/cache grandes;
- logs grandes;
- `media/`, delivery queues e failed tasks acumulados;
- compaction/pruning configurados;
- `% ctx`, compactions recentes, contexto perto do limite;
- heartbeat/crons gerando contexto demais;
- status/health lentos.

Veredito interno:
- 🟢 leve;
- 🟡 risco de lentidão;
- 🔴 degradado.

### 4. Official OpenClaw Compliance
Está alinhado com docs e ferramentas oficiais?

Checks:
- `openclaw doctor` quando seguro;
- `openclaw security audit --deep`;
- `openclaw health --json`;
- update posture: versão atual vs latest/dry-run;
- session pruning/compaction;
- memory status/search;
- sandbox explain/tool policy;
- diagnostics/stability disponíveis.

### 5. Access & Execution Capability
O agente está empoderado o suficiente para resolver problemas — sem estar perigoso demais?

Checks:
- `exec/process` disponíveis? host, sandbox ou node?
- elevated/full realmente disponível?
- read/write/edit/apply_patch;
- web_fetch/web_search/browser;
- cron/message/nodes/sessions_spawn;
- GitHub CLI/auth;
- 1Password CLI/auth;
- gog/Gmail/Calendar OAuth;
- Tailscale/SSH;
- provider/model tool-use/fallback/rate-limit/billing.

Classificação:
- ✅ acesso suficiente;
- ⚠️ falta acesso para o trabalho esperado;
- 🔴 acesso demais para o contexto.

## Severidade e confiança

Cada finding importante recebe internamente:

| Campo | Valores | Como decidir |
|---|---|---|
| Criticidade | `critical`, `high`, `medium`, `low` | dano se ignorar |
| Urgência | `today`, `this_week`, `later` | quando agir |
| Impacto usuário | `blocks`, `degrades`, `invisible` | efeito no usuário final |
| Confiança | `verified`, `inferred`, `unknown` | força da evidência |

### Regra para unknown

- `unknown` não reduz score como falha confirmada.
- Se for área crítica não verificada, entra como “precisa checar antes de produção”.
- Não escrever “quebrado” sem evidência.

## Score

Comece em 100, aplique deduções confirmadas e depois travas.

### Deduções sugeridas

| Problema verificado | Dedução |
|---|---:|
| Sem backup/sync verificável | -20 |
| GitHub/origin ausente | -15 |
| Repo sujo sem commit/backup | -10 |
| Memória crítica ausente/corrompida | -15 |
| Sem memória semântica e sem fallback FTS em agente dependente de memória | -12 |
| Skills registry quebrado | -10 |
| Sem heartbeat em agente proativo | -8 |
| Cron essencial falhando repetidamente | -8 |
| Sem watchdog/restart em host remoto | -12 |
| Runtime degradado por sessão/cache/logs | -10 a -20 |
| Gateway exposto sem proteção clara | -25 |
| Segredo hardcoded | -30 |
| SSH/root remoto inseguro | -15 |
| Falta acesso essencial para executar função do agente | -10 |
| Acesso excessivo para contexto multiusuário | -10 a -25 |
| Estrutura de pastas confusa | -5 |
| Docs/organização do workspace stale | -5 |

### Travas de nota

Aplique o menor teto que aparecer:

| Condição | Score máximo |
|---|---:|
| Segredo real hardcoded | 40 |
| Gateway público sem auth/firewall | 35 |
| Exec/elevated perigoso em grupo público | 45 |
| Sem backup e sem Git remoto | 60 |
| Sem Git remoto | 75 |
| Sem backup automático verificável | 70 |
| Memória essencial quebrada | 75 |
| Runtime claramente degradado | 75 |
| Sem watchdog em host remoto de produção | 80 |
| Crons essenciais com falha recorrente | 85 |
| Acesso essencial não verificado em produção | 85 |

### Veredito

| Score | Status | Significado |
|---:|---|---|
| 90-100 | ✅ Produção | pode operar com confiança |
| 75-89 | 🟡 Operável | bom, com ajustes não bloqueantes |
| 60-74 | ⚠️ Operável com ressalvas | usar em teste/piloto, corrigir antes de escalar |
| 40-59 | 🟠 Risco alto | não colocar usuário real sem correções |
| 0-39 | ❌ Não operar | risco crítico/security/data loss |

## Workflow

### 1. Definir alvo

Identifique:
- agente/workspace/host alvo;
- modo (`quick`, `standard`, `deep`);
- perfil do agente;
- função esperada;
- o que é essencial para esse agente.

Se faltar alvo e não for inferível, faça uma pergunta curta.

### 2. Rodar checks read-only

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

### 3. Classificar achados

Para cada achado relevante, registre internamente:

```md
- [severity/urgency/confidence] Título
  Eixo: readiness/course/performance/compliance/access
  Evidência: comando/path/observação curta
  Impacto: por que importa para operação
  Próxima ação: verbo claro
  Dono: agente ou humano
```

### 4. Gerar resposta padrão

No modo `standard`, use exatamente esta estrutura curta:

```md
# Agent Readiness — {nome}

Score: {N}/100 — {veredito}

Veredito:
{1-3 frases. Pode operar? Em que condição?}

Top 3 riscos que eu atacaria:
1. {risco + impacto}
2. {risco + impacto}
3. {risco + impacto}

Modo de execução:
Existem 3 modos: `audit-only`, `fix-capable` e `full-maintenance`.
Este agente está em **{modo}** — com isso, eu {posso fazer X / não posso fazer Y}.

Eu posso assumir:
- Criar o plano de ação.
- Fazer backup/snapshot.
- Executar o que for reversível e permitido pelo modo atual.

Seu trabalho vai ser aprovar estas etapas:
- {login/OAuth/conta/token/firewall/SSH/envio externo, somente quando necessário}

Próximo movimento:
Só responde **bora** e eu monto o plano, faço backup e começo.
```

Não inclua tabela executiva no `standard` salvo se o usuário pedir. O fechamento deve reduzir carga cognitiva: não despeje uma lista de tarefas para o humano; transforme em plano que o agente pode executar e escale apenas os bloqueios humanos reais.

### 5. Gerar modo deep

No modo `deep`, depois da resposta padrão, adicione:

```md
## Eixos internos
| Eixo | Status | Evidência curta |

## Findings relevantes
| Severidade | Urgência | Confiança | Achado | Dono |

## Apêndice técnico
{comandos/paths sem segredos}
```

### 6. Fechar com decisão leve

No final, não despeje novas tarefas. Feche com uma chamada leve para ação:

> “Só responde **bora** e eu monto o plano, faço backup e começo.”

Se o usuário aprovar, crie um PRD de correção passo a passo. O PRD deve começar com backup/snapshot, declarar o modo de permissão necessário (`audit-only`, `fix-capable` ou `full-maintenance`), separar o que o agente executa sozinho e marcar exatamente onde precisa de humano para login, conta, OAuth, token, firewall/SSH ou aprovação externa.

Regra: a próxima ação padrão após o audit é **oferecer planejamento executável + backup**, não jogar tarefas no humano.

Nunca execute correções automaticamente sem pedido claro. Se o usuário aprovar execução direta, ainda assim faça backup/snapshot antes.

## Divisão: agente vs humano

### O agente pode resolver, com backup antes

- Commit/backup de arquivos locais.
- Atualizar registries e organização do workspace.
- Organizar arquivos fora do lugar para `archive/`.
- Corrigir paths de skills.
- Criar relatórios e manifests.
- Rodar checks read-only.
- Preparar comandos de firewall/SSH sem aplicar.
- Ajustar crons somente com aprovação explícita.
- Arquivar sessões/logs/mídias antigas somente se for reversível e aprovado.

### O humano precisa fazer ou aprovar

- OAuth/login interativo (`gog auth`, Google, Tailscale approval).
- Criar/autorizar token no GitHub/1Password.
- Decidir abrir/fechar acesso externo.
- Aplicar firewall/SSH em host onde lockout é possível.
- Enviar mensagem/email/post externo.
- Qualquer ação destrutiva ou irreversível.

## Regra de backup antes de execução

Se o usuário pedir “segue”, “executa”, “corrige”, “faz”, antes de qualquer mudança:

1. Criar snapshot seguro do estado atual.
2. Registrar manifest do backup.
3. Confirmar que o backup existe.
4. Só então aplicar mudanças.

Backup mínimo local:

```bash
backup_dir="archive/agent-readiness/$(date +%Y-%m-%d-%H%M%S)"
mkdir -p "$backup_dir"
git status --short > "$backup_dir/git-status-before.txt" 2>/dev/null || true
git diff > "$backup_dir/git-diff-before.patch" 2>/dev/null || true
find . -maxdepth 4 -type f \( -name 'SKILL.md' -o -name 'MAPA.md' -o -name 'MEMORY.md' -o -name 'HEARTBEAT.md' -o -name 'AGENTS.md' -o -name 'TOOLS.md' \) \
  > "$backup_dir/manifest-files.txt"
```

Em host remoto, criar backup no host remoto também. Se houver Git limpo e remoto funcionando, preferir commit/checkpoint. Se houver mudanças locais do usuário, não sobrescrever: preservar em patch e avisar.

## Anti-overwhelm

Não colocar no topo:
- warnings cosméticos;
- itens sem evidência;
- detalhes de comando;
- histórico repetido sem mudança;
- “boas práticas” que não mudam risco real;
- eixo completo se só uma ação importa.

Colocar no topo:
- perda de dados;
- risco de segurança;
- falha de entrega;
- ausência de rollback;
- login humano necessário;
- bloqueio para usuário final;
- lentidão/degradação que afeta uso real.

## Exemplo de saída standard

```md
# Agent Readiness — bot-curso-teste

Score: 68/100 — ⚠️ Operável com ressalvas

Veredito:
Pode operar em teste. Eu não colocaria aluno real ainda porque falta rollback confiável e watchdog.

Top 3 riscos que eu atacaria:
1. GitHub/rollback frágil.
2. Sem watchdog confiável.
3. SSH/portas precisam revisão.

Modo de execução:
Existem 3 modos: `audit-only`, `fix-capable` e `full-maintenance`.
Este agente está em **fix-capable parcial** — posso preparar e corrigir arquivos, mas firewall/serviço precisa aprovação.

Eu posso assumir:
- Criar o plano de ação.
- Fazer backup/snapshot.
- Executar correções reversíveis.

Seu trabalho vai ser aprovar estas etapas:
- GitHub/1Password se token faltar.
- Firewall/SSH antes de aplicar.

Próximo movimento:
Só responde **bora** e eu monto o plano, faço backup e começo.
```
