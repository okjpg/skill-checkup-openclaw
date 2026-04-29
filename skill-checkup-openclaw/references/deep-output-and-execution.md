# Deep output, backup e execução

## Gerar modo deep

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

## Fechar com decisão leve

No final, não despeje novas tarefas. Feche com uma chamada leve para ação:

> “Só responde **bora** e eu monto o plano/PRD de correção, faço backup e começo.”

Se o usuário aprovar, crie um PRD de correção passo a passo. Em setup multi-workspace, o PRD deve incluir um mapa de escopo: skills globais, skills por agente, scripts compartilhados, paths a corrigir e testes de carregamento por agente. O PRD deve começar com backup/snapshot, declarar o modo de permissão necessário (`audit-only`, `fix-capable` ou `full-maintenance`), separar o que o agente executa sozinho, marcar exatamente onde precisa de humano para login, conta, OAuth, token, firewall/SSH ou aprovação externa, e terminar com critérios de sucesso + re-run do checkup para comparar score recalibrado vs pós-correção.

Regra: a próxima ação padrão após o audit é **oferecer planejamento executável + backup**, não jogar tarefas no humano.

Nunca execute correções automaticamente sem pedido claro. Se o usuário aprovar execução direta, ainda assim faça backup/snapshot antes.

## Divisão: agente vs humano

## O agente pode resolver, com backup antes

- Commit/backup de arquivos locais.
- Atualizar registries e organização do workspace.
- Organizar arquivos fora do lugar para `archive/`.
- Corrigir paths de skills.
- Criar relatórios e manifests.
- Rodar checks read-only.
- Preparar comandos de firewall/SSH sem aplicar.
- Ajustar crons somente com aprovação explícita.
- Arquivar sessões/logs/mídias antigas somente se for reversível e aprovado.

## O humano precisa fazer ou aprovar

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

