# Organizador de Fotos

## 📋 Descrição

Sistema para organização automática de fotos com **configuração totalmente personalizável**. Permite definir datas de início/fim, nomenclatura customizada e diferentes padrões de organização.

### 🆕 Novidades da Versão 2.0
- ✅ **Configuração Personalizada**: Defina suas próprias datas, prefixos e padrões
- ✅ **Compatibilidade Total**: Mantém funcionamento com sistema anterior
- ✅ **Flexibilidade**: Adapte o sistema para qualquer projeto de fotos
- ✅ **Interface Melhorada**: Menu intuitivo com novas opções

## 🏗️ Arquitetura Refatorada

O projeto segue princípios **SOLID** e **Clean Code** com separação clara de responsabilidades:

```
src/
├── cli/                 # Interface de linha de comando
├── domain/              # Entidades e regras de negócio
│   ├── image.py         # Modelo de imagem
│   └── configuration.py # Sistema de configuração personalizável
├── services/            # Serviços de negócio
├── utils/               # Utilitários
```

## 🎯 Princípios SOLID Aplicados

- **S**ingle Responsibility: Cada classe tem uma responsabilidade específica
- **O**pen/Closed: Extensível sem modificar código existente
- **L**iskov Substitution: Subclasses substituem classes base
- **I**nterface Segregation: Interfaces específicas e coesas
- **D**ependency Inversion: Dependências abstratas, não concretas

## 🚀 Como Usar

### Executar a aplicação:
```bash
python main.py
```

### Configuração Personalizada (Novidade!):
```python
from src.domain.configuration import ConfigurationManager
from datetime import datetime

# Criar configuração personalizada
config = ConfigurationManager.create_custom_configuration(
    data_inicio=datetime(2023, 1, 1),
    data_final=datetime(2023, 12, 31),
    prefixo="VIAGEM",
    incluir_periodo=True
)

# Aplicar na aplicação
from src.services.photo_organizer_service import PhotoOrganizerService
service = PhotoOrganizerService(config)
```

## 📝 Padrões de Nomenclatura

### Sistema Flexível (Novo):
**Formato configurável:** `[PERÍODO] - [PREFIXO] [DATA](SEQUENCIAL) [- EVENTO]`

Exemplos:
- `00 - VIAGEM 01012023(00).jpg` (com período)
- `FOTO 01012023(00).jpg` (sem período)
- `IMG 15062023(01) - Aniversário.jpg` (com evento)

### Sistema Legado (Compatível):
**Formato:** `MM - IMG DDMMAAAA(XX) [- evento].extensão`

- **MM**: Mês do período (00-12)
- **IMG**: Identificador específico
- **DDMMAAAA**: Data da foto
- **XX**: Número sequencial do dia
- **evento**: Descrição opcional

## ⚙️ Configuração do Sistema

### Menu Principal (Opção 9 - Nova!):
1. **Configurar novo projeto personalizado**
   - Define data de início e fim
   - Escolhe prefixo da nomenclatura
   - Configura cálculo de períodos

2. **Usar configuração compatível**
   - Mantém sistema anterior (IMG)
   - Data base: 01/01/2025

3. **Visualizar configuração atual**
   - Mostra parâmetros ativos

### Exemplo de Configuração Interativa:
```
⚙️  CONFIGURAÇÃO PERSONALIZADA DO PROJETO
============================================================
📅 Data de início (DD/MM/AAAA): 01/01/2023
📅 Data final (DD/MM/AAAA) [opcional]: 31/12/2023  
🏷️  Prefixo da nomenclatura: VIAGEM
📊 Incluir cálculo de período/mês? (s/N): s

✅ Configuração criada com sucesso!
   📅 Período: 01/01/2023 até 31/12/2023
   🏷️  Prefixo: VIAGEM
   📊 Período: Sim
```

## 🗓️ Cálculos de Período

### Sistema Flexível:
- **Período base**: Configurável pelo usuário
- **Cálculo**: Baseado na data de início definida
- **Flexibilidade**: Qualquer data de referência

### Sistema Legado (Compatibilidade):
- **Data de nascimento**: 01/01/2025
- **Ano 1**: 01/01/2025 a 31/12/2025
- **Ano 2**: 17/08/2025 a 16/08/2026

## 🔧 Funcionalidades

1. **Análise de Imagens**: Lista e categoriza imagens
2. **Detecção de Duplicatas**: Identifica e move duplicatas
3. **Renomeação Flexível**: Aplica padrão configurável
4. **Organização por Pastas**: Organiza por períodos/eventos
5. **Relatórios Detalhados**: Estatísticas completas
6. **Busca por Período**: Localiza fotos em datas específicas
7. **Sistema de Backup**: Backup automático antes de operações
8. **Gestão de Eventos**: Adiciona eventos às fotos
9. **🆕 Configuração Personalizada**: Sistema totalmente flexível

## 🛡️ Segurança

- **Backup automático** antes de qualquer operação destrutiva
- **Modo simulação** para prévia de todas as operações
- **Validação** de datas e formatos
- **Recuperação** de dados via backups

## 🧪 Testes

```bash
# Executar testes
python -m pytest tests/

# Teste específico
python tests/test_image.py
```

## 📈 Benefícios da Refatoração v2.0

- ✅ **Flexibilidade Total**: Configure para qualquer projeto
- ✅ **Compatibilidade**: Sistema anterior funciona normalmente
- ✅ **Manutenibilidade**: Código mais fácil de manter
- ✅ **Testabilidade**: Cada componente testável independentemente
- ✅ **Extensibilidade**: Novas funcionalidades fáceis de adicionar
- ✅ **Reutilização**: Configurações salvadas e reutilizáveis
- ✅ **Separação de Responsabilidades**: Cada classe tem um propósito claro
- ✅ **Baixo Acoplamento**: Componentes independentes

## 🔄 Migração do Sistema Anterior

O novo sistema mantém **total compatibilidade** com o anterior:

1. **Automática**: Sistema detecta configuração legada
2. **Opcional**: Pode migrar para novo sistema gradualmente  
3. **Reversível**: Sempre pode voltar ao sistema anterior
4. **Dados**: Nenhuma perda de dados ou configurações

## 📋 Próximas Implementações

- ✅ ~~Configuração personalizada~~
- ✅ ~~Sistema flexível de nomenclatura~~
- 🚧 Organizar vídeos também
- 🚧 Interface gráfica (GUI)
- 🚧 Configurações salvas em arquivo
- 🚧 Templates de configuração predefinidos
- 🚧 Integração com cloud storage

## 🏗️ Arquitetura Refatorada

O código foi refatorado seguindo princípios **SOLID** e **Clean Code**, com separação clara de responsabilidades:

### 📁 Estrutura de Diretórios

```
src/
├── domain/          # Entidades e regras de negócio
│   └── image.py     # ImageInfo, BabyAge, Event
├── services/        # Lógica de negócio
│   ├── image_analyzer.py       # Análise de imagens
│   ├── duplicate_manager.py    # Gerenciamento de duplicatas
│   ├── file_renamer.py         # Renomeação de arquivos
│   ├── folder_organizer.py     # Organização em pastas
│   ├── backup_manager.py       # Criação de backups
│   ├── report_generator.py     # Geração de relatórios
│   └── photo_organizer_service.py  # Orquestrador principal
├── utils/           # Utilitários
│   └── event_manager.py        # Gerenciamento de eventos
└── cli/             # Interface de linha de comando
    ├── menu_controller.py      # Controle de menus
    └── photo_organizer_cli.py  # Interface principal
```

## 🎯 Princípios SOLID Aplicados

### Single Responsibility Principle (SRP)
- Cada classe tem uma única responsabilidade
- `ImageAnalyzer`: apenas análise de imagens
- `DuplicateManager`: apenas gerenciamento de duplicatas
- `FileRenamer`: apenas renomeação de arquivos

### Open/Closed Principle (OCP)
- Classes abertas para extensão, fechadas para modificação
- Novos tipos de organização podem ser adicionados sem alterar código existente

### Liskov Substitution Principle (LSP)
- Implementações podem ser substituídas sem quebrar o código

### Interface Segregation Principle (ISP)
- Interfaces específicas em vez de interfaces grandes
- Cada serviço expõe apenas o que é necessário

### Dependency Inversion Principle (DIP)
- Dependências são injetadas via composição
- `PhotoOrganizerService` orquestra outros serviços

## 🚀 Como Usar

### Executar a aplicação:
```bash
python main.py
```

### Executar apenas análise programática:
```python
from src.services.photo_organizer_service import PhotoOrganizerService

service = PhotoOrganizerService()
imagens_nao_org, imagens_org = service.analyze_directory("/caminho/para/fotos")
service.generate_report(imagens_nao_org + imagens_org)
```

## 📝 Padrão de Nomenclatura

**Formato:** `MM - IMG DDMMAAAA(XX) [- evento].extensão`

- **MM**: Mês do bebê (00-12)
- **IMG**: Identificador fixo (Maria Antônia 19ª)
- **DDMMAAAA**: Data da foto
- **XX**: Número sequencial do dia
- **evento**: Descrição opcional do evento

## 🗓️ Cálculo da Idade do Bebê

- **Data de nascimento**: 01/01/2025
- **Ano 1**: 01/01/2025 a 31/12/2025
- **Ano 2**: 17/08/2025 a 16/08/2026
- E assim por diante...

## 🔧 Funcionalidades

1. **Análise de Imagens**: Lista e categoriza imagens
2. **Detecção de Duplicatas**: Identifica e move duplicatas
3. **Renomeação Automática**: Aplica padrão de nomenclatura
4. **Organização por Pastas**: Organiza por anos/eventos
5. **Relatórios Detalhados**: Estatísticas completas
6. **Busca por Período**: Localiza fotos em datas específicas
7. **Sistema de Backup**: Backup automático antes de operações
8. **Gestão de Eventos**: Adiciona eventos às fotos

## 🛡️ Segurança

- Backup automático antes de operações destrutivas
- Simulação antes de executar alterações
- Confirmação do usuário para todas as operações

## 🧪 Testes

Os testes existentes em `tests/` continuam funcionando com a nova arquitetura.

## 📈 Benefícios da Refatoração

- ✅ **Manutenibilidade**: Código mais fácil de manter e modificar
- ✅ **Testabilidade**: Cada componente pode ser testado independentemente  
- ✅ **Extensibilidade**: Novas funcionalidades são fáceis de adicionar
- ✅ **Reutilização**: Serviços podem ser reutilizados em outros contextos
- ✅ **Separação de Responsabilidades**: Cada classe tem um propósito claro
- ✅ **Baixo Acoplamento**: Componentes são independentes entre si


Implementar:

- Não faz sentindo implementar o incremento no nome do arquivo no momento de renomear e organizar.

- Tirar o endereço fixo e solicitar ao usuário a localização da pasta para ser organizada

- Organizar vídeos também

- Remover os dados pré-estabelecidos e deixar o usuário definir, como: qual a data de início da pasta, qual a data final, qual será o padrão da nomenclatura das imagens (IMG DDMMAAAA)