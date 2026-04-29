# Critical Systems Deep Dive

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
Se esta skill incluir o helper:
python3 skill-checkup-openclaw/scripts/path_integrity_check.py .
```

Classificação:
- path quebrado em skill essencial: high;
- path absoluto de outro agente/workspace: high ou critical se vazar dados sensíveis;
- registry stale sem impacto imediato: low/medium;
- skills duplicadas entre raiz e agente: medium, high se carregamento for ambíguo.

Regra: não dizer “skills ok” só porque `SKILL.md` existe. Skill ok significa que paths, scripts e arquivos auxiliares resolvem no contexto do agente auditado.

