# Organizador de Fotos

## 📋 Descrição

Sistema para organização automática de fotos seguindo padrão específico de nomenclatura e organização por datas/eventos.

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

**Formato:** `MM - MA 19a DDMMAAAA(XX) [- evento].extensão`

- **MM**: Mês do bebê (00-12)
- **MA 19a**: Identificador fixo (Maria Antônia 19ª)
- **DDMMAAAA**: Data da foto
- **XX**: Número sequencial do dia
- **evento**: Descrição opcional do evento

## 🗓️ Cálculo da Idade do Bebê

- **Data de nascimento**: 17/08/2024
- **Ano 1**: 17/08/2024 a 16/08/2025
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

- Remover os dados pré-estabelecidos e deixar o usuário definir, como: qual a data de início da pasta, qual a data final, qual será o padrão da nomenclatura das imagens (MA 19a DDMMAAAA)