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
version: 1.2.0
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


## Recursos empacotados

- `scripts/path_integrity_check.py` — scanner read-only para inventariar roots de skills, duplicatas, symlinks quebrados, refs de scripts e caminhos em `SKILL.md` e links quebrados de registries. Use em setups multi-workspace ou quando paths forem risco.

## Antes de rodar para usuário final

Se este repositório incluir `ANTES-DE-RODAR.md`, leia esse arquivo antes de executar a auditoria para uma pessoa não técnica. Ele contém a explicação simples de contexto, como preparar expectativa e como orientar a leitura do resultado.

Use essa explicação para deixar claro que a skill escaneia muita coisa internamente, mas devolve só o que importa: score, veredito, top 3 riscos, responsabilidades e próximo passo.

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

## Output Contract — standard

No modo `standard`, a resposta final deve seguir **exatamente** o template da seção “Gerar resposta padrão”.

Regras obrigatórias:
- usar somente estas seções, nesta ordem: `Agent Readiness`, `Score/Confiança`, `Veredito`, `Mapa detectado` (somente se houver múltiplos workspaces/agentes), `Top 3 riscos que eu atacaria`, `Modo de execução`, `Eu posso assumir`, `Seu trabalho vai ser aprovar estas etapas`, `Próximo movimento`;
- terminar com a chamada explícita: **“Só responde bora e eu monto o plano, faço backup e começo.”**;
- mencionar que o próximo passo é montar plano/PRD de correção com backup antes da execução;
- quando o modo não for `full-maintenance`, explicar em 1 frase que o usuário pode escolher delegar mais acesso/manutenção para reduzir fricção operacional, sem prometer “sem aprovação” para ações sensíveis;
- não adicionar seções extras.

Seções proibidas no `standard`:
- `Achados bons`;
- `Problemas menores`;
- `Observações`;
- `Checklist`;
- `Evidências`;
- `Detalhes técnicos`;
- qualquer tabela não solicitada;
- lista completa de paths/arquivos no standard.

Se houver bons sinais ou problemas menores, use-os apenas internamente para calibrar score. Só entram na resposta se mudarem uma das 3 ações principais.

Falha conhecida a evitar:

```md
Achados bons:
• Gateway local em loopback...

Problemas menores:
• Embeddings sem quota...

Próximo movimento recomendado: fazer um plano curto...
```

Isso está errado para `standard`: aumenta ruído, foge do contrato e não fecha com o PRD/backup assumido pelo agente.

## Princípios

1. **Utilidade > completude.** Não listar 40 achados se 3 ações destravam 80% do risco.
2. **Score com travas.** A nota não pode mascarar bomba crítica.
3. **Permissão antes da promessa.** Antes de dizer que pode corrigir, verificar se está em modo audit-only, fix-capable ou full-maintenance.
4. **Perfil antes do score.** Um agente pessoal, bot de curso, agente de aluno, cliente real e grupo público não têm o mesmo padrão.
5. **Unknown não é falha.** O que não foi verificado vira “não verificado”, não problema confirmado.
6. **Acesso não é sempre bom.** Medir se há acesso suficiente sem estar perigoso demais.
7. **Ação segura.** Qualquer execução corretiva exige backup antes.
8. **Sem overwhelm.** Se o achado não muda a próxima ação, não entra no topo.
9. **Explique recalibração.** Se uma auditoria mais profunda encontrar evidência nova e a nota cair, diga explicitamente que a queda veio da evidência nova, não da correção aplicada.
10. **Não cure auditor calando boa prática.** Não sugerir hardcode de URLs/configs só para reduzir alerta. Primeiro classifique se `process.env` é configuração não sensível ou segredo real.
11. **Paths são parte do produto.** Em setups com workspace raiz + múltiplos agentes, auditar integridade de paths de skills e scripts é obrigatório antes de dizer que skills estão ok.
12. **Score é operacional, não gamificação.** A pessoa não deve “caçar nota”; deve reduzir risco real. Não sugerir mudanças cosméticas só para subir score.

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
- `full-maintenance` reduz fricção operacional, mas não elimina aprovação para ações sensíveis, destrutivas, externas ou com risco de lockout.
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
- paths de skills e scripts válidos para o workspace raiz e para cada agente isolado;
- sem skill apontando para script inexistente, caminho absoluto de outro agente ou `../` frágil;
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


## Critical Systems Deep Dive

Algumas áreas são críticas demais para auditoria superficial. Quando qualquer uma delas aparecer como ausente, quebrada, desconhecida, degradada ou essencial para o perfil do agente, faça uma **análise cirúrgica obrigatória** antes de pontuar ou concluir.

Áreas críticas:
- memory / embeddings / FTS / LCM / recall;
- backup / GitHub / rollback;
- security / gateway / exec / elevated / sandbox;
- secrets / `.env` / tokens / 1Password;
- crons que executam ação externa ou backup;
- runtime performance: sessões, SQLite, logs, media, cache, delivery queue;
- skill and script path integrity em setups multi-agente ou workspace raiz compartilhado.

Fluxo obrigatório:

1. **Fast scan** — detectar sinais de risco nas áreas críticas.
2. **Surgical pass** — aprofundar somente nas áreas críticas detectadas ou essenciais para o agente.
3. **Executive output** — continuar mostrando só score, veredito, top 3 riscos e próximo passo.
4. **Deep appendix** — mostrar evidências completas somente no modo `deep` ou quando o usuário pedir.

Regra: simplicidade na devolutiva não autoriza análise rasa. Se a área é crítica, verifique com evidência.

### Surgical pass — Memory / Recall

Use quando o agente depende de memória, contexto, segundo cérebro, busca, curso, atendimento recorrente ou personalização.

Verifique, quando disponível:
- arquivos totais vs arquivos indexados;
- número de chunks;
- FTS disponível;
- embeddings disponíveis e cache pronto;
- última indexação ou freshness provável;
- erros recentes de indexação/search/LCM;
- tamanho de `lcm.db`, bancos SQLite e caches;
- presença de arquivos essenciais (`MEMORY.md`, `AGENTS.md`, `HEARTBEAT.md`, `TOOLS.md`) quando o template exigir;
- fallback funcional se embeddings não estiverem disponíveis;
- risco prático: o agente vai esquecer, alucinar recall, ficar lento ou só perder busca semântica?

Comandos úteis:

```bash
openclaw memory status --deep || true
find . -maxdepth 3 -type f \( -name 'MEMORY.md' -o -name 'AGENTS.md' -o -name 'HEARTBEAT.md' -o -name 'TOOLS.md' \) -print
find ~/.openclaw -type f \( -name 'lcm.db' -o -name '*.sqlite' -o -name '*.db' \) -printf '%s %p\n' 2>/dev/null | sort -nr | head -20
```

Não conclua “memória ok” só porque existe `MEMORY.md`. Memória ok exige cobertura, busca ou fallback, e ausência de erro crítico.

### Surgical pass — Backup / Rollback

Use quando houver repo sujo, falta de remoto, host de produção, aluno/cliente real ou mudança planejada.

Verifique:
- `git remote -v`;
- `git status --short`;
- último commit;
- branch tracking;
- backup automático ou cron de sync;
- snapshots existentes;
- divergência local/remoto;
- risco de sobrescrever trabalho humano.

Não conclua “tem backup” só porque existe Git. Precisa haver remoto, frequência ou checkpoint verificável.

### Surgical pass — Security / Access

Use quando houver canal público/grupo, exec/elevated, gateway, SSH, tokens ou host remoto.

Verifique:
- `openclaw security audit --deep`;
- gateway loopback vs público;
- políticas de DM/grupo/canal;
- exec/elevated/safeBins;
- SSH/portas expostas;
- fail2ban/UFW quando remoto;
- multi-user context risk;
- plugin allowlist e versões.

Não normalize `exec full` sem cruzar com o perfil do agente. Em agente pessoal pode ser aceitável; em grupo público pode ser crítico.

### Surgical pass — Secrets

Use quando houver `.env`, tokens, logs, repo público, aluno/cliente ou suspeita de credencial hardcoded.

Verifique sem revelar valores:
- padrões de token;
- `.env` commitado ou exposto;
- credenciais fora do 1Password/secret manager;
- logs com possíveis tokens;
- repo público com arquivos sensíveis.

Nunca cole segredo no relatório. Informe só tipo e path aproximado.

#### Heurística para `process.env`

Nem todo `process.env` é segredo. Antes de classificar como critical ou sugerir patch:

- **Config não sensível:** URLs/base URLs, portas, feature flags, nomes de ambiente, caminhos locais. Ex.: `VOBI_API`, `VOBI_CDP`, `PORT`, `BASE_URL`. Isso pode ser warning/low se estiver mal documentado, mas não é segredo por si só.
- **Possível segredo:** nomes com `KEY`, `TOKEN`, `SECRET`, `PASSWORD`, `PRIVATE`, `CLIENT_SECRET`, `WEBHOOK_SECRET`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GITHUB_TOKEN`, `GH_TOKEN`, `API_KEY`.
- **Env-harvesting real:** código que enumera/exporta `process.env` inteiro, envia variáveis para rede/log externo, ou combina leitura ampla de env + transmissão remota sem allowlist clara.

Regra: não recomendar substituir variável de ambiente por string hardcoded quando ela é configuração não sensível. Preferir allowlist explícita, validação de env, nomes menos ambíguos, comentário de segurança ou suppressão documentada do falso positivo.

### Surgical pass — Runtime Performance

Use quando houver lentidão, sessões antigas, SQLite grande, logs grandes, crons ruidosos ou contexto próximo do limite.

Verifique:
- maiores arquivos de runtime;
- número/tamanho/idade de sessões;
- bancos SQLite/LCM/cache;
- logs e media;
- delivery failures;
- crons com erro recorrente;
- compaction/pruning configurados.

Diferencie “grande mas saudável” de “grande e degradando uso”.

### Surgical pass — Skill and Script Path Integrity

Use quando houver múltiplos agentes, workspace raiz compartilhado, skills na raiz + skills por agente, scripts auxiliares, symlinks, submodules, ou erro recorrente de “file not found”.

Objetivo: garantir que cada agente consiga carregar e executar as skills certas sem vazar contexto entre agentes.

Verifique:
- inventário de pastas `skills/` no workspace raiz e em cada workspace/agente;
- skills duplicadas com mesmo nome e conteúdo diferente;
- referências em `SKILL.md` para scripts, templates, arquivos auxiliares e paths relativos;
- scripts citados existem e são executáveis quando necessário;
- paths relativos resolvem a partir do diretório da skill, não de um cwd acidental;
- paths absolutos não apontam para workspace/agente errado;
- uso frágil de `../`, `~/`, `/root/...`, `/home/...` que quebra em instalação de aluno;
- symlinks quebrados;
- registries (`skills/_registry.md`, categoria `_registry.md`) apontam para arquivos existentes;
- separação entre skills globais compartilhadas e skills específicas de agente sensível;
- risco de agente de pacientes carregar skill da “influencer/Sidecar” ou vice-versa.

Comandos úteis:

```bash
find . -path '*/skills/*/SKILL.md' -print
find . -path '*/skills/*' -type l -exec ls -la {} \;
grep -RInE '(scripts/|\.sh|\.py|\.js|\.mjs|\.ts|\.json|\.md|/root/|/home/|~/|\.\./)' skills */skills 2>/dev/null | head -200
find skills -type f \( -name '*.sh' -o -name '*.py' -o -name '*.js' -o -name '*.mjs' \) -print
# If this skill repo includes the helper script:
python3 skill-checkup-openclaw/scripts/path_integrity_check.py .
```

Classificação:
- path quebrado em skill essencial: high;
- path absoluto de outro agente/workspace: high ou critical se vazar dados sensíveis;
- registry stale sem impacto imediato: low/medium;
- skills duplicadas entre raiz e agente: medium, high se carregamento for ambíguo.

Regra: não dizer “skills ok” só porque `SKILL.md` existe. Skill ok significa que paths, scripts e arquivos auxiliares resolvem no contexto do agente auditado.

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

### Recalibração e comparação entre rodadas

Se houver mais de uma rodada (`quick` → `standard` → `deep`, antes/depois de patch, ou aluno dizendo que “a nota baixou depois da correção”):

1. Separar claramente **score de triagem**, **score recalibrado por evidência nova** e **score pós-correção**.
2. Não comparar score superficial com score deep como se fossem a mesma régua.
3. Se o score cair após auditoria mais profunda, explicar: “a nota caiu porque apareceram evidências novas; não significa que a correção piorou o sistema”.
4. Se o score cair após patch, identificar qual eixo piorou e se a correção criou regressão real, tradeoff aceitável ou falso positivo.
5. Quando possível, mostrar uma linha curta: `52 triagem → 45 deep com criticals → 82 pós-correção`.

No modo `standard`, essa explicação deve caber dentro do `Veredito` ou do risco relevante. Não criar seção extra. Reforce que o objetivo não é “ganhar nota”, é reduzir risco real.

### Deduções sugeridas

| Problema verificado | Dedução |
|---|---:|
| Sem backup/sync verificável | -20 |
| GitHub/origin ausente | -15 |
| Repo sujo sem commit/backup | -10 |
| Memória crítica ausente/corrompida | -15 |
| Sem memória semântica e sem fallback FTS em agente dependente de memória | -12 |
| Skills registry quebrado | -10 |
| Paths de skills/scripts quebrados em skill essencial | -10 a -20 |
| Skill path mistura agente sensível com agente público/marketing | -15 a -25 |
| Sem heartbeat em agente proativo | -8 |
| Cron essencial falhando repetidamente | -8 |
| Sem watchdog/restart em host remoto | -12 |
| Runtime degradado por sessão/cache/logs | -10 a -20 |
| Gateway exposto sem proteção clara | -25 |
| Segredo real hardcoded | -30 |
| Possível falso positivo de secret/env sem evidência de valor sensível | -0 a -5 |
| SSH/root remoto inseguro | -15 |
| Falta acesso essencial para executar função do agente | -10 |
| Acesso excessivo para contexto multiusuário | -10 a -25 |
| Estrutura de pastas confusa | -5 |
| Docs/organização do workspace stale | -5 |

### Travas de nota

Aplique o menor teto que aparecer:

| Condição | Score máximo |
|---|---:|
| Segredo real hardcoded ou token exposto | 40 |
| Env-harvesting real confirmado | 40 |
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

### 3. Fazer surgical pass nas áreas críticas

Antes de classificar achados, revise o fast scan. Se memory, backup, security, secrets, crons externos, runtime performance ou paths de skills e scripts aparecerem como risco, desconhecidos ou essenciais para o perfil do agente, execute o **Critical Systems Deep Dive** correspondente.

Não avance para score/veredito enquanto uma área crítica estiver baseada só em inferência superficial. Se não for possível verificar, marque como `unknown` e explique o impacto prático sem tratar como falha confirmada.

### 4. Classificar achados

Para cada achado relevante, registre internamente:

```md
- [severity/urgency/confidence] Título
  Eixo: readiness/course/performance/compliance/access
  Evidência: comando/path/observação curta
  Impacto: por que importa para operação
  Próxima ação: verbo claro
  Dono: agente ou humano
```

### 5.1 Multi-workspace output rule

Se detectar múltiplos workspaces/agentes, mantenha o `standard` simples. Adicione somente um bloco curto `Mapa detectado`, com no máximo 4 linhas:

```md
Mapa detectado:
- Raiz: skills globais/compartilhadas
- Agente pacientes: skills clínicas/guardrails
- Sidecar: vídeo/design/conteúdo
```

Regras:
- não listar todos os arquivos, scripts ou paths no standard;
- não gerar um sub-relatório por workspace;
- se houver problema de path, ele deve aparecer como um dos Top 3 riscos apenas quando muda a próxima ação;
- detalhes completos ficam no `deep` ou no PRD/plano após o usuário responder **bora**.

### 5. Gerar resposta padrão

No modo `standard`, use exatamente esta estrutura curta e **não adicione nenhuma seção além dela**:

```md
# Agent Readiness — {nome}

Score: {N}/100 — {veredito}
Confiança: {alta | média | baixa} — {1 frase curta se houver área crítica não verificada}

Veredito:
{1-3 frases. Pode operar? Em que condição?}

{Se houver múltiplos workspaces/agentes:
Mapa detectado:
- {Raiz/agente 1: função}
- {Agente 2: função}
- {Agente 3: função}
}

Top 3 riscos que eu atacaria:
1. {risco + impacto}
2. {risco + impacto}
3. {risco + impacto}

Modo de execução:
Existem 3 modos: `audit-only`, `fix-capable` e `full-maintenance`.
Este agente está em **{modo}** — com isso, eu {posso fazer X / não posso fazer Y}.
{Se modo != full-maintenance: Se você quiser uma jornada com menos pedidos operacionais, dá para me colocar em `full-maintenance`; ainda assim login/OAuth, firewall/SSH, update, envio externo e mudanças destrutivas continuam pedindo aprovação explícita.}

Eu posso assumir:
- Criar o plano de ação.
- Fazer backup/snapshot.
- Executar o que for reversível e permitido pelo modo atual.

Seu trabalho vai ser aprovar estas etapas:
- {login/OAuth/conta/token/firewall/SSH/envio externo, somente quando necessário}

Próximo movimento:
Só responde **bora** e eu monto o plano/PRD de correção, faço backup e começo.
```

Não inclua tabela executiva no `standard` salvo se o usuário pedir. Não inclua “achados bons”, “problemas menores” ou observações técnicas. O fechamento deve reduzir carga cognitiva: não despeje uma lista de tarefas para o humano; transforme em plano que o agente pode executar e escale apenas os bloqueios humanos reais.

### 6. Gerar modo deep

No modo `deep`, depois da resposta padrão, adicione:

```md
## Eixos internos
| Eixo | Status | Evidência curta |

## Findings relevantes
| Severidade | Urgência | Confiança | Achado | Dono |

## Apêndice técnico
{comandos/paths sem segredos}

## Path inventory
{somente no deep: workspace raiz, agentes, skill roots, duplicatas, refs quebradas}
```

### 7. Fechar com decisão leve

No final, não despeje novas tarefas. Feche com uma chamada leve para ação:

> “Só responde **bora** e eu monto o plano/PRD de correção, faço backup e começo.”

Se o usuário aprovar, crie um PRD de correção passo a passo. Em setup multi-workspace, o PRD deve incluir um mapa de escopo: skills globais, skills por agente, scripts compartilhados, paths a corrigir e testes de carregamento por agente. O PRD deve começar com backup/snapshot, declarar o modo de permissão necessário (`audit-only`, `fix-capable` ou `full-maintenance`), separar o que o agente executa sozinho, marcar exatamente onde precisa de humano para login, conta, OAuth, token, firewall/SSH ou aprovação externa, e terminar com critérios de sucesso + re-run do checkup para comparar score recalibrado vs pós-correção.

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
- Aprovar update/restart de gateway em agente produtivo.
- Autorizar envio externo ou ação representando o usuário.
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
Confiança: alta — evidências principais verificadas.

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
