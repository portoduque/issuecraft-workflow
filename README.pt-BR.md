# IssueCraft Workflow

[![CI](https://github.com/portoduque/issuecraft-workflow/actions/workflows/ci.yml/badge.svg)](https://github.com/portoduque/issuecraft-workflow/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Workflow agnóstico de agente de IA e de stack para implementar issues desde a descoberta do projeto até a validação humana.

**Versão:** 0.15.0  
**Licença:** MIT  
**Idioma:** [English](README.md) · [Português (Brasil)](README.pt-BR.md)

## Comece em 3 passos

Você precisa de **Git**, **Python 3** para a instalação e um agente de programação compatível.

### 1. Clone

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

### 3. Rode `implement-issue`

| Agente | Comando |
|---|---|
| Codex | `$implement-issue` |
| Claude Code | `/implement-issue` |
| Antigravity | `/implement-issue` |

Exemplo:

```text
/implement-issue
Implemente a issue #42: adicionar botão para mostrar/ocultar a senha.
```

No Codex, use `$implement-issue`.

Isso já é suficiente para começar. Na primeira execução, o IssueCraft entende como o repositório realmente funciona antes de alterar o código da aplicação.

## O que acontece na primeira execução

Em um projeto existente, o IssueCraft descobre por evidência as linguagens, runtimes, frameworks, dependências, persistência/migrations, comandos de teste, política de coverage, lint/type/build, CI, segurança, performance e arquitetura.

Ele propõe um `PROJECT_PROFILE` e pede aprovação antes de persistir.

Em um projeto vazio ou quase vazio, faz uma entrevista adaptativa curta e propõe um `PROJECT_BLUEPRINT` em vez de inventar uma stack.

Nas execuções futuras, detecta drift material e só atualiza conhecimento persistente pelo human gate aplicável.

## Fluxo de uma issue

```text
issue
  ↓
descobrir/reconciliar contexto do projeto
  ↓
planejar por evidência
  ↓
implementar a menor mudança coerente
  ↓
triagem de segurança + performance
  ↓
validação automatizada aplicável
  ↓
In Review
  ↓
MANUAL_VALIDATION_PLAN.md
  ↓
validação humana
  ↓
PASS → Done
FAIL → volta para implementação
PARTIAL / NOT RUN → permanece In Review
```

O agente não pode marcar a issue como `Done` apenas porque os testes automatizados passaram ou porque a própria IA testou a interface.

## Testes e cobertura de código

O IssueCraft considera todo o espaço semântico de testes e executa/adiciona os tipos aplicáveis ao comportamento alterado e à infraestrutura disponível no projeto.

Isso pode incluir unitário, componente, integração, contrato, API, sistema, end-to-end, aceitação, smoke, regressão, negativo/borda, property-based, fuzz, mutation, concorrência, resiliência, segurança, benchmark/load/stress/soak, acessibilidade, compatibilidade, migration/recovery, lint, type/static analysis e build/package.

Para comportamento materialmente alterado, a evidência precisa apontar um check/assertion significativo; uma suíte ampla verde ou um percentual alto de coverage, sozinhos, não provam correção.

Coverage também é guardrail de qualidade:

- descobrir ferramenta/comando/política de coverage existente;
- preservar thresholds/baselines já estabelecidos;
- não reduzir/burlar coverage apenas para fazer uma mudança passar;
- cobrir diretamente código/comportamento executável novo ou alterado quando viável;
- se o projeto não tiver tooling de coverage, não instalar silenciosamente nem inventar um percentual universal.

As regras completas ficam em [core/TEST_STRATEGY.md](core/TEST_STRATEGY.md) e [docs/testing.md](docs/testing.md).

Segurança e performance continuam sendo análises obrigatórias de impacto; veja [core/SECURITY.md](core/SECURITY.md) e [core/PERFORMANCE.md](core/PERFORMANCE.md).

## Validação manual antes do Done

Depois da validação automatizada, o IssueCraft gera:

```text
.implement-issue/issues/<issue-key>/MANUAL_VALIDATION_PLAN.md
```

O IssueCraft resolve `<issue-key>` a partir da issue/referência atual e informa o caminho exato do artefato no handoff.

O passo final humano é:

1. Abra o `.implement-issue/issues/<issue-key>/MANUAL_VALIDATION_PLAN.md` informado.
2. Confirme os pré-requisitos/setup listados.
3. Execute cada cenário numerado na ordem.
4. Compare cada ação com o resultado esperado.
5. Execute os checks de regressão/segurança/performance/acessibilidade/compatibilidade/migration/recovery quando aplicáveis.
6. Registre um resultado: **PASS**, **FAIL** ou **PARTIAL / NOT RUN**.
7. Se **FAIL**, informe etapa que falhou, esperado e observado; o IssueCraft volta para implementação e revalida.
8. Somente um **PASS** humano explícito (ou aprovação claramente equivalente) permite sair de `In Review` para `Done`.

Veja [docs/validation.md](docs/validation.md) para o modelo completo.

## Agnóstico de agente de IA

Existe um único workflow canônico:

```text
core/WORKFLOW.md
```

Os arquivos específicos dos agentes são adapters finos:

```text
.agents/skills/implement-issue/SKILL.md   # Codex + Antigravity
.claude/skills/implement-issue/SKILL.md  # Claude Code
```

Comportamento específico de provedor não pode vazar para `core/`. Veja [docs/compatibility.md](docs/compatibility.md).

## Agnóstico de stack/linguagem

O IssueCraft descobre o projeto-alvo em vez de assumir Python, JavaScript, Java, banco, framework ou test runner.

Comandos e ferramentas vêm de evidência do repositório e contexto aprovado. Monorepos e repositórios multisserviço são tratados por componente quando necessário.

## Trabalho paralelo

Vários agentes/issues podem trabalhar em paralelo, mas execuções que alteram código devem preferir workspaces/checkouts físicos isolados quando o ambiente suportar.

O IssueCraft **não** cria servidor de locks, scheduler, heartbeat, registro de agentes, worktree automático, rebase automático ou merge automático. Ele separa artefatos por issue, relê estado compartilhado antes de writes concorrentes aprovados, trata overlap como risco em vez de dependência automática e invalida seletivamente evidências quando a base de integração muda.

Veja [docs/parallel-work.md](docs/parallel-work.md).

## Aprendizado controlado

O IssueCraft aprende com uso real sem reescrever silenciosamente suas próprias regras.

```text
observar evidência
  ↓
rascunhar proposta
  ↓
aprovação humana para persistir
  ↓
.implement-issue/proposals/WIP-*.md
  ↓
registro opcional em LEARNINGS.md
  ↓
nova aprovação humana para adotar
```

Uma proposta ou entrada em `LEARNINGS.md` é memória histórica, não comportamento normativo automático.

Veja [docs/learning.md](docs/learning.md) e [core/CONTINUOUS_IMPROVEMENT.md](core/CONTINUOUS_IMPROVEMENT.md).

## O que é instalado

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

Conhecimento compartilhado como `PROJECT_PROFILE.yaml`, `PROJECT_BLUEPRINT.yaml`, `PROJECT_RULES.md`, `LEARNINGS.md` e propostas continua no nível do projeto. Handoff, validação manual e relatório de execução ficam por issue em `.implement-issue/issues/<issue-key>/`.

## Atualizando o IssueCraft

```bash
git pull
python scripts/install.py /caminho/do/seu/projeto --overwrite-system
```

`--overwrite-system` substitui apenas runtime/adapters e preserva o estado do projeto.

Instalação manual sem Python: [docs/install.md](docs/install.md).

## Validando este repositório

Execute as camadas determinísticas:

```bash
python scripts/validate_repo.py
python scripts/run_evals.py
python scripts/run_live_evals.py validate
python -m unittest discover tests -v
```

Para o gate de cobertura branch-aware do próprio IssueCraft:

```bash
python -m pip install -r requirements-dev.txt
python -m coverage erase
python -m coverage run --branch --source=scripts -m unittest discover tests -v
python -m coverage run --append --branch --source=scripts scripts/validate_repo.py
python -m coverage run --append --branch --source=scripts scripts/run_evals.py
python -m coverage run --append --branch --source=scripts scripts/run_live_evals.py validate
python -m coverage report --show-missing --fail-under=90
```

A CI roda a suíte principal em Linux, macOS e Windows e aplica o gate de coverage separadamente.

## Documentação

- [Instalação](docs/install.md)
- [Arquitetura](docs/architecture.md)
- [Compatibilidade dos agentes](docs/compatibility.md)
- [Smoke de compatibilidade para releases](docs/compatibility-release.md)
- [Testes e coverage](docs/testing.md)
- [Validação manual e gate de Done](docs/validation.md)
- [Segurança para trabalho paralelo](docs/parallel-work.md)
- [Aprendizado controlado](docs/learning.md)
- [Arquivos do runtime do projeto](docs/project-files.md)

## Problemas comuns

Se o agente não encontrar `implement-issue`, confirme se o adapter existe no projeto-alvo e recarregue o workspace quando a descoberta de skills do agente exigir isso.

Se o runtime já existir, atualize com `--overwrite-system`.

Se um fato descoberto estiver errado, corrija a proposta antes de aprovar. O IssueCraft deve preservar evidências/conflitos, não inventar fatos.

Se um teste aplicável não puder rodar, ele fica `unavailable`; isso nunca vira `pass`.

## Contribuindo

Leia [CONTRIBUTING.md](CONTRIBUTING.md). Mudanças genéricas devem incluir evidência de regressão/eval e preservar neutralidade de agente/stack.

## Licença

MIT. Veja [LICENSE](LICENSE).
