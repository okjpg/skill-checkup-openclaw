---
name: skill-checkup-openclaw
description: Use when auditing OpenClaw agents, workspaces, or hosts for production readiness, safety, backup/GitHub, memory/recall, skills, heartbeat, crons, watchdog, security, access, runtime bloat, or course baseline fit.
---

# Skill Checkup OpenClaw

Audita se um agente OpenClaw está pronto para operar sem virar dívida operacional. A entrega é **executiva, decisória e acionável**: score, veredito, top 3 riscos e próximo passo.

Pergunta central:

> Esse agente pode operar com usuário/cliente real? Se não, qual é o próximo movimento mais importante?

## When to Use

Use quando o alvo for OpenClaw e a pergunta envolver:

- readiness para produção, curso, aluno, cliente ou grupo;
- segurança, secrets, gateway, sandbox, exec/elevated ou canais;
- backup, GitHub, rollback, crons, heartbeat ou watchdog;
- memória, embeddings, FTS, LCM, recall ou segundo cérebro;
- lentidão, runtime inchado, sessões/logs/cache grandes;
- skills, registries, scripts auxiliares ou paths em setup multi-workspace;
- auditoria antes de corrigir, migrar ou dar acesso para terceiros.

## When NOT to Use

Não use para:

- Claude Desktop, Cursor, LangChain, n8n, servidor Linux genérico ou framework que não seja OpenClaw;
- auditoria de código de app/produto sem relação com agente OpenClaw;
- pentest profundo, hardening completo de infraestrutura ou compliance formal;
- publicação/envio externo em nome do usuário;
- correções destrutivas ou mudanças de firewall/SSH sem aprovação explícita;
- “ganhar nota” com mudanças cosméticas. A nota é operacional, não gamificação.

## Recursos empacotados

- `scripts/path_integrity_check.py` — scanner read-only para inventariar roots de skills, duplicatas, symlinks quebrados, refs de scripts/caminhos em `SKILL.md` e links quebrados de registries.

Se houver `ANTES-DE-RODAR.md`, leia antes de executar para usuário não técnico.

## Regra-mãe

**Executive-first. Deep internally. Short by default.**

A skill pode verificar muita coisa por baixo, mas o modo padrão mostra só:

1. Score + confiança
2. Veredito operacional
3. Top 3 riscos que importam agora
4. Modo de execução
5. O que o agente pode assumir
6. O que o humano precisa aprovar
7. Próximo movimento

Tabela, checklist completo e evidências técnicas só entram em `deep` ou se o usuário pedir.

## Output Contract — standard

No modo `standard`, siga exatamente o template em `references/report-template.md`.

Regras obrigatórias:
- usar somente estas seções, nesta ordem: `Agent Readiness`, `Score/Confiança`, `Veredito`, `Mapa detectado` (somente se houver múltiplos workspaces/agentes), `Top 3 riscos que eu atacaria`, `Modo de execução`, `Eu posso assumir`, `Seu trabalho vai ser aprovar estas etapas`, `Próximo movimento`;
- terminar com: **“Só responde bora e eu monto o plano, faço backup e começo.”**;
- mencionar que o próximo passo é montar plano/PRD de correção com backup antes da execução;
- não adicionar `Achados bons`, `Problemas menores`, `Observações`, `Checklist`, `Evidências`, `Detalhes técnicos`, tabelas não solicitadas ou lista completa de paths/arquivos.

Bons sinais e problemas menores entram só internamente para calibrar score. Só aparecem se mudarem uma das 3 ações principais.

## Modos

| Modo | Quando usar | Saída |
|---|---|---|
| `quick` | triagem em 2-3 min | score aproximado + top 3 riscos |
| `standard` | padrão | resposta executiva curta + plano |
| `deep` | pré-produção, incidente, cliente real | resposta executiva + evidências/apêndice técnico |

Se o usuário não escolher, use `standard`.

## Execution Permission Preflight

Antes de prometer correções, classifique o nível real de permissão da sessão/alvo:

| Modo | Significado | Pode fazer |
|---|---|---|
| `audit-only` | só leitura ou permissões incertas | diagnosticar, gerar PRD, listar bloqueios |
| `fix-capable` | write/edit/exec básico disponíveis | corrigir arquivos, registries, backups locais, limpezas reversíveis |
| `full-maintenance` | exec/elevated/security full no host alvo | mexer em serviço, systemd, gateway, permissões, firewall/SSH com aprovação |

`full-maintenance` reduz fricção operacional, mas não elimina aprovação para login/OAuth, firewall/SSH, update/restart produtivo, envio externo, ação destrutiva ou risco de lockout.

## Perfis de agente

Classifique antes de pontuar:

| Perfil | Tolerância | Exemplo |
|---|---|---|
| `personal` | mais autonomia aceitável | agente pessoal do Bruno |
| `internal-test` | pode ter ressalvas | bot de curso teste |
| `student` | precisa ser simples e seguro | agente de aluno |
| `client-production` | rigor alto | cliente/pagante |
| `group-public` | rigor máximo de acesso/contexto | grupo Telegram/WhatsApp |

Use o perfil para calibrar. `exec full` pode ser aceitável em `personal`, mas crítico em `group-public`.

## Eixos internos

Calcule internamente, sem despejar todos por padrão:

1. **Operational Readiness** — gateway, versão, channels, Git/remoto, backup/sync, heartbeat, crons, watchdog, sessões, workspace.
2. **Course Baseline Fit** — estrutura ensinada no curso, GitHub/backup, memória/FTS, arquivos base, skills/registry, security sem critical, docs mínimas.
3. **Runtime Performance Risk** — sessões, SQLite/LCM/cache, logs, media, queues, failed tasks, compaction, contexto, crons ruidosos.
4. **Official OpenClaw Compliance** — `openclaw doctor/status/health/security/memory`, sandbox/tool policy, update posture, diagnostics.
5. **Access & Execution Capability** — ferramentas disponíveis, GitHub/1Password/GOG/Tailscale/SSH/browser/nodes, fallbacks e risco de acesso excessivo.

## Critical Systems Deep Dive

Se memory, backup, security, secrets, crons externos, runtime performance ou paths de skills/scripts aparecerem como risco, desconhecidos ou essenciais para o perfil, faça análise cirúrgica antes de pontuar.

Use `references/critical-systems.md` para checklists de deep dive. Regra: simplicidade na resposta não autoriza análise rasa.

## Workflow

### 1. Definir alvo

Identifique:
- agente/workspace/host auditado;
- perfil (`personal`, `internal-test`, `student`, `client-production`, `group-public`);
- modo (`quick`, `standard`, `deep`);
- permissões reais (`audit-only`, `fix-capable`, `full-maintenance`);
- se há múltiplos workspaces/agentes.

### 2. Rodar checks read-only

Priorize evidência. Use somente leituras e comandos não destrutivos.

Checklist de comandos: `references/read-only-checks.md`.

Se houver setup multi-workspace, scripts auxiliares ou risco de path:

```bash
python3 skill-checkup-openclaw/scripts/path_integrity_check.py .
```

O scanner é evidência, não relatório final.

### 3. Fazer surgical pass nas áreas críticas

Revise o fast scan. Se uma área crítica estiver baseada só em inferência superficial, não avance para score/veredito. Verifique ou marque como `unknown`.

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

Use `references/scoring.md` para severidade, deduções, travas e veredito.

### 5. Gerar resposta

- `standard`: usar `references/report-template.md` e não adicionar seções extras.
- `deep`: depois do standard, usar o formato de evidências em `references/deep-output-and-execution.md`.
- Multi-workspace no standard: incluir só `Mapa detectado` com até 4 linhas. Detalhes completos ficam no `deep` ou no PRD pós-**bora**.

### 6. Fechar com decisão leve

A próxima ação padrão é oferecer planejamento executável + backup, não despejar tarefa no humano.

Se o usuário aprovar (“bora”, “segue”, “executa”, “corrige”), antes de qualquer mudança:

1. criar snapshot/backup;
2. registrar manifest;
3. confirmar que o backup existe;
4. só então aplicar mudanças reversíveis e permitidas.

Detalhes de backup e divisão agente/humano: `references/deep-output-and-execution.md`.

## Anti-overwhelm

Não colocar no topo:
- warnings cosméticos;
- itens sem evidência;
- detalhes de comando;
- histórico repetido sem mudança;
- boas práticas que não mudam risco real;
- eixo completo se só uma ação importa.

Colocar no topo:
- perda de dados;
- risco de segurança;
- falha de entrega;
- ausência de rollback;
- login humano necessário;
- bloqueio para usuário final;
- lentidão/degradação que afeta uso real.

## Common Mistakes

- Copiar só o `SKILL.md` e esquecer `scripts/`/`references/`.
- Dizer “memória ok” só porque existe `MEMORY.md`.
- Dizer “backup ok” só porque existe Git local sem remoto/sync.
- Tratar todo `process.env` como segredo ou sugerir hardcode para calar alerta.
- Gerar relatório gigante no modo `standard`.
- Prometer correção sem classificar permissão real.
- Executar correção sem backup.
- Listar tarefas para o humano em vez de assumir plano e escalar só aprovações reais.
