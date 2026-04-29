# Template de resposta standard

## Multi-workspace output rule

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

### Gerar resposta padrão

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


### Exemplo de saída standard

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
