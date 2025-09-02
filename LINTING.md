# Configuração de Linting e Formatação

Este projeto possui uma configuração rigorosa de linting e formatação de código para garantir qualidade e consistência.

## Ferramentas Utilizadas

### 1. **Black** - Formatação de código
- Formata automaticamente o código Python
- Configurado para linha máxima de 79 caracteres

### 2. **isort** - Organização de imports
- Organiza automaticamente as importações
- Configurado para ser compatível com Black

### 3. **flake8** - Linting básico
- Verifica erros de sintaxe e estilo
- Detecta importações não utilizadas (F401)
- Detecta variáveis não utilizadas (F841)

### 4. **pylint** - Análise avançada
- Detecta argumentos não utilizados
- Detecta variáveis e importações não utilizadas
- Análise mais rigorosa de qualidade de código

### 5. **autoflake** - Limpeza automática
- Remove automaticamente importações não utilizadas
- Remove variáveis não utilizadas

### 6. **vulture** - Código morto
- Detecta código não utilizado
- Classes, métodos e variáveis não referenciadas

### 7. **mypy** - Verificação de tipos
- Verificação estática de tipos
- Garante consistência de tipagem

## Como Usar

### Executar todas as verificações:
```bash
./scripts/format-and-lint.sh
```

### Executar ferramentas individuais:

```bash
# Formatação
.venv/bin/python -m black --line-length=79 .
.venv/bin/python -m isort --profile=black --line-length=79 .

# Limpeza
.venv/bin/python -m autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive src/

# Verificações
.venv/bin/python -m flake8 src/
.venv/bin/python -m pylint src/ --disable=all --enable=unused-import,unused-variable,unused-argument --reports=no
.venv/bin/python -m vulture src/ --min-confidence 80
.venv/bin/python -m mypy src/
```

### Configurar pre-commit (opcional):
```bash
.venv/bin/python -m pip install pre-commit
.venv/bin/python -m pre_commit install
```

## Arquivos de Configuração

- `.flake8` - Configuração do flake8
- `pyproject.toml` - Configuração do Black, isort, pylint e mypy
- `.pre-commit-config.yaml` - Configuração do pre-commit hooks

## Problemas Comuns

### Importações não utilizadas
- **Detecção**: flake8 (F401), pylint, autoflake
- **Correção**: Remover as importações ou usar autoflake

### Variáveis não utilizadas
- **Detecção**: flake8 (F841), pylint, autoflake
- **Correção**: Remover as variáveis ou usar autoflake

### Argumentos não utilizados
- **Detecção**: pylint (unused-argument)
- **Correção**: Usar o argumento no código ou prefixar com `_`

### Código não utilizado
- **Detecção**: vulture
- **Correção**: Remover o código ou documentar por que deve ser mantido

## Status Atual

✅ **Configuração funcionando corretamente!**

As ferramentas estão configuradas e detectando:
- Importações não utilizadas
- Variáveis não utilizadas
- Argumentos não utilizados
- Código morto
- Problemas de tipagem
- Problemas de formatação

O problema anterior era que a configuração `.flake8` estava ignorando globalmente os erros F401 (importações não utilizadas). Isso foi corrigido e agora todas as verificações estão funcionando adequadamente.
