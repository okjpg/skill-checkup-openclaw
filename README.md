# Skill Checkup OpenClaw

**v1.3.0 — mini-curso OpenClaw por Bruno Okamoto**

Skill instalável para auditar agentes no **OpenClaw**.

Ela foi feita exclusivamente para responder uma pergunta simples:

> Esse agente OpenClaw está pronto para operar com segurança, estabilidade e baixo risco operacional?

A skill escaneia muita coisa por baixo, mas a devolutiva é propositalmente simples. A ideia não é gerar um calhamaço técnico; é dar um diagnóstico executivo com score, veredito, top 3 riscos e próximo passo claro.

## Exclusiva para OpenClaw

Use esta skill somente em agentes, workspaces e hosts OpenClaw.

Ela assume que existem ou podem existir:

- `openclaw status`
- `openclaw health`
- `openclaw security audit`
- `openclaw memory status`
- gateway OpenClaw
- agentes OpenClaw
- sessões OpenClaw
- crons OpenClaw
- workspace com `MEMORY.md`, `HEARTBEAT.md`, `AGENTS.md`, `TOOLS.md`
- skills OpenClaw
- paths de skills e scripts auxiliares
- canais como Telegram, WhatsApp, Slack etc.

Não é uma skill genérica para auditar qualquer servidor ou qualquer framework de agentes.


## Para agentes: leia antes de rodar

Antes de executar a skill para uma pessoa, leia [`ANTES-DE-RODAR.md`](ANTES-DE-RODAR.md).

Esse arquivo explica, em linguagem simples, como apresentar o checkup para usuários não técnicos e como evitar transformar a auditoria em um relatório técnico gigante.

## O que ela analisa

A auditoria calcula internamente 5 eixos.

### 1. Operational Readiness

Se o agente consegue operar sem depender de sorte:

- gateway ativo
- versão do OpenClaw
- canais configurados
- Git/repo remoto
- estado limpo ou sujo do workspace
- backup/sync automático
- heartbeat
- crons
- watchdog/restart
- integridade básica de sessões
- organização do workspace

### 2. Course Baseline Fit

Se o agente está alinhado com o padrão ensinado no mini-curso:

- GitHub privado ou estratégia clara de backup
- backup automático
- memória semântica ou fallback FTS
- arquivos base quando o template exigir: `MEMORY.md`, `HEARTBEAT.md`, `AGENTS.md`, `TOOLS.md`
- skills organizadas
- registry funcionando
- security audit sem critical
- gateway local/tokenizado
- políticas corretas para canais
- 1Password ou equivalente seguro para credenciais
- documentação mínima para o aluno entender a estrutura


### Skill and script path integrity

A v1.2.0 adiciona uma checagem importante para setups avançados: workspace raiz com múltiplos agentes isolados.

Ela verifica se skills e scripts resolvem paths corretamente em cada contexto:

- skills globais na raiz;
- skills específicas por agente;
- scripts citados em `SKILL.md`;
- templates e arquivos auxiliares;
- paths absolutos de outro workspace;
- uso frágil de `../`, `~/`, `/root/...` ou `/home/...`;
- registries apontando para arquivos inexistentes;
- risco de um agente sensível carregar skill de outro agente.

Exemplo: um agente de pacientes não deve herdar acidentalmente uma skill de vídeo/design da Sidecar, e uma skill da Sidecar não deve depender de script dentro do workspace do agente clínico.


### Como fica o report em multi-workspace

Mesmo quando existem vários agentes dentro de um workspace raiz, o report padrão continua curto.

Ele pode mostrar um bloco pequeno de mapa detectado:

```md
Mapa detectado:
- Raiz: skills globais/compartilhadas
- Pacientes: skills clínicas/guardrails
- Sidecar: vídeo/design/conteúdo
```

A lista completa de paths, scripts e duplicatas não aparece no report padrão. Ela fica para o modo `deep` ou para o PRD de correção depois que o usuário responder **bora**.

### 3. Runtime Performance Risk

Se o agente está ficando lento ou inchado:

- tamanho das sessões
- número e idade das sessões ativas
- arquivos `sessions.json`
- bancos SQLite/LCM/cache
- logs grandes
- pasta `media/`
- filas de delivery falhando
- tasks acumuladas
- crons gerando contexto demais
- compaction/pruning
- proximidade do limite de contexto

### 4. Official OpenClaw Compliance

Se o agente está alinhado com ferramentas e práticas oficiais do OpenClaw:

- `openclaw status`
- `openclaw health --json`
- `openclaw security audit`
- `openclaw memory status --deep`
- postura de update
- sandbox/tool policy
- session pruning/compaction
- diagnostics disponíveis

### 5. Access & Execution Capability

Se o agente tem acesso suficiente para resolver problemas sem ficar perigoso demais:

- `exec/process`
- `read/write/edit/apply_patch`
- elevated/full access
- GitHub CLI
- 1Password CLI
- GOG/Google auth
- Tailscale/SSH
- cron/message/browser/nodes
- modelo/provider/fallbacks/rate limit


## Análise cirúrgica em áreas críticas

A v1.1 adiciona uma regra importante: algumas áreas não podem ser avaliadas “por cima”.

Quando a skill encontra risco ou incerteza em pontos críticos, ela faz um segundo passe mais cirúrgico antes de concluir:

- memória, embeddings, FTS, LCM e recall;
- backup, GitHub e rollback;
- segurança, gateway, exec, elevated e sandbox;
- secrets, `.env`, tokens e 1Password;
- crons que executam ação externa ou backup;
- performance: sessões, SQLite, logs, media, cache e filas de entrega;
- paths de skills e scripts em setups multi-agente.

Isso não muda a promessa principal: a devolutiva continua simples.

A diferença é que, por baixo, a skill é obrigada a verificar evidências antes de dizer que algo crítico está ok ou quebrado.

Exemplo: ela não pode dizer “memória ok” só porque existe `MEMORY.md`. Precisa olhar cobertura, chunks, FTS/embeddings, freshness, erros e risco prático para recall.

## Como a resposta funciona

A skill evita despejar todos os achados técnicos.

No modo padrão, a saída agora é contratual: não deve trazer “achados bons”, “problemas menores”, checklist ou tabela técnica. Esses pontos ficam internos, usados só para calibrar score e escolher os top 3 riscos.

A resposta padrão mostra:

1. score de 0 a 100
2. confiança da análise
3. veredito claro
3. top 3 riscos que importam agora
4. modo de execução atual
5. o que o agente pode assumir
6. quais etapas o humano precisa aprovar
8. próximo passo simples

O relatório técnico completo só aparece se você pedir modo `deep`.

## Modos de execução

A skill sempre identifica o modo operacional do agente que está auditando:

- `audit-only` — só pode diagnosticar e gerar plano
- `fix-capable` — pode editar arquivos, fazer backup e corrigir coisas reversíveis
- `full-maintenance` — pode mexer em serviço, gateway, permissões e host, sempre com aprovação humana para ações sensíveis. Reduz fricção operacional, mas não significa “sem aprovação” para update, firewall/SSH, envio externo, OAuth ou mudanças destrutivas.

## Exemplo de report

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
Só responde **bora** e eu monto o plano/PRD de correção, faço backup e começo.
```


## Helper opcional para paths

A v1.2.0 inclui um scanner read-only para ajudar o agente a auditar paths de skills e scripts:

```bash
python3 skill-checkup-openclaw/scripts/path_integrity_check.py .
```

Ele não corrige nada sozinho. Só gera evidências para o agente usar no checkup, no modo `deep` ou no PRD de correção após o usuário responder **bora**.

## Instalação

Copie a **pasta inteira** da skill para o diretório de skills do seu agente OpenClaw. Não copie só o `SKILL.md`: a skill depende de `scripts/` e `references/`.

Exemplo:

```bash
cp -R skill-checkup-openclaw ~/.openclaw/skills/
```

Validação rápida:

```bash
test -f ~/.openclaw/skills/skill-checkup-openclaw/SKILL.md
test -f ~/.openclaw/skills/skill-checkup-openclaw/scripts/path_integrity_check.py
test -d ~/.openclaw/skills/skill-checkup-openclaw/references
```

Depois peça ao agente:

```text
Rode a skill checkup OpenClaw neste agente.
```

Ou:

```text
Audite se este agente OpenClaw está pronto para produção.
```

## Status

Esta é uma **v1.3.0** em cima da v1 inicial.

Ela nasceu do mini-curso OpenClaw do Bruno Okamoto para ajudar alunos e operadores a enxergarem rapidamente se um agente está pronto, perigoso, lento, mal configurado ou só precisando de manutenção básica.

A v1.3.0 prioriza empacotamento confiável para curso/terceiros: instalação da pasta inteira, apenas um `SKILL.md` real no repo, evals mínimos, fixtures não detectáveis por scanner de skills e `SKILL.md` enxuto com referências em `references/`. Ela mantém análise cirúrgica nas áreas críticas, contrato rígido de saída no modo padrão e helper opcional para path integrity. Ainda não tenta corrigir tudo automaticamente.
