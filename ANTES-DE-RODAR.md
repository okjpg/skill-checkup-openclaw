# Antes de rodar o Skill Checkup OpenClaw

Este texto é para o agente ler antes de executar a skill e explicar para a pessoa, em linguagem simples, o que vai acontecer.

## Explicação curta para enviar ao usuário

Vou rodar um checkup do seu agente OpenClaw.

Ele olha várias camadas por baixo — segurança, memória, GitHub, backup, sessões, crons, canais, performance e permissões — mas eu não vou te devolver um relatório técnico gigante.

A devolutiva vai ser simples:

1. uma nota de 0 a 100;
2. um veredito claro: pronto, operável com ressalvas ou não recomendado;
3. os 3 riscos mais importantes;
4. o que eu consigo resolver sozinho;
5. o que precisa de aprovação humana;
6. o próximo passo.

Você não precisa entender todos os detalhes técnicos. A ideia é saber se o agente está seguro e saudável o suficiente para continuar operando — e, se não estiver, qual é a próxima ação certa.


## O que significa “análise cirúrgica”

Em coisas críticas, o agente não deve passar batido.

Se aparecer risco em memória, backup, segurança, secrets, crons importantes ou performance, ele faz um segundo passe mais cuidadoso antes de dar o veredito.

Isso não significa que você vai receber um relatório maior. Significa que a resposta simples vai estar melhor fundamentada.

## Como a pessoa deve lidar com o resultado

Não trate a nota como boletim escolar.

A nota serve para priorizar ação, não para julgar se o agente é “bom” ou “ruim”.

Um agente com 60/100 pode estar perfeitamente usável para teste interno. Um agente com 82/100 pode ser perigoso se tiver uma falha crítica escondida, como gateway exposto ou segredo hardcoded.

O que importa é:

- existe risco de segurança?
- existe risco de perder dados?
- existe backup?
- o agente está ficando lento?
- tem coisa quebrada que impede operação real?
- o humano precisa fazer algum login/aprovação?

## Como interpretar os vereditos

### ✅ Pronto para operar

O agente está em bom estado para o uso esperado.

Ainda pode ter melhorias, mas nada crítico bloqueia a operação.

### ⚠️ Operável com ressalvas

O agente pode continuar sendo usado, mas existem riscos ou dívidas que devem ser corrigidos.

Esse é o resultado mais comum.

Não é pânico. É manutenção.

### ❌ Não recomendado operar

Existe risco importante: segurança, perda de dados, ausência de backup, canal mal configurado, gateway exposto, credencial em lugar errado ou performance muito degradada.

Neste caso, o certo é parar, fazer backup e corrigir antes de colocar usuário/cliente/aluno dependendo do agente.

## O que o agente deve evitar

Não despeje tudo que encontrou.

A pessoa não quer um inventário de 80 linhas. Ela quer saber:

- está seguro?
- está funcionando?
- o que precisa fazer agora?
- o que você consegue assumir?
- onde preciso aprovar?

Detalhes técnicos só entram se forem necessários para justificar uma decisão ou se a pessoa pedir modo deep.

## Frase de abertura recomendada

Antes de rodar, diga:

> Vou fazer um checkup executivo do seu agente OpenClaw. Ele escaneia bastante coisa por baixo, mas vou te devolver só o que importa: nota, veredito, top 3 riscos e próximo passo. Se aparecer algo que exige login, token, firewall ou aprovação externa, eu separo claramente o que é comigo e o que é com você.

## Frase de fechamento recomendada

Depois do report, feche com:

> Só responde **bora** e eu monto o plano, faço backup e começo.

## Regra principal

O objetivo da skill não é provar que o agente sabe auditar.

O objetivo é reduzir ansiedade e transformar bagunça técnica em decisão simples.
