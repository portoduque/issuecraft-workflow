# IssueCraft Workflow

[![CI](https://github.com/portoduque/issuecraft-workflow/actions/workflows/ci.yml/badge.svg)](https://github.com/portoduque/issuecraft-workflow/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Workflow reutilizável, agnóstico de agente de IA, stack, framework e linguagem para implementar issues desde a descoberta do projeto até a validação humana, com segurança, performance, testes, detecção de drift e aprendizado controlado.

**Versão:** 0.10.0  
**Licença:** MIT  
**Idioma:** [English](README.md) · [Português (Brasil)](README.pt-BR.md)

---

## Comece em 3 passos

Você precisa de **Git**, **Python 3** para a instalação e um agente de programação compatível.

### 1. Clone o IssueCraft

```bash
git clone https://github.com/portoduque/issuecraft-workflow.git
cd issuecraft-workflow
```

### 2. Instale no seu projeto

```bash
python scripts/install.py /caminho/do/seu/projeto
```

Exemplos:

```bash
# Linux/macOS
python scripts/install.py ~/projetos/meu-sistema

# Windows
python scripts/install.py C:\dev\meu-sistema
```

O instalador copia somente o runtime do workflow e os pontos de entrada dos agentes. Ele **não muda a stack da aplicação** e **não cria decisões de arquitetura antecipadamente**.

### 3. Rode `implement-issue`

| Agente | Comando |
|---|---|
| Codex | `$implement-issue` |
| Claude Code | `/implement-issue` |
| Antigravity | `/implement-issue` |

Exemplo:

```text
/implement-issue
Implemente a issue #42: adicionar botão para mostrar/ocultar a senha no formulário de usuário.
```

No Codex, use `$implement-issue` em vez de `/implement-issue`.

**Isso já é suficiente para começar.** Na primeira execução, o IssueCraft entende como o repositório realmente funciona antes de alterar o código da aplicação.

---

## O que o IssueCraft faz

Existe um único workflow canônico `implement-issue` que:

- descobre linguagens, frameworks, gerenciamento de dependências, banco, migrations, testes, CI, lint, build, segurança e performance com base em evidências;
- trata projetos vazios com uma entrevista curta e adaptativa em vez de inventar uma stack;
- propõe um `PROJECT_PROFILE` para a realidade observada ou um `PROJECT_BLUEPRINT` para a arquitetura planejada;
- exige aprovação humana antes de persistir conhecimento importante do projeto;
- detecta drift nas execuções futuras;
- planeja e implementa a menor mudança coerente que atende a issue;
- modela mudanças materiais como contrato atual → delta solicitado → contrato resultante, preservando obrigações existentes não alteradas;
- aplica solution economy depois de entender o fluxo real: reutiliza capacidades adequadas já existentes no projeto/runtime/plataforma/dependências aprovadas antes de criar novo ownership;
- faz triagem obrigatória de segurança e performance;
- escolhe testes conforme o risco, sem depender de framework específico;
- exige evidence-or-zero para obrigações materiais, decompõe requisitos compostos e usa discrimination checks direcionados quando a força do teste é materialmente incerta;
- preserva integridade de escopo: replanning local/reversível continua autônomo, mas drift material de intenção/escopo da issue exige decisão humana;
- mantém um proof floor acima da simplicidade: correção/completude, segurança, acessibilidade, compatibilidade, preservação, confiabilidade e validação aplicável não podem ser trocadas por menos linhas/arquivos/tokens;
- conduz `In Progress → In Review → validação humana → Done`;
- gera um roteiro manual específico da issue ao entrar em `In Review`;
- aprende com o uso real, mas mantém persistência e adoção sob controle humano.

---

## Output compacto, evidência completa

O IssueCraft mantém análise e validação profundas, mas evita transformar cada handoff no chat em um relatório enorme.

A regra é:

> **Compactar a apresentação, nunca a evidência.**

Os detalhes ficam nos artefatos duráveis do projeto, como Profile, relatório de drift, plano de validação, relatório de execução ou proposta de melhoria. No chat, o IssueCraft prioriza estado atual, mudanças materiais, falhas/checks indisponíveis, riscos residuais, decisão humana necessária e próxima ação.

Checks rotineiros que passaram podem ser agrupados; casos `not_applicable` podem ser resumidos. Falhas, validações indisponíveis, riscos de segurança/performance, incerteza e human gates nunca são escondidos para economizar tokens.

Output compacto é uma **projeção do resultado completo da validação**, nunca um motivo para validar menos obrigações. Evidência parcial continua parcial: se membros materiais ainda não foram provados, a obrigação pai não vira `pass` integral.

Assim o histórico da conversa fica menor sem reduzir testes ou profundidade técnica.

---

## Solution economy sem code golf

O IssueCraft separa **economia de implementação** de simplesmente escrever menos código.

Depois de entender o fluxo afetado e o contrato, ele prefere:

```text
não criar implementação nova quando não é necessária
  ↓
reutilizar capacidade adequada já existente no projeto
  ↓
usar capacidade adequada do runtime/plataforma
  ↓
reutilizar dependência já aprovada/instalada
  ↓
só então criar a menor implementação nova coerente
```

O objetivo é **menos ownership e menos complexidade sem justificativa**, não o menor número de linhas ou arquivos. Uma solução maior é preferível quando a menor perderia comportamento obrigatório, validação, segurança, acessibilidade, compatibilidade, observabilidade, integridade de dados ou confiabilidade.

Em correções de bug, o IssueCraft também verifica se o sintoma citado na issue é apenas um dos caminhos até uma causa compartilhada. Quando a evidência do repositório mostra um invariante comum, ele prefere o menor ponto comum correto de enforcement e valida o blast radius mais amplo, em vez de duplicar guards entre callers.

Antes de `In Review`, o diff passa por uma revisão de ownership/complexidade para detectar abstrações, wrappers, dependências, configurações ou capacidades duplicadas sem necessidade comprovada. Boundaries legítimos não são tratados como bloat só porque adicionam código.

Delegação/subagents continuam opcionais. Se forem usados, o IssueCraft não presume que outro contexto herdou regras do projeto ou human gates; o workflow controlador continua responsável por reconciliar o resultado e validar o estado final.

---

## Primeira execução: projeto existente ou projeto vazio

```text
primeira execução
       ↓
inspecionar repositório
       ↓
┌─────────────────────────┬──────────────────────────┐
│ projeto existente       │ projeto novo/vazio       │
│                         │                          │
│ Project Discovery       │ Project Bootstrap        │
│                         │                          │
│ proposta de Profile     │ proposta de Blueprint    │
└────────────┬────────────┴─────────────┬────────────┘
             │                          │
             └──── aprovação humana ────┘
                         ↓
                 implementar issue
```

### Projeto existente

O IssueCraft procura evidências de:

- linguagens, runtimes, frameworks e bibliotecas estruturais;
- gerenciadores de dependências/pacotes e workspaces;
- persistência, bancos e migrations;
- testes unitários, integração, contrato, sistema, E2E e demais testes existentes;
- lint, format, análise estática/typecheck e build;
- CI/CD e automação de release;
- políticas/ferramentas de segurança e trust boundaries;
- ferramentas de performance, budgets, baselines e capacidade;
- arquitetura, módulos/serviços e convenções do repositório.

Ele propõe `.implement-issue/PROJECT_PROFILE.yaml`.

Quando algo não pode ser comprovado, permanece `unknown` ou `not_detected`. Falta de evidência não vira fato automaticamente.

### Projeto vazio ou quase vazio

O IssueCraft não tenta "descobrir" uma stack que ainda não existe.

Primeiro lê a documentação disponível; depois pergunta somente o que ainda precisa ser decidido para o scaffold atual. Decisões que podem continuar abertas ficam como `undecided`.

O resultado proposto é `.implement-issue/PROJECT_BLUEPRINT.yaml`.

A diferença é intencional:

- **Blueprint** = o que pretendemos construir.
- **Profile** = o que o repositório comprova que existe hoje.

Ambos exigem aprovação humana antes de serem persistidos.

---

## Ciclo da issue

```text
issue/tarefa
    ↓
entender contexto
    ↓
In Progress
    ↓
planejar por evidências
    ↓
implementar
    ↓
revisar segurança
    ↓
revisar performance
    ↓
validação automatizada baseada em risco
    ↓
gerar roteiro manual
    ↓
In Review
    ↓
validação humana
    ├── falhou → In Progress
    └── passou → Done
```

O IssueCraft pode preparar a issue para `In Review`, mas **Done pertence ao humano**. Testes automatizados, a própria IA exercitar a interface ou confiança no diff não substituem a validação humana final.

Durante a implementação, o contexto é recuperado progressivamente: o IssueCraft segue código, contratos e testes de maior sinal até resolver as lacunas materiais, sem tentar ler o repositório inteiro. Se correções repetidas falharem sem nova evidência, ele faz um diagnostic reset antes de outra alteração.

Em trabalhos não triviais que atravessam várias superfícies, o IssueCraft prefere incrementos pequenos e verificáveis e resolve cedo incertezas capazes de invalidar o plano com slices risk-first. Quando a correção depende de comportamento externo sensível à versão que o repositório não consegue comprovar, ele confere a versão detectada em documentação oficial e marca como `unverified` o que não puder confirmar.

A validação também considera a validade temporal da evidência: um resultado verde anterior só é reutilizado enquanto seus inputs relevantes continuarem materialmente iguais. Antes de `In Review`, o IssueCraft verifica se o diff enfraqueceu o quality bar do projeto, se migrations que exigem coexistência seguem uma sequência compatível de expand/migrate/contract e se mudanças de dependências estão sustentadas pelo lock state resolvido e por evidências relevantes de release/migration.

Se o trabalho for interrompido, o IssueCraft pode gravar um `.implement-issue/HANDOFF.md` compacto. Esse handoff é apenas uma hipótese de retomada: na sessão seguinte ele é reconciliado com o estado atual do repositório/VCS, tracker quando disponível e evidências duráveis de validação antes de qualquer edição. A evidência atual vence uma narrativa stale.

Decisões de implementação materialmente difíceis de reverter, quando ainda não determinadas pela issue, conhecimento aprovado do projeto, contratos existentes ou restrições inevitáveis, são tratadas como one-way doors e exigem decisão humana explícita. Escolhas locais e reversíveis continuam autônomas.

Para mudanças materiais de comportamento, o IssueCraft distingue o que foi **adicionado, modificado, removido, renomeado/preservado e unchanged-but-at-risk**. Comportamentos modificados carregam obrigações de preservação para cenários/campos/estados/caminhos existentes que a issue não removeu explicitamente; comportamento removido é validado como ausente, não como algo a ser restaurado.

Antes de `In Review`, uma revisão de coerência confronta issue/acceptance criteria, contratos/regras do projeto, behavior delta, diff implementado, evidência automatizada e roteiro manual. Toda mudança material no diff precisa de justificativa rastreável. Se o plano estiver errado mas o resultado pretendido da issue continuar igual, o IssueCraft replana autonomamente; se a própria issue virar materialmente outro trabalho, o humano decide.

Na retomada e em transições materiais de fase, o IssueCraft relê os inputs autoritativos e mutáveis necessários para a próxima decisão em vez de confiar na memória antiga do chat. Repositórios/specs externos podem servir de referência, mas permissão de leitura nunca implica autorização para modificar.

---

## Agnóstico de agente de IA

Existe um único core:

```text
core/WORKFLOW.md
```

Os arquivos específicos de agente são apenas adaptadores finos:

```text
.agents/skills/implement-issue/SKILL.md
.claude/skills/implement-issue/SKILL.md
```

O core não pode ramificar comportamento por fornecedor de IA. A validação do repositório procura vazamentos de nomes de fornecedores no core, e os adapters precisam permanecer comportamentalmente idênticos.

Veja [docs/compatibility.md](docs/compatibility.md).

---

## Agnóstico de stack, framework e linguagem

O core trabalha com conceitos semânticos:

```text
comando de build
comandos de teste
mecanismo de migration
persistência
checks de segurança
checks de performance
comportamento da CI
```

Ele não impõe um gerenciador de pacotes, framework, banco, ferramenta de migration, biblioteca de testes ou sistema operacional. As respostas concretas vêm das evidências do repositório e do contexto aprovado do projeto.

Monorepos e múltiplos serviços são analisados por componente, sem forçar uma stack global.

---

## Segurança é obrigatória

Toda issue recebe triagem de impacto de segurança.

Quando aplicável, o IssueCraft considera autenticação/autorização, isolamento, privilégios, entrada não confiável, secrets, dados sensíveis, arquivos, rede, persistência, supply chain, transições de estado, concorrência e logs.

Uma regressão material de segurança bloqueia `In Review`, salvo se um humano aceitar explicitamente **aquele risco residual específico**.

O IssueCraft não declara que algo é "100% seguro". Ele registra o que foi analisado, o que realmente foi executado e o que permaneceu sem verificação.

Veja [core/SECURITY.md](core/SECURITY.md).

---

## Performance é obrigatória

Toda issue também recebe triagem de impacto de performance.

Quando relevante, são considerados complexidade, I/O e consultas, rede, memória/recursos, concorrência/locks, cache, payloads, startup/build, responsividade, processamento em background e volume de observabilidade.

Budgets e baselines reais são respeitados quando existem. O workflow não inventa thresholds numéricos.

Um baseline confiável pode funcionar como ratchet de não regressão somente quando evidências do repositório, regras aprovadas, a issue ou uma decisão humana já o tornam normativo. Uma medição incidental nunca vira política silenciosamente.

Testes destrutivos ou de alta carga em produção/ambientes compartilhados exigem autorização explícita.

Veja [core/PERFORMANCE.md](core/PERFORMANCE.md).

---

## Testes abrangentes e baseados em risco

O IssueCraft considera todo o espaço de testes sem executar coisas irrelevantes.

Conforme a mudança, isso pode incluir unidade, componente, integração, contrato, API/interface, sistema, E2E, aceitação, smoke, regressão, erros/bordas, property-based, fuzz, mutation, concorrência/race/idempotência, resiliência/fault injection, segurança, benchmark, load, stress, spike, soak, acessibilidade, regressão visual, compatibilidade, migrations, recovery, lint, typecheck e build.

Cada check selecionado mantém um resultado explícito:

```text
pass
fail
not_applicable
unavailable
```

`not_applicable` e `unavailable` nunca significam `pass`.

Para bugs reproduzíveis, o fluxo preferido é criar/identificar um teste de regressão que falha antes da correção e passa depois, quando isso for viável. Esse RED só é válido quando o defeito/invariante alvo realmente causa a falha.

O IssueCraft também liga comportamentos materiais e critérios de aceitação a evidências reais, escolhe a camada de teste mais barata que prova o comportamento com fidelidade, avalia a qualidade das assertions em vez da quantidade de testes e verifica caminhos equivalentes/superfícies irmãs quando a mesma causa raiz pode atingi-los. Mocks/fakes precisam preservar o contrato testado; E2E caro fica para risco realmente cross-layer.

A cobertura segue **evidence-or-zero**: uma obrigação material não é considerada provada só porque uma suíte relacionada ficou verde. Requisitos compostos são decompostos em cláusulas/campos/casos falsificáveis de forma independente, requisitos vagos viram `verification precision gaps` explícitos em vez de thresholds inventados, e um check aplicável só recebe `unavailable` depois de um probe seguro ou outra evidência concreta do ambiente/capacidade. Para assertions de alto risco ou força incerta, o IssueCraft pode usar fault/mutation discrimination em estado isolado para comprovar que a verificação realmente detecta o comportamento errado; isso é proporcional ao risco, não obrigatório em toda issue.

Veja [core/TEST_STRATEGY.md](core/TEST_STRATEGY.md).

---

## Validação manual antes do Done

Após a validação automatizada, o IssueCraft gera:

```text
.implement-issue/MANUAL_VALIDATION_PLAN.md
```

O roteiro é derivado da issue, critérios de aceitação, diff real, código afetado, regras do projeto e resultados automatizados. Ele deve trazer pré-requisitos, ações e resultados esperados, além de verificações de regressão, segurança, performance, acessibilidade, compatibilidade, migrations e cleanup quando relevantes.

Não pode ser um checklist genérico do tipo "verifique se funciona".

---

## Detecção de drift

O Profile aprovado não é considerado verdade eterna.

Nas execuções futuras, o IssueCraft faz um preflight barato em evidências que podem mudar a forma de implementar ou validar: manifests, lockfiles, runtimes, frameworks, testes/build, políticas/ferramentas de segurança, budgets/baselines/ferramentas de performance, observabilidade, persistência/migrations, CI e fronteiras arquiteturais.

Mudanças materiais geram uma proposta de drift. O Profile nunca é reescrito silenciosamente.

Veja [core/DRIFT_DETECTION.md](core/DRIFT_DETECTION.md).

---

## Aprendizado controlado ao longo do tempo

O IssueCraft pode aprender com uso real sem virar um sistema que altera suas próprias regras escondido.

Ao final de uma issue ele pode detectar uma lacuna recorrente, edge case perdido, convenção do projeto, falha de validação, escape de segurança/performance ou limitação de adapter.

O processo separa:

```text
observar
  ↓
rascunhar proposta
  ↓
aprovação humana para persistir
  ↓
.implement-issue/proposals/WIP-*.md
  ↓
registro aprovado opcional
  ↓
.implement-issue/LEARNINGS.md
  ↓
nova aprovação humana para adotar comportamento
```

Uma proposta persistida ou entrada em `LEARNINGS.md` **não vira regra automaticamente**. A adoção em `PROJECT_RULES`, Profile/Blueprint, adapter ou core canônico exige a decisão humana apropriada.

Recorrência em issues/features independentes pode fortalecer a evidência de uma proposta, mas nunca promove automaticamente um aprendizado para comportamento persistente ou normativo.

Isso evita que particularidades de um projeto contaminem o workflow genérico.

Mudanças genéricas no próprio IssueCraft também passam por um filtro anti-bloat: lacuna/evidência concreta, verificação de sobreposição, preferência por fundir com regra existente, generalidade real, custo contínuo de contexto/complexidade e prova de regressão. Popularidade ou novidade não são motivo suficiente.

As regras canônicas também devem descrever procedimentos de engenharia portáveis, e não workarounds para uma peculiaridade de um agente/runtime específico; comportamentos específicos ficam em compatibilidade/adapters/evals até existir uma necessidade genérica comprovada.

Veja [core/CONTINUOUS_IMPROVEMENT.md](core/CONTINUOUS_IMPROVEMENT.md).

---

## O que é instalado no projeto

```text
seu-projeto/
├── .agents/skills/implement-issue/SKILL.md
├── .claude/skills/implement-issue/SKILL.md
└── .implement-issue/
    └── system/
        ├── core/
        ├── schemas/
        ├── templates/
        ├── manifest.json
        └── VERSION
```

O IssueCraft **não** cria antecipadamente `PROJECT_PROFILE`, `PROJECT_BLUEPRINT`, `PROJECT_RULES.md`, `LEARNINGS.md`, propostas persistentes ou `HANDOFF.md`. Conhecimento persistente segue os human gates; `HANDOFF.md` só é criado quando trabalho incompleto realmente precisa de estado para retomada.

---

## Atualizando o IssueCraft em um projeto

Atualize este repositório e reinstale somente o runtime:

```bash
git pull
python scripts/install.py /caminho/do/seu/projeto --overwrite-system
```

`--overwrite-system` substitui runtime/adapters e preserva o estado do projeto em `.implement-issue/`.

---

## Instalação sem Python

Python é apenas uma conveniência para copiar os arquivos. A instalação manual está documentada em [docs/install.md](docs/install.md).

---

## Validando este repositório

Rode as mesmas camadas determinísticas usadas pela CI:

```bash
python scripts/validate_repo.py
python scripts/run_evals.py
python scripts/run_live_evals.py validate
python -m unittest discover tests -v
```

A CI executa isso em Linux, macOS e Windows.

Os 46 cenários de `evals/scenarios/` possuem assertions de contrato executáveis e agnósticas de fornecedor. Evals com agentes reais podem ser feitos em repositórios sandbox, mas o core não depende de uma API de IA específica.

---

## Estrutura do repositório

```text
issuecraft-workflow/
├── core/                 # comportamento canônico e agnóstico
├── schemas/              # contratos de Profile e Blueprint
├── templates/            # templates de estado/artefatos
├── docs/                 # instalação, arquitetura e exemplos
├── evals/                # cenários comportamentais
├── tests/                # testes de invariantes
├── scripts/              # instalador, validator, eval runner e release
├── .agents/skills/       # entrada Codex/Antigravity
├── .claude/skills/       # entrada Claude Code
├── manifest.json
├── VERSION
└── README.md
```

O contrato normativo de execução é [core/WORKFLOW.md](core/WORKFLOW.md).

---

## Problemas comuns

### O agente não encontrou `implement-issue`

Confirme que o workflow foi instalado no mesmo repositório/workspace aberto pelo agente e que o ponto de entrada correspondente existe:

```text
.agents/skills/implement-issue/SKILL.md
.claude/skills/implement-issue/SKILL.md
```

Recarregue o workspace se o agente mantiver cache das skills.

### O runtime já está instalado

Use:

```bash
python scripts/install.py /caminho/do/seu/projeto --overwrite-system
```

O estado próprio do projeto é preservado.

### O discovery encontrou algo errado

Não aprove o Profile/Blueprint como está. Corrija o fato, forneça evidência se necessário e deixe o IssueCraft reconciliar a proposta antes de persistir.

### Um teste não pode ser executado

O IssueCraft deve fazer um probe seguro do check ou do pré-requisito/capacidade quando isso for razoável, então marcar `unavailable` com evidência e usar a alternativa segura mais forte. Ele não pode inventar um `pass` nem executar ação destrutiva/high-load só para provar indisponibilidade.

---

## Contribuindo

Leia [CONTRIBUTING.md](CONTRIBUTING.md). Mudanças genéricas de comportamento devem trazer cenário concreto e cobertura determinística de regressão/eval.

Problemas de segurança devem seguir [SECURITY.md](SECURITY.md).

## Licença

MIT — veja [LICENSE](LICENSE).
