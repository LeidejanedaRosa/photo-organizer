# 📸 Manual do Usuário - Sistema de Organiz#### **Opção B: Sistema Padrão** 
- Usa configuração básica com prefixo "IMG"
- Organização por períodos mensais
- Data base configurável pelo usuário de Fotos

## 🎯 Visão Geral

Este sistema foi desenvolvido para organizar automaticamente suas fotos de forma inteligente e personalizada. Ele pode:

- **Organizar por data** - Classifica fotos pela data de criação
- **Detectar duplicatas** - Move fotos duplicad### **Cenário 3: Álbum de Bebê**
```
Configuração:
- Sistema Compatível (IMG)
- Data nascimento: 17/08/2024

Caminho da pasta: /sua/pasta/fotos-bebe

Resultado:
- 00 - IMG 17082024(00).jpg (Nascimento)
- 01 - IMG 15092024(00).jpg (1º mês)
- 02 - IMG 20102024(00) - Primeiro Sorriso.jpg (2º mês)
```ta separada  
- **Renomear automaticamente** - Aplica padrão consistente de nomenclatura
- **Organizar eventos especiais** - Cria pastas para eventos como "Batizado", "Aniversário"
- **Continuar organização** - Integra novas fotos sem mexer nas já organizadas
- **Backup automático** - Protege suas fotos antes de qualquer alteração

---

## 🚀 Como Começar

### 1. Executar o Sistema
```bash
python3 main.py
```

### 2. Escolher Configuração

O sistema oferece duas opções principais:

#### **Opção A: Configuração Personalizada (Recomendada)**
- Você define suas próprias regras
- Ideal para qualquer projeto: viagens, eventos, família
- Totalmente flexível

#### **Opção B: Sistema Compatível** 
- Usa configuração pré-definida (fotos de bebê)
- Data base: 01/01/2025
- Prefixo: "IMG"

---

## 📋 Passo a Passo Completo

### **ETAPA 1: Configuração do Projeto**

1. Execute o programa: `python main.py`
2. Escolha a opção **9 - Configuração Personalizada**
3. Preencha as informações:

```
⚙️  CONFIGURAÇÃO PERSONALIZADA DO PROJETO
============================================================
📅 Data de início (DD/MM/AAAA): 01/01/2023
📅 Data final (DD/MM/AAAA) [opcional]: 31/12/2023  
🏷️  Prefixo da nomenclatura: VIAGEM
📊 Incluir cálculo de período/mês? (s/N): s
```

**Resultado:** Sistema configurado para suas necessidades específicas.

### **ETAPA 2: Organização Automática**

1. Escolha a opção **3 - Processo Completo**
2. Informe o caminho da pasta com fotos quando solicitado
3. O sistema executará automaticamente:

#### **2.1 Análise Inicial**
```
🔍 ANALISANDO DIRETÓRIO: /sua/pasta/MinhasFotos
📊 Encontradas: 150 imagens
   ✅ 45 já organizadas
   📝 105 precisam ser organizadas
```

#### **2.2 Detecção de Duplicatas**
```
🔍 DETECTANDO DUPLICATAS...
📋 Simulação:
   📷 IMG_001.jpg -> DUPLICADO de VIAGEM 15032023(00).jpg
   📷 IMG_002.jpg -> DUPLICADO de VIAGEM 16032023(01).jpg
   
❓ Confirma mover 2 duplicatas para pasta 'duplicadas'? (s/N):
```

#### **2.3 Renomeação Inteligente**
```
📝 RENOMEANDO IMAGENS...
📋 Simulação:
   📷 DSC001.jpg -> 01 - VIAGEM 15032023(00).jpg
   📷 DSC002.jpg -> 01 - VIAGEM 15032023(01).jpg
   📷 DSC003.jpg -> 01 - VIAGEM 16032023(00).jpg
   
❓ Confirma as alterações? (s/N):
```

### **ETAPA 3: Organizando Eventos Especiais**

Se você tem fotos de eventos especiais (Batizado, Aniversário, Casamento):

1. Durante a renomeação, o sistema perguntará sobre eventos
2. Você pode definir eventos para datas específicas:

```
🎉 CONFIGURAÇÃO DE EVENTOS
Digite datas com eventos (formato DD/MM/AAAA):
📅 Data: 15/03/2023
🎈 Evento: Batizado
📅 Data: 20/03/2023  
🎈 Evento: Aniversário
📅 Data: [Enter para finalizar]
```

**Resultado das fotos com eventos:**
```
📷 01 - VIAGEM 15032023(00) - Batizado.jpg
📷 01 - VIAGEM 15032023(01) - Batizado.jpg  
📷 01 - VIAGEM 20032023(00) - Aniversário.jpg
```

### **ETAPA 4: Organização em Pastas (Opcional)**

Após renomear, o sistema oferece organizar em pastas:

```
📁 ORGANIZAÇÃO POR PASTAS DE EVENTOS
❓ Deseja organizar fotos de eventos em pastas separadas? (s/N): s

Criando estrutura:
📁 MinhasFotos/
   📁 Batizado/
      📷 01 - VIAGEM 15032023(00) - Batizado.jpg
      📷 01 - VIAGEM 15032023(01) - Batizado.jpg
   📁 Aniversário/  
      📷 02 - VIAGEM 20032023(00) - Aniversário.jpg
   📁 Geral/
      📷 01 - VIAGEM 16032023(00).jpg
      📷 02 - VIAGEM 17032023(00).jpg
```

---

## 🏷️ Sistema de Nomenclatura

### **Formato Completo:**
```
[PERÍODO] - [PREFIXO] [DATA](SEQUENCIAL) [- EVENTO]
```

### **Exemplos Práticos:**

#### **Com Configuração "VIAGEM":**
- `01 - VIAGEM 15032023(00).jpg` - Primeira foto do dia 15/03/2023, período 01
- `01 - VIAGEM 15032023(01).jpg` - Segunda foto do mesmo dia
- `01 - VIAGEM 15032023(00) - Batizado.jpg` - Primeira foto com evento especial

#### **Com Configuração "IMG" (Padrão):**
- `02 - IMG 15102024(00).jpg` - Foto do 2º período
- `03 - IMG 20112024(01) - Primeiro Evento.jpg` - Segunda foto com evento

#### **Sem Período (Configuração Simples):**
- `FOTO 15032023(00).jpg` - Apenas data e sequencial
- `CORP 20112023(01) - Reunião.jpg` - Foto corporativa com evento

---

## 📊 Entendendo os Períodos

### **Sistema Personalizado:**
Baseado na sua data de início configurada.

**Exemplo - Projeto iniciado em 01/01/2023:**
- **Período 00:** Janeiro/2023 (01/01 a 31/01)
- **Período 01:** Fevereiro/2023 (01/02 a 28/02)  
- **Período 02:** Março/2023 (01/03 a 31/03)

### **Sistema Padrão:**
Baseado na configuração definida pelo usuário.

**Exemplo - Projeto iniciado em 01/01/2023:**
- **Período 00:** Janeiro/2023 (01/01 a 31/01)
- **Período 01:** Fevereiro/2023 (01/02 a 28/02)  
- **Período 02:** Março/2023 (01/03 a 31/03)

---

## 🔧 Funcionalidades Avançadas

### **1. Adicionar Novas Fotos a Pasta Organizada**

Quando você adiciona novas fotos a uma pasta já organizada:

1. Execute novamente o sistema na mesma pasta
2. Ele detectará automaticamente as fotos já organizadas
3. Organizará apenas as novas fotos
4. Manterá a numeração sequencial correta

**Exemplo:**
```
🔍 ANÁLISE DA PASTA:
   ✅ 50 fotos já organizadas (mantidas intactas)
   📝 10 novas fotos para organizar
   
📝 Organizando apenas as novas fotos...
   📷 nova_foto1.jpg -> 03 - VIAGEM 25032023(02).jpg
   📷 nova_foto2.jpg -> 03 - VIAGEM 25032023(03).jpg
```

### **2. Busca por Período**

Localiza rapidamente fotos de um período específico:

```
Menu Principal > Opção 5 - Buscar por Período
📅 Digite o período (formato MM): 02
📋 Encontradas 15 fotos do período 02:
   📷 02 - VIAGEM 15032023(00).jpg
   📷 02 - VIAGEM 16032023(00).jpg
   📷 02 - VIAGEM 17032023(01).jpg
```

### **3. Relatório Detalhado**

Gera estatísticas completas da sua coleção:

```
📊 RELATÓRIO DETALHADO:
============================================================
📁 Diretório: /sua/pasta/MinhasFotos
📷 Total de imagens: 150
✅ Organizadas: 145 (96.7%)
📝 Não organizadas: 5 (3.3%)
🔁 Duplicatas: 8

📈 Por Período:
   Período 00: 25 fotos
   Período 01: 30 fotos  
   Período 02: 35 fotos

🎉 Eventos Especiais:
   Batizado: 12 fotos
   Aniversário: 8 fotos
   Casamento: 15 fotos
```

### **4. Sistema de Backup**

Antes de qualquer operação, o sistema cria backups automáticos:

```
🛡️  CRIANDO BACKUP...
📁 Backup salvo em: /sua/pasta/MinhasFotos/.backup_20231215_143022/
✅ Backup concluído! Suas fotos estão protegidas.
```

---

## 📂 Estrutura Final Organizada

Após todo o processo, sua pasta ficará assim:

```
MinhasFotos/
├── .backup_20231215_143022/          # Backup automático
├── duplicadas/                       # Fotos duplicadas
│   ├── IMG_001.jpg
│   └── IMG_002.jpg
├── Batizado/                         # Eventos especiais (opcional)
│   ├── 01 - VIAGEM 15032023(00) - Batizado.jpg
│   └── 01 - VIAGEM 15032023(01) - Batizado.jpg
├── Aniversário/
│   └── 02 - VIAGEM 20032023(00) - Aniversário.jpg
├── Geral/                           # Fotos sem evento especial
│   ├── 01 - VIAGEM 16032023(00).jpg
│   ├── 01 - VIAGEM 17032023(00).jpg
│   ├── 02 - VIAGEM 18032023(00).jpg
│   └── 03 - VIAGEM 25032023(00).jpg
└── organizacao_log.txt               # Log das operações
```

---

## ⚙️ Cenários de Uso Práticos

### **Cenário 1: Fotos de Viagem**
```
Configuração:
- Data início: 01/06/2023
- Data fim: 31/08/2023  
- Prefixo: VIAGEM
- Período: Sim

Caminho da pasta: /sua/pasta/fotos-viagem

Resultado:
- 01 - VIAGEM 15062023(00).jpg (Junho)
- 02 - VIAGEM 20072023(00).jpg (Julho)  
- 03 - VIAGEM 10082023(00).jpg (Agosto)
```

### **Cenário 2: Evento Corporativo**
```
Configuração:
- Data início: 15/11/2023
- Prefixo: CORP
- Período: Não

Caminho da pasta: /sua/pasta/evento-corporativo

Resultado:
- CORP 15112023(00).jpg
- CORP 15112023(01) - Palestras.jpg
- CORP 16112023(00) - Confraternização.jpg
```

### **Cenário 3: Álbum de Bebê**
```
Configuração:
- Sistema Compatível (IMG)
- Data nascimento: 01/01/2025

Resultado:
- 00 - IMG 17082024(00).jpg (Nascimento)
- 01 - IMG 15092024(00).jpg (1º mês)
- 02 - IMG 20102024(00) - Primeiro Sorriso.jpg (2º mês)
```

---

## 🛡️ Segurança e Proteção

### **Backups Automáticos**
- Criados antes de qualquer operação destrutiva
- Preservam estado original completo
- Fáceis de restaurar se necessário

### **Modo Simulação**
- Todas as operações são simuladas primeiro
- Você vê exatamente o que vai acontecer
- Confirma antes de executar

### **Validações**
- Verifica formatos de arquivo suportados
- Valida datas e configurações
- Previne sobrescrita acidental

---

## ❓ Perguntas Frequentes

### **P: Posso mudar a configuração no meio do projeto?**
R: Sim! Você pode reconfigurar a qualquer momento. O sistema manterá as fotos já organizadas e aplicará a nova configuração apenas às novas fotos.

### **P: E se eu quiser organizar vídeos também?**
R: Atualmente o sistema foca em fotos, mas há planos para incluir vídeos em versões futuras.

### **P: Posso usar prefixos diferentes para eventos diferentes?**
R: No momento, o prefixo é definido por projeto. Mas você pode executar o sistema várias vezes com configurações diferentes para subconjuntos de fotos.

### **P: O que acontece se duas fotos tiverem exatamente a mesma data e hora?**
R: O sistema usa numeração sequencial: `(00)`, `(01)`, `(02)`, etc., garantindo nomes únicos.

### **P: Como restaurar um backup?**
R: Copie o conteúdo da pasta `.backup_AAAAMMDD_HHMMSS/` de volta para a pasta principal.

---

## 🎯 Dicas Pro

1. **Configure primeiro**: Sempre configure o projeto antes de organizar
2. **Teste em pasta pequena**: Teste com poucas fotos primeiro
3. **Use eventos estrategicamente**: Agrupe fotos relacionadas com eventos
4. **Mantenha backups**: Os backups automáticos são seus amigos
5. **Organize incrementalmente**: Adicione novas fotos gradualmente
6. **Use relatórios**: Acompanhe o progresso com relatórios detalhados

---

## 🚀 Exemplo Completo Passo a Passo

Vamos organizar uma pasta de fotos de festa de aniversário:

### **1. Configuração**
```bash
python main.py
# Escolher opção 9
Data início: 20/07/2023
Prefixo: FESTA
Período: Não
```

### **2. Organização**
```bash
# Escolher opção 3 - Processo Completo
Pasta: /sua/pasta/Aniversario_Maria
```

### **3. Definir Eventos**
```
Data: 20/07/2023 -> Evento: Aniversário
Data: 21/07/2023 -> Evento: Pós-festa
```

### **4. Resultado Final**
```
Aniversario_Maria/
├── .backup_20231215_150000/
├── duplicadas/
├── Aniversário/
│   ├── FESTA 20072023(00) - Aniversário.jpg
│   ├── FESTA 20072023(01) - Aniversário.jpg
│   └── FESTA 20072023(02) - Aniversário.jpg
├── Pós-festa/
│   └── FESTA 21072023(00) - Pós-festa.jpg
└── Geral/
    └── FESTA 19072023(00).jpg
```

---

## 📞 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique se a pasta existe e tem fotos
2. Confira as permissões de escrita
3. Restaure o backup se algo der errado
4. Execute com pasta pequena para teste

O sistema foi projetado para ser seguro e reversível, então explore sem medo! 🚀

---

*Manual atualizado para versão 2.0 - Sistema de Configuração Personalizada*
