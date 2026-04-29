# Scoring e severidade

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

