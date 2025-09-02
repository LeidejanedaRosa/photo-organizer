# 📸 Organizador de Fotos

Um organizador inteligente de fotos em Python que automatiza a organização, renomeação e gerenciamento de arquivos de imagem com base em metadados EXIF.

## ✨ Funcionalidades

- 🗂️ **Organização Automática**: Organiza fotos por ano/mês com base na data da foto
- 🏷️ **Renomeação Inteligente**: Renomeia arquivos com padrões personalizáveis
- 🔍 **Detecção de Duplicatas**: Identifica e gerencia fotos duplicadas
- 💾 **Backup Automático**: Cria backups antes de realizar operações
- 📊 **Relatórios Detalhados**: Gera relatórios sobre o processo de organização
- 🎯 **Análise EXIF**: Extrai informações dos metadados das imagens
- ⚙️ **Configuração Flexível**: Múltiplas opções de personalização
- 🖥️ **Interface CLI**: Interface de linha de comando intuitiva

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório**
   ```bash
   git clone https://github.com/LeidejanedaRosa/photo-organizer.git
   cd photo-organizer
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

## 📋 Como Usar

### Uso Básico

Execute o organizador de fotos:

```bash
python main.py
```

### Fluxo de Uso

1. **Selecione o diretório** com suas fotos
2. **Escolha uma opção** do menu inteligente:
   - Organizar fotos por data
   - Renomear arquivos
   - Detectar duplicatas
   - Gerar relatórios
   - Configurar parâmetros

3. **Acompanhe o progresso** das operações
4. **Revise os resultados** e relatórios gerados

### Exemplo de Estrutura Gerada

```
fotos/
├── 2023/
│   ├── 01-Janeiro/
│   │   ├── 20230115_142530_IMG001.jpg
│   │   └── 20230120_091045_IMG002.jpg
│   └── 02-Fevereiro/
│       └── 20230205_163220_IMG003.jpg
└── 2024/
    ├── 03-Março/
    └── backup/
        └── backup_20241201_143022/
```

## ⚙️ Configurações

O organizador oferece diversas opções de configuração:

- **Padrões de nomeação**: Customize como os arquivos são renomeados
- **Estrutura de pastas**: Defina como as pastas são organizadas
- **Formatos suportados**: JPG, PNG, TIFF, BMP e outros
- **Backup automático**: Configure políticas de backup
- **Filtros de data**: Organize por períodos específicos

## 🏗️ Arquitetura

O projeto segue princípios SOLID e Clean Code:

```
src/
├── cli/          # Interface de linha de comando
├── domain/       # Entidades e regras de negócio
├── services/     # Serviços de aplicação
└── utils/        # Utilitários e helpers
```

### Principais Componentes

- **PhotoOrganizerService**: Orquestrador principal
- **ImageAnalyzer**: Análise de metadados EXIF
- **FolderOrganizer**: Organização de estrutura de pastas
- **DuplicateManager**: Detecção de duplicatas
- **BackupManager**: Gerenciamento de backups
- **ReportGenerator**: Geração de relatórios

## 🛠️ Desenvolvimento

### Configuração do Ambiente

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Configurar hooks de pre-commit
make setup-dev

# Formatar código
make format

# Executar linting
make lint
```

### Ferramentas de Qualidade

- **Black**: Formatação automática de código
- **Flake8**: Análise estática e linting
- **isort**: Organização de imports
- **pre-commit**: Hooks automáticos de qualidade

Para mais detalhes, veja [DESENVOLVIMENTO.md](DESENVOLVIMENTO.md).

## 📊 Exemplo de Relatório

```
📊 RELATÓRIO DE ORGANIZAÇÃO
=====================================
📁 Diretório analisado: /home/user/fotos
⏰ Data/hora: 2024-12-01 14:30:22

📈 ESTATÍSTICAS GERAIS:
• Total de imagens: 1,247
• Imagens organizadas: 1,180
• Imagens com problemas: 67
• Duplicatas encontradas: 15

📅 DISTRIBUIÇÃO POR ANO:
• 2024: 520 fotos
• 2023: 485 fotos
• 2022: 242 fotos

💾 BACKUP:
• Backup criado: backup_20241201_143022
• Tamanho: 2.4 GB
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'feat: add amazing feature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Leidejane da Rosa**
- GitHub: [@LeidejanedaRosa](https://github.com/LeidejanedaRosa)

## 🆘 Suporte

Se você encontrou um bug ou tem uma sugestão, por favor:

1. Verifique se já existe uma [issue](https://github.com/LeidejanedaRosa/photo-organizer/issues) sobre o assunto
2. Se não existir, crie uma nova issue com detalhes
3. Para dúvidas de uso, consulte a documentação ou abra uma discussão

## 🙏 Agradecimentos

- Comunidade Python pelo excelente ecossistema
- Contribuidores que ajudaram a melhorar o projeto
- Bibliotecas utilizadas: Pillow, pathlib, e outras

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!** ⭐
