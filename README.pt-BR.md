# Implement Issue Workflow

Workflow reutilizável e agnóstico de IA, stack, framework e linguagem para implementar issues com discovery, planejamento, segurança, performance, testes, revisão e aprovação humana.

**Versão:** 0.2.1  
**Licença:** MIT  
**Idioma:** [English](README.md) · [Português (Brasil)](README.pt-BR.md)

---

## Comece em 3 passos

Você precisa apenas de **Git**, **Python 3** para o instalador e um agente de programação compatível.

### 1. Clone este repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd implement-issue-workflow
```

Substitua `<URL_DO_REPOSITORIO>` pela URL de clone deste projeto no GitHub.

### 2. Instale o workflow no seu projeto

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

O instalador **não muda a stack da sua aplicação** e **não toma decisões de arquitetura por você**. Ele apenas instala o runtime do workflow e os pontos de entrada dos agentes.

### 3. Abra seu projeto no agente e rode o workflow

| Agente | Comando |
|---|---|
| Codex | `$implement-issue` |
| Claude Code | `/implement-issue` |
| Antigravity | `/implement-issue` |

Depois informe a issue, bug, tarefa ou feature que deseja implementar.

Exemplo:

```text
/implement-issue
Implemente a issue #42: adicionar botão para mostrar/ocultar a senha no formulário de usuário.
```

No Codex, use `$implement-issue` no lugar de `/implement-issue`.

**Pronto. Isso já é suficiente para começar.** Na primeira execução, o workflow entende como seu projeto funciona antes de alterar código.

---

## O que acontece na primeira execução?

O workflow primeiro inspeciona o repositório. Ele não presume que você usa uma tecnologia específica.

```text
primeira execução
       ↓
inspecionar repositório
       ↓
┌─────────────────────────┬──────────────────────────┐
│ projeto já existente    │ projeto novo/vazio       │
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

O workflow procura evidências de:

- linguagens e runtimes;
- frameworks e bibliotecas estruturais;
- gerenciadores de pacotes/dependências;
- banco e persistência;
- migrations;
- ferramentas e comandos de teste;
- lint, format e typecheck;
- build e execução;
- CI/CD;
- ferramentas e políticas de segurança;
- benchmarks, budgets e ferramentas de performance;
- arquitetura e convenções relevantes do repositório.

A partir dessas evidências, ele propõe um `PROJECT_PROFILE.yaml`.

Se não conseguir descobrir alguma coisa, o valor continua como `unknown` ou `not_detected`. O workflow não deve inventar o que não conseguiu comprovar.

### Projeto novo ou vazio

Se ainda não existir implementação suficiente para descobrir a stack, o workflow entra em **Project Bootstrap**.

Ele:

1. lê a documentação que já existir;
2. reaproveita decisões já documentadas;
3. faz uma rodada curta e adaptativa de perguntas somente sobre o que continua indefinido;
4. mantém decisões não tomadas como `undecided`;
5. propõe um `PROJECT_BLUEPRINT.yaml`;
6. pede aprovação humana antes de salvar.

A separação é intencional:

- **Blueprint** = o que pretendemos construir.
- **Profile** = o que o repositório comprova que existe hoje.

---

## Fluxo normal de uma issue

Depois do onboarding, toda issue segue o mesmo ciclo principal:

```text
issue/tarefa
    ↓
entender contexto
    ↓
In Progress
    ↓
planejar
    ↓
implementar
    ↓
revisar segurança
    ↓
revisar performance
    ↓
validação automatizada baseada em risco
    ↓
gerar roteiro manual de validação
    ↓
In Review
    ↓
validação humana
    ├── falhou → In Progress
    └── passou → Done
```

O workflow pode levar a issue até **In Review**, mas **Done pertence ao humano**. A IA não deve marcar uma issue como concluída apenas porque acredita que a própria implementação está correta.

---

## Por que ele é stack agnóstico?

O core canônico não possui comandos específicos de uma tecnologia, como:

```text
npm test
pytest
mvn test
docker compose up
```

Em vez disso, ele descobre os comandos realmente utilizados pelo repositório e registra esse conhecimento no contexto do projeto.

O core trabalha com conceitos abstratos, por exemplo:

```text
comando de build
comando de teste unitário
comando de integração
comando de lint
mecanismo de migration
banco utilizado
comportamento da CI
```

Quem fornece as respostas concretas é o próprio projeto, por meio de evidências.

Por isso o mesmo workflow pode ser usado em aplicação web, API, CLI, biblioteca, mobile, monorepo, serviço ou outro tipo de projeto sem exigir uma linguagem ou framework específico.

---

## Por que ele é agnóstico de IA?

Existe apenas **um workflow canônico**:

```text
core/WORKFLOW.md
```

Os arquivos específicos de cada agente são apenas pontos de entrada finos que encaminham para esse mesmo core.

```text
Codex ─────────┐
Claude Code ───┼──→ core canônico
Antigravity ───┘
```

O próprio repositório possui testes que impedem que regras específicas de um fornecedor de IA vazem para `core/`.

Pontos de entrada atuais:

```text
.agents/skills/implement-issue/SKILL.md
.claude/skills/implement-issue/SKILL.md
```

Mais detalhes em [`docs/compatibility.md`](docs/compatibility.md).

---

## Segurança é obrigatória

Toda issue passa por uma triagem de impacto de segurança, mesmo quando inicialmente parece não ter relação com segurança.

O workflow considera, conforme aplicável:

- autenticação e autorização;
- permissões e privilégios;
- secrets e credenciais;
- dados sensíveis;
- validação de entradas;
- riscos de injeção;
- manipulação de arquivos;
- limites de rede;
- persistência e integridade dos dados;
- dependências e supply chain;
- concorrência e consistência de estado;
- logs e vazamento acidental de informações.

A profundidade da validação é proporcional ao risco da mudança. Uma regressão material de segurança bloqueia a revisão, salvo quando um humano aceita explicitamente aquele risco específico.

Veja [`core/SECURITY.md`](core/SECURITY.md).

---

## Performance é obrigatória

Toda issue também passa por uma triagem de impacto de performance.

Quando relevante, o workflow analisa:

- complexidade algorítmica;
- queries e I/O;
- chamadas de rede;
- uso de memória;
- uso de CPU;
- concorrência e locks;
- cache;
- tamanho de payloads;
- custo de startup/build;
- vazamento de recursos;
- budgets e baselines já existentes.

Ele utiliza baselines reais do projeto quando disponíveis e não inventa limites de performance.

Testes caros ou destrutivos de carga/stress não devem ser executados em produção sem autorização explícita.

Veja [`core/PERFORMANCE.md`](core/PERFORMANCE.md).

---

## Estratégia de testes

O workflow **não executa todos os tipos de teste cegamente**. Ele considera o espaço completo de validação e seleciona o que faz sentido para os riscos introduzidos pela issue.

Dependendo do projeto e da mudança, podem ser considerados:

- testes unitários;
- testes de componente;
- integração;
- contrato;
- API;
- sistema;
- end-to-end (E2E);
- aceitação;
- smoke e sanity;
- regressão;
- casos negativos e de borda;
- property-based;
- fuzz;
- mutation;
- concorrência, race, locking e idempotência;
- resiliência e fault injection;
- segurança;
- benchmarks;
- load, stress, spike e soak;
- acessibilidade;
- regressão visual;
- compatibilidade;
- instalação, upgrade, downgrade e rollback;
- migrations e integridade dos dados;
- backup, restore e recovery;
- análise estática, lint, typecheck e build.

O resultado de cada categoria precisa permanecer explícito:

```text
pass
fail
not_applicable
unavailable
```

`not_applicable` e `unavailable` nunca significam `pass`.

Em correções de bugs reproduzíveis, o fluxo preferido é criar ou identificar um teste de regressão que falhe antes da correção e passe depois, sempre que isso for viável.

Veja [`core/TEST_STRATEGY.md`](core/TEST_STRATEGY.md).

---

## Validação manual antes do Done

Depois da implementação e da validação automatizada, o workflow gera um roteiro manual específico para a issue.

Quando aplicável, ele deve conter:

- pré-requisitos;
- dados de teste;
- ações exatas;
- resultados esperados;
- edge cases;
- regressões;
- verificações sensíveis de segurança;
- verificações sensíveis de performance;
- passos de limpeza.

Não vale um checklist genérico do tipo “verifique se funciona”.

Depois disso, a issue entra em **In Review**. Um humano executa a validação e decide se ela pode ir para **Done**.

---

## Detecção de drift

O projeto pode mudar com o tempo. Por isso o workflow não presume que o Profile original continuará correto para sempre.

Nas execuções seguintes, ele faz uma checagem leve das evidências importantes.

Exemplo:

```text
PROJECT_PROFILE informa:
gerenciador de pacotes = A

repositório agora mostra:
lockfile de B
manifest declara B
lockfile antigo foi removido

→ possível drift detectado
→ proposta de atualização do Profile
→ aprovação humana obrigatória
```

O workflow nunca reescreve silenciosamente um conhecimento de projeto já aprovado.

Veja [`core/DRIFT_DETECTION.md`](core/DRIFT_DETECTION.md).

---

## Melhoria contínua sem autoalteração silenciosa

O workflow pode aprender com o uso, mas não modifica a si mesmo de forma silenciosa.

Quando identifica uma melhoria reutilizável, ele pode gerar uma proposta estruturada contendo:

- problema encontrado;
- evidências;
- comportamento atual;
- comportamento proposto;
- classificação como aprendizado genérico ou específico do projeto;
- benefício esperado;
- riscos e trade-offs;
- sugestão de teste/eval de regressão.

Somente depois de aprovação humana uma regra persistente do workflow ou do projeto deve ser alterada.

Isso impede que as convenções de um único projeto contaminem o workflow genérico.

Veja [`core/CONTINUOUS_IMPROVEMENT.md`](core/CONTINUOUS_IMPROVEMENT.md).

---

## O que o instalador adiciona ao projeto?

Ao executar:

```bash
python scripts/install.py /caminho/do/seu/projeto
```

o projeto passa a ter:

```text
seu-projeto/
├── .agents/
│   └── skills/
│       └── implement-issue/
│           └── SKILL.md
├── .claude/
│   └── skills/
│       └── implement-issue/
│           └── SKILL.md
└── .implement-issue/
    └── system/
        ├── core/
        ├── schemas/
        ├── templates/
        ├── manifest.json
        └── VERSION
```

Ele **não cria antecipadamente**:

```text
PROJECT_PROFILE.yaml
PROJECT_BLUEPRINT.yaml
PROJECT_RULES.md
```

Esses arquivos representam estado pertencente ao projeto e dependem do processo de evidências/decisões e de aprovação humana.

Seu projeto alvo não vira um projeto Python. Python é usado apenas pelo instalador deste repositório para copiar os arquivos.

---

## Como atualizar uma instalação existente

Baixe ou faça pull de uma versão mais nova deste workflow e rode:

```bash
python scripts/install.py /caminho/do/seu/projeto --overwrite-system
```

Esse comando substitui o runtime e os adapters do workflow, mas preserva estado pertencente ao projeto, como Profile, Blueprint, Rules, artefatos de validação e propostas de melhoria.

---

## Instalação sem Python

Python é apenas uma conveniência para copiar os arquivos. Também é possível instalar manualmente.

Copie:

```text
core/      → <projeto>/.implement-issue/system/core/
schemas/   → <projeto>/.implement-issue/system/schemas/
templates/ → <projeto>/.implement-issue/system/templates/
VERSION    → <projeto>/.implement-issue/system/VERSION
manifest.json → <projeto>/.implement-issue/system/manifest.json

.agents/skills/implement-issue/
    → <projeto>/.agents/skills/implement-issue/

.claude/skills/implement-issue/
    → <projeto>/.claude/skills/implement-issue/
```

Não crie Profile ou Blueprint manualmente a partir dos templates apenas para pular o onboarding.

---

## Estrutura deste repositório

```text
implement-issue-workflow/
├── core/                 # comportamento canônico agnóstico
├── schemas/              # contratos de Profile e Blueprint
├── templates/            # templates de artefatos gerados
├── docs/                 # documentação e exemplos
├── evals/                # cenários de regressão comportamental
├── tests/                # testes e invariantes do repositório
├── scripts/              # instalador, validator e release tooling
├── .agents/skills/       # entrada do Codex/Antigravity
├── .claude/skills/       # entrada do Claude Code
├── manifest.json
├── VERSION
└── README.md
```

O arquivo mais importante é [`core/WORKFLOW.md`](core/WORKFLOW.md). Ele é o contrato canônico de execução.

---

## Como validar este repositório

Antes de publicar ou alterar o workflow, rode:

```bash
python scripts/validate_repo.py
python -m unittest discover tests -v
```

Esses testes verificam contratos estruturais como neutralidade de IA, neutralidade de stack, segurança, performance, estratégia de testes, adapters, segurança do instalador, schemas e cobertura dos cenários de regressão.

---

## Problemas comuns

### O agente não encontrou `implement-issue`

1. Confirme que você instalou o workflow no mesmo repositório/workspace aberto pelo agente.
2. Confirme que pelo menos o arquivo correspondente ao seu agente existe:

```text
.agents/skills/implement-issue/SKILL.md
.claude/skills/implement-issue/SKILL.md
```

3. Feche e abra novamente o agente caso ele faça cache das skills do projeto.
4. Use o comando explícito da tabela de compatibilidade no início deste README.

### O instalador informa que o workflow já existe

Use o modo de atualização:

```bash
python scripts/install.py /caminho/do/seu/projeto --overwrite-system
```

### Meu projeto já possui `.agents/` ou `.claude/`

Sem problema. O instalador gerencia somente a pasta `implement-issue` dentro desses locais.

### Meu repositório está vazio

É suportado. Rode o workflow normalmente. Ele utilizará Project Bootstrap em vez de fingir que descobriu uma stack inexistente.

### Minha stack é incomum

É suportado por design. O workflow deve aprender pelos arquivos, comandos e evidências do seu repositório, e não por uma lista fixa de tecnologias conhecidas.

---

## Documentação adicional

Você só precisa destas páginas se quiser aprofundar:

- [Instalação](docs/install.md)
- [Arquitetura](docs/architecture.md)
- [Compatibilidade dos agentes](docs/compatibility.md)
- [Arquivos pertencentes ao projeto](docs/project-files.md)
- [Baseline de segurança, performance e testes](docs/security-quality-baseline.md)
- [Exemplo com projeto existente](docs/examples/existing-project.md)
- [Exemplo com projeto vazio](docs/examples/empty-project.md)
- [Exemplo de drift](docs/examples/drift.md)

---

## Como contribuir

Contribuições são bem-vindas. Alterações no core canônico devem preservar:

- neutralidade de fornecedor/agente de IA;
- neutralidade de stack, linguagem e framework;
- evidência antes de suposição;
- gates de aprovação humana;
- triagem de segurança e performance;
- validação abrangente baseada em risco;
- domínio humano sobre o estado Done.

Veja [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Licença

MIT. Veja [`LICENSE`](LICENSE).
