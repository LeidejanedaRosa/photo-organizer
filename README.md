# Photo Organizer

Um organizador inteligente de fotos e arquivos que separa automaticamente seus arquivos por tipo, mantendo suas imagens organizadas na pasta principal.

## 🎯 Funcionalidades

- **📸 Identificação inteligente** de tipos de arquivo (Imagem, Vídeo, Texto, Outros)
- **📁 Organização automática** em pastas específicas
- **🔒 Segurança** - não sobrescreve arquivos existentes
- **⚡ Interface dupla** - CLI e JSON (preparado para frontend)
- **🧪 Totalmente testado** com cobertura abrangente

## 🚀 Como Usar

### Interface de Linha de Comando (CLI)

```bash
# Analisar arquivos sem organizar
python3 main.py "/caminho/para/pasta"

# Organizar arquivos automaticamente
python3 main.py "/caminho/para/pasta" --organize

# Saída em JSON (para integração com frontend)
python3 main.py "/caminho/para/pasta" --json
python3 main.py "/caminho/para/pasta" --organize --json
```

### Como Funciona a Organização

- **🖼️ Imagens** (JPG, PNG, GIF, etc.) → Permanecem na pasta atual
- **🎬 Vídeos** (MP4, AVI, MOV, etc.) → Pasta `Videos/`
- **📄 Textos** (PDF, DOC, TXT, etc.) → Pasta `Textos/`
- **📦 Outros** (arquivos sem extensão específica) → Pasta `Outros/`

*Pastas são criadas apenas quando há arquivos para mover!*

## 🏗️ Arquitetura (Preparada para Frontend)

O projeto foi estruturado em camadas para facilitar a futura integração com interfaces web:

```
photo_organizer/
├── models.py          # Modelos de dados (Request/Response)
├── service.py         # Lógica de negócio pura
├── controller.py      # Controladores (preparados para API)
├── file_handler.py    # Manipulação de arquivos
├── file_organizer.py  # Organização de arquivos
└── directory_scanner.py # Escaneamento de diretórios
```

### Exemplo de Saída JSON

```json
{
  "success": true,
  "message": "Organização concluída: 15 arquivos movidos.",
  "data": {
    "source_folder": "/home/user/fotos",
    "total_files": 55,
    "files_by_type": {
      "Imagem": 40,
      "Vídeo": 11,
      "Texto": 1,
      "Outro": 3
    },
    "moved_files": {
      "Vídeo": 11,
      "Texto": 1,
      "Outro": 3
    },
    "folders_created": ["Videos", "Textos", "Outros"],
    "organization_summary": {
      "total_analyzed": 55,
      "total_moved": 15,
      "images_remaining": 40
    }
  },
  "errors": []
}
```

## 🌐 Integração com Frontend (Futura)

O projeto está preparado para receber um frontend web. Estrutura sugerida:

### Endpoints Planejados

 `GET /api/analyze?path={urlencoded_path}` - Analisa pasta (dentro de um diretório raiz permitido)
- `POST /api/organize` - Organiza arquivos
- `GET /api/file-types` - Tipos suportados
- `GET /api/health` - Status da API
> Nota: normalize o caminho no backend (join seguro + bloqueio de `..`) e exija que `path` esteja sob um diretório raiz configurado.

### Frameworks Recomendados

- **Backend**: Flask ou FastAPI
- **Frontend**: React.js, Vue.js, Angular ou Vanilla JS
- **Exemplo**: Veja `api_example.py` para implementação de referência

## 🧪 Testes

```bash
# Executar todos os testes
python3 -m unittest discover tests -v

# Testes específicos
python3 -m unittest tests.test_file_organizer -v
python3 -m unittest tests.test_service_and_controller -v
```

## 📦 Instalação

```bash
# Clone o repositório
git clone <repository-url>
cd photo-organizer

# Execute (sem dependências externas!)
python3 main.py --help
```

## 🎯 Exemplos de Uso

### Comando Básico
```bash
python3 main.py "/home/user/Downloads"
```

### Organização Completa
```bash
python3 main.py "/home/user/Photos" --organize
```

### Para Desenvolvimento (JSON)
```bash
python3 main.py "/home/user/Photos" --organize --json | jq '.'
```

## 🔄 Roadmap

- [x] ✅ CLI funcional
- [x] ✅ Estrutura para API
- [x] ✅ Saída JSON
- [x] ✅ Testes abrangentes
- [ ] 🔲 API REST (Flask/FastAPI)
- [ ] 🔲 Interface web
- [ ] 🔲 Configurações customizáveis
- [ ] 🔲 Organização por data
- [ ] 🔲 Preview de arquivos

## 📋 Tipos de Arquivo Suportados

| Tipo | Extensões | Destino |
|------|-----------|---------|
| **Imagem** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff` | Pasta atual |
| **Vídeo** | `.mp4`, `.mov`, `.avi`, `.mkv`, `.flv`, `.wmv` | `Videos/` |
| **Texto** | `.txt`, `.doc`, `.docx`, `.pdf`, `.rtf`, `.odt` | `Textos/` |
| **Outro** | Demais extensões | `Outros/` |

---

**Photo Organizer** - Mantenha suas fotos organizadas e seus arquivos no lugar certo! 📸✨
