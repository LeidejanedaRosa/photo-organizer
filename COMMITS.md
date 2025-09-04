# Guia de Commits Semânticos - Photo Organizer

Este projeto utiliza **Conventional Commits** para manter um histórico claro e consistente das mudanças.

## 📋 Formato do Commit

```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

## 🏷️ Tipos de Commit

| Tipo | Emoji | Descrição | Exemplo |
|------|-------|-----------|---------|
| `feat` | ✨ | Nova funcionalidade | `feat(scanner): adicionar busca por data` |
| `fix` | 🐛 | Correção de bug | `fix(handler): corrigir erro ao mover arquivos` |
| `docs` | 📚 | Documentação | `docs: atualizar README com exemplos` |
| `style` | 🎨 | Formatação de código | `style: ajustar indentação` |
| `refactor` | ♻️ | Refatoração | `refactor(scanner): melhorar lógica de busca` |
| `test` | 🧪 | Testes | `test: adicionar testes para file_handler` |
| `chore` | 🔧 | Tarefas de manutenção | `chore: atualizar dependências` |
| `build` | 📦 | Sistema de build | `build: adicionar script de deploy` |
| `ci` | 🧱 | Integração contínua | `ci: configurar GitHub Actions` |
| `perf` | ⚡ | Performance | `perf: otimizar algoritmo de organização` |
| `revert` | 💥 | Reversão | `revert: desfazer mudança na estrutura` |

## 🎯 Escopos Recomendados

Para este projeto, use os seguintes escopos quando aplicável:

- `scanner` - Funcionalidades de escaneamento de diretórios
- `handler` - Manipulação de arquivos
- `main` - Arquivo principal e configuração
- `tests` - Arquivos de teste
- `docs` - Documentação
- `config` - Configurações

## 🚀 Como Usar

### Método 1: Script Auxiliar (Recomendado)
```bash
# 1. Adicione suas mudanças
git add .

# 2. Use o script auxiliar
./commit.sh
```

### Método 2: Comando Git Direto
```bash
git add .
git commit -m "feat(scanner): adicionar suporte para filtros de data"
```

### Método 3: Editor Interativo
```bash
git add .
git commit
# Isso abrirá o editor com o template configurado
```

## ✅ Exemplos Válidos

```bash
✅ feat: adicionar funcionalidade de backup
✅ feat(scanner): implementar busca recursiva
✅ fix(handler): corrigir erro ao criar diretórios
✅ docs(readme): adicionar seção de instalação
✅ test(scanner): adicionar testes unitários
✅ chore: atualizar versão do Python
✅ refactor: reorganizar estrutura de módulos
```

## ❌ Exemplos Inválidos

```bash
❌ Adicionando nova funcionalidade
❌ Bug fix
❌ WIP
❌ update
❌ fix bug
```

## 🛡️ Validação Automática

Este projeto possui um hook do Git que valida automaticamente suas mensagens de commit. Se a mensagem não seguir o padrão Conventional Commits, o commit será rejeitado com uma mensagem de erro explicativa.

## 🔧 Configuração

O projeto já está configurado com:

- ✅ Hook de validação (`.git/hooks/commit-msg`)
- ✅ Template de commit (`.gitmessage`)
- ✅ Script auxiliar (`commit.sh`)

## 📚 Referências

- [Conventional Commits](https://www.conventionalcommits.org/pt-br/)
- [Padrões de Commits do iuricode](https://github.com/iuricode/padroes-de-commits)
