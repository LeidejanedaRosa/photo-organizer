import os
import shutil
import hashlib
import re
import json
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from typing import NamedTuple
from pathlib import Path
from collections import defaultdict


class InfoImagem(NamedTuple):
    arquivo: str
    formato: str | None  # Formato pode ser None para alguns tipos de arquivo
    dimensoes: tuple
    modo: str
    tamanho: int
    data_mod: datetime
    data_exif: datetime | None
    hash_imagem: str | None = None


def criar_backup_operacao(diretorio: str, operacao: str) -> str:
    """
    Cria um backup/log das operações realizadas.
    Retorna o caminho do arquivo de backup criado.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(diretorio, "backups")
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    backup_file = os.path.join(
        backup_dir, f"backup_{operacao}_{timestamp}.json"
    )
    
    # Lista todos os arquivos atuais
    arquivos_atuais = []
    for arquivo in os.listdir(diretorio):
        caminho = os.path.join(diretorio, arquivo)
        if os.path.isfile(caminho) and not arquivo.endswith('.json'):
            try:
                stat = os.stat(caminho)
                arquivos_atuais.append({
                    "nome": arquivo,
                    "tamanho": stat.st_size,
                    "modificado": datetime.fromtimestamp(
                        stat.st_mtime
                    ).isoformat()
                })
            except (OSError, IOError):
                continue
    
    backup_data = {
        "operacao": operacao,
        "timestamp": timestamp,
        "diretorio": diretorio,
        "arquivos": arquivos_atuais
    }
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)
    
    return backup_file
        
        if imagens_por_ano:
            print(f"\n🎂 ANOS DO BEBÊ DETECTADOS ({len(imagens_por_ano)}):")
            for ano in sorted(imagens_por_ano.keys()):
                print(f"   📅 Ano {ano}: {len(imagens_por_ano[ano])} imagem(ns)")
                # Mostra período do ano
                if ano == 1:
                    print("       📆 Período: 01/01/2025 a 31/12/2025")
                elif ano == 2:
                    print("       📆 Período: 17/08/2025 a 16/08/2026")
                else:
                    inicio = 2024 + (ano - 1)
                    fim = inicio + 1
                    print(f"       📆 Período: 17/08/{inicio} a 16/08/{fim}")
            
            # Mostra simulação
            organizar_por_anos_automatico(imagens_todas, diretorio, simular=True)
            
            # Pergunta confirmação
            resposta = input("\n❓ Confirma a organização por anos? (s/N): ").lower()
            if resposta == 's':
                # Cria backup antes da operação
                backup_file = criar_backup_operacao(diretorio, "organizar_anos")
                print(f"💾 Backup criado: {os.path.basename(backup_file)}")
                organizar_por_anos_automatico(imagens_todas, diretorio, simular=False)
        else:
            print("📅 Nenhuma imagem com data válida para organização por anos.")
            print("💡 As imagens devem ter datas a partir de 01/01/2025.")
            
    elif opcao == 9:
        print("💾 CRIANDO BACKUP DO ESTADO ATUAL...")
        backup_file = criar_backup_operacao(diretorio, "backup_manual")
        print("✅ Backup criado com sucesso!")
        print(f"📁 Arquivo: {backup_file}")
        print(f"📊 {len(imagens_todas)} imagens registradas no backup.")}_{timestamp}.json"
    )
    
    # Lista todos os arquivos atuais
    arquivos_atuais = []
    for arquivo in os.listdir(diretorio):
        caminho = os.path.join(diretorio, arquivo)
        if os.path.isfile(caminho) and not arquivo.endswith('.json'):
            try:
                stat = os.stat(caminho)
                arquivos_atuais.append({
                    "nome": arquivo,
                    "tamanho": stat.st_size,
                    "modificado": datetime.fromtimestamp(
                        stat.st_mtime
                    ).isoformat()
                })
            except (OSError, IOError):
                continue
    
    backup_data = {
        "operacao": operacao,
        "timestamp": timestamp,
        "diretorio": diretorio,
        "arquivos": arquivos_atuais
    }
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)
    
    return backup_file


def gerar_relatorio_detalhado(imagens: list[InfoImagem]) -> None:
    """Gera um relatório detalhado das imagens analisadas."""
    if not imagens:
        print("📋 Nenhuma imagem para analisar no relatório.")
        return
    
    print("\n" + "=" * 70)
    print("📊 RELATÓRIO DETALHADO DAS IMAGENS")
    print("=" * 70)
    
    # Estatísticas gerais
    total_imagens = len(imagens)
    total_tamanho = sum(img.tamanho for img in imagens)
    
    # Análise por formato
    formatos = defaultdict(int)
    tamanhos_por_formato = defaultdict(int)
    for img in imagens:
        formatos[img.formato] += 1
        tamanhos_por_formato[img.formato] += img.tamanho
    
    # Análise por mês do bebê
    meses_bebe = defaultdict(int)
    for img in imagens:
        data = img.data_exif or img.data_mod
        mes = calcular_mes_bebe(data)
        meses_bebe[mes] += 1
    
    # Análise por dimensões
    dimensoes = defaultdict(int)
    for img in imagens:
        dim_str = f"{img.dimensoes[0]}x{img.dimensoes[1]}"
        dimensoes[dim_str] += 1
    
    print("\n📈 ESTATÍSTICAS GERAIS:")
    print(f"   📷 Total de imagens: {total_imagens}")
    print(f"   💾 Tamanho total: {total_tamanho / (1024*1024):.2f} MB")
    print(f"   📏 Tamanho médio: {total_tamanho / total_imagens / 1024:.1f} KB")
    
    print("\n🎨 DISTRIBUIÇÃO POR FORMATO:")
    for formato, count in sorted(formatos.items()):
        tamanho_mb = tamanhos_por_formato[formato] / (1024*1024)
        porcentagem = (count / total_imagens) * 100
        print(
            f"   📄 {formato}: {count} arquivos ({porcentagem:.1f}%) - "
            f"{tamanho_mb:.2f} MB"
        )
    
    print("\n📅 DISTRIBUIÇÃO POR MÊS DO BEBÊ:")
    for mes in sorted(meses_bebe.keys()):
        count = meses_bebe[mes]
        porcentagem = (count / total_imagens) * 100
        print(f"   🗓️  Mês {mes:02d}: {count} fotos ({porcentagem:.1f}%)")
    
    print("\n📐 RESOLUÇÕES MAIS COMUNS:")
    top_dimensoes = sorted(
        dimensoes.items(), key=lambda x: x[1], reverse=True
    )[:5]
    for dim, count in top_dimensoes:
        porcentagem = (count / total_imagens) * 100
        print(f"   🖼️  {dim}: {count} imagens ({porcentagem:.1f}%)")
    
    # Análise temporal
    if imagens:
        datas = [img.data_exif or img.data_mod for img in imagens]
        data_mais_antiga = min(datas)
        data_mais_recente = max(datas)
        periodo = (data_mais_recente - data_mais_antiga).days
        
        print("\n⏰ ANÁLISE TEMPORAL:")
        print(
            f"   📆 Foto mais antiga: "
            f"{data_mais_antiga.strftime('%d/%m/%Y %H:%M')}"
        )
        print(
            f"   📆 Foto mais recente: "
            f"{data_mais_recente.strftime('%d/%m/%Y %H:%M')}"
        )
        print(f"   📊 Período abrangido: {periodo} dias")
        
        if periodo > 0:
            frequencia = total_imagens / periodo
            print(f"   📈 Frequência média: {frequencia:.2f} fotos/dia")
    
    print("=" * 70)


def buscar_fotos_periodo(
    imagens: list[InfoImagem],
    data_inicio: str,
    data_fim: str
) -> list[InfoImagem]:
    """
    Busca fotos em um período específico.
    Formato das datas: DD/MM/AAAA
    """
    try:
        inicio = datetime.strptime(data_inicio, '%d/%m/%Y')
        fim = datetime.strptime(data_fim, '%d/%m/%Y')
        
        # Ajusta para incluir o dia inteiro
        fim = fim.replace(hour=23, minute=59, second=59)
        
        fotos_periodo = []
        for img in imagens:
            data_foto = img.data_exif or img.data_mod
            if inicio <= data_foto <= fim:
                fotos_periodo.append(img)
        
        return fotos_periodo
    except ValueError:
        print("❌ Formato de data inválido! Use DD/MM/AAAA")
        return []


def esta_organizada(nome_arquivo: str) -> bool:
    """
    Verifica se o arquivo já segue o padrão de organização.
    Formato esperado: MM - IMG DDMMAAAA(XX)[- evento].extensão
    """
    # Remove a extensão para análise
    nome_sem_ext = Path(nome_arquivo).stem
    
    # Padrão regex para detectar arquivos já organizados
    # Formato: DD - IMG DDMMAAAA(XX) opcionalmente seguido de - evento
    padrao = r'^\d{2} - IMG \d{8}\(\d{2}\)(?:\s-\s.+)?$'
    
    return bool(re.match(padrao, nome_sem_ext))


def calcular_hash_imagem(caminho: str) -> str:
    """Calcula o hash MD5 do conteúdo da imagem."""
    hasher = hashlib.md5()
    try:
        with Image.open(caminho) as img:
            # Converte para um formato comum para comparação
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Converte a imagem em bytes para calcular o hash
            img_bytes = img.tobytes()
            hasher.update(img_bytes)
    except (IOError, OSError) as e:
        print(f"Erro ao calcular hash de {caminho}: {e}")
        return ""
    return hasher.hexdigest()


def encontrar_duplicadas(
    imagens: list[InfoImagem]
) -> dict[str, list[InfoImagem]]:
    """
    Encontra imagens duplicadas baseado em seu hash e características.
    Retorna um dicionário onde a chave é o hash e o valor é a lista de
    imagens duplicadas.
    """
    grupos_hash: dict[str, list[InfoImagem]] = defaultdict(list)
    
    # Primeiro, agrupa por hash
    for img in imagens:
        if img.hash_imagem:
            grupos_hash[img.hash_imagem].append(img)
    
    # Filtra apenas os grupos que têm duplicatas
    return {
        hash_: grupo
        for hash_, grupo in grupos_hash.items()
        if len(grupo) > 1
    }


def mover_duplicadas(
    duplicadas: dict[str, list[InfoImagem]],
    diretorio_origem: str,
    simular: bool = True
) -> None:
    """Move as imagens duplicadas para uma pasta de duplicadas."""
    if not duplicadas:
        print("✅ Nenhuma imagem duplicada encontrada!")
        return
    
    # Cria a pasta de duplicadas se não existir
    pasta_duplicadas = os.path.join(diretorio_origem, "duplicadas")
    if not simular and not os.path.exists(pasta_duplicadas):
        os.makedirs(pasta_duplicadas)
    
    if simular:
        print("\n🔄 SIMULAÇÃO: Movendo duplicatas...")
    else:
        print("\n📦 MOVENDO DUPLICATAS...")
    
    print("─" * 60)
    
    total_movidas = 0
    total_grupos = len(duplicadas)
    
    for i, grupo in enumerate(duplicadas.values(), 1):
        # Mantém a primeira imagem (geralmente a mais antiga) e move as outras
        original = grupo[0]
        print(f"\n📂 Grupo {i}/{total_grupos} de duplicatas:")
        print(f"   🏠 Mantendo: {original.arquivo}")
        
        for duplicata in grupo[1:]:
            origem = os.path.join(diretorio_origem, duplicata.arquivo)
            destino = os.path.join(pasta_duplicadas, duplicata.arquivo)
            
            if simular:
                print(f"   📤 Moveria: {duplicata.arquivo}")
            else:
                print(f"   📤 Movendo: {duplicata.arquivo}")
            
            if not simular:
                try:
                    shutil.move(origem, destino)
                    total_movidas += 1
                    print("      ✅ Sucesso")
                except (IOError, OSError) as e:
                    print(f"      ❌ Erro: {e}")
    
    print("─" * 60)
    if not simular:
        print(
            f"📊 RESULTADO: {total_movidas} imagens movidas para "
            "'duplicadas/'"
        )
    else:
        duplicatas_total = sum(len(grupo) - 1 for grupo in duplicadas.values())
        print(f"📊 PREVISÃO: {duplicatas_total} imagens seriam movidas")
    print("─" * 60)


def get_data_exif(img):
    try:
        exif = img.getexif()
        if exif is not None:
            for tag_id in exif:
                tag = TAGS.get(tag_id, tag_id)
                data = exif.get(tag_id)
                if tag == 'DateTimeOriginal':
                    return datetime.strptime(data, '%Y:%m:%d %H:%M:%S')
    except (AttributeError, ValueError, TypeError):
        return None
    return None


def get_info_imagem(caminho: str) -> InfoImagem | None:
    try:
        with Image.open(caminho) as img:
            data_mod = datetime.fromtimestamp(os.path.getmtime(caminho))
            fmt = img.format or "Desconhecido"  # Fallback se format for None
            hash_imagem = calcular_hash_imagem(caminho)
            return InfoImagem(
                arquivo=os.path.basename(caminho),
                formato=fmt,
                dimensoes=img.size,
                modo=img.mode,
                tamanho=os.path.getsize(caminho),
                data_mod=data_mod,
                data_exif=get_data_exif(img),
                hash_imagem=hash_imagem
            )
    except (IOError, OSError) as e:
        print(f"Não foi possível ler '{os.path.basename(caminho)}': {e}")
        return None


def calcular_mes_bebe(data: datetime) -> int:
    """Calcula o mês do bebê baseado na data da foto."""
    mes = data.month
    dia = data.day
    
    # Se estamos em agosto
    if mes == 8:
        # Se é depois ou igual a 17/08
        if dia >= 17:
            return 0  # Mês 00
        else:
            return 12  # Mês 12 (primeira parte de agosto)
    
    # Para outros meses
    if mes >= 9:  # Setembro a dezembro
        return mes - 8  # 9-8=1 (setembro), 10-8=2 (outubro), etc.
    else:  # Janeiro a julho
        return mes + 4  # 1+4=5 (janeiro), 2+4=6 (fevereiro), etc.


def calcular_ano_bebe(data: datetime) -> int:
    """
    Calcula qual ano do bebê baseado na data da foto.
    Ano 1: 01/01/2025 a 31/12/2025
    Ano 2: 17/08/2025 a 16/08/2026
    E assim por diante...
    """
    # Data de nascimento base: 01/01/2025
    data_nascimento = datetime(2024, 8, 17)
    
    # Se a foto é antes do nascimento, retorna 0 (inválido)
    if data < data_nascimento:
        return 0
    
    # Calcula quantos anos completos se passaram
    anos_completos = data.year - data_nascimento.year
    
    # Verifica se já passou o aniversário no ano atual
    aniversario_atual = datetime(data.year, 8, 17)
    
    if data >= aniversario_atual:
        return anos_completos + 1
    else:
        return anos_completos + 1 if anos_completos >= 0 else 1


def organizar_por_anos_automatico(
    imagens: list[InfoImagem],
    diretorio: str,
    simular: bool = True
) -> dict[int, list[InfoImagem]]:
    """
    Organiza imagens automaticamente por ano do bebê.
    Retorna um dicionário com ano -> lista de imagens
    """
    if not imagens:
        return {}
    
    # Agrupa imagens por ano do bebê
    imagens_por_ano = defaultdict(list)
    
    for img in imagens:
        data = img.data_exif or img.data_mod
        ano_bebe = calcular_ano_bebe(data)
        if ano_bebe > 0:  # Só considera datas válidas
            imagens_por_ano[ano_bebe].append(img)
    
    if not imagens_por_ano:
        print("📅 Nenhuma imagem com data válida para organização por anos.")
        return {}
    
    if simular:
        print("\n🔄 SIMULAÇÃO: Organizando por anos do bebê...")
    else:
        print("\n📅 ORGANIZANDO POR ANOS DO BEBÊ...")
    
    print("─" * 70)
    
    total_organizadas = 0
    
    for ano, imgs_do_ano in sorted(imagens_por_ano.items()):
        pasta_ano = os.path.join(diretorio, f"Ano {ano}")
        
        print(f"\n📂 Ano {ano} do bebê")
        print(f"   📊 {len(imgs_do_ano)} imagem(ns) encontrada(s)")
        
        if simular:
            print(f"   📁 Criaria pasta: Ano {ano}/")
            for img in imgs_do_ano:
                print(f"   📤 Moveria: {img.arquivo}")
        else:
            # Cria a pasta se não existir
            if not os.path.exists(pasta_ano):
                os.makedirs(pasta_ano)
                print(f"   ✅ Pasta criada: Ano {ano}/")
            
            # Move as imagens
            for img in imgs_do_ano:
                origem = os.path.join(diretorio, img.arquivo)
                destino = os.path.join(pasta_ano, img.arquivo)
                
                try:
                    shutil.move(origem, destino)
                    total_organizadas += 1
                    print(f"   📤 Movida: {img.arquivo}")
                except (IOError, OSError) as e:
                    print(f"   ❌ Erro ao mover {img.arquivo}: {e}")
    
    print("─" * 70)
    if not simular:
        print(f"📊 RESULTADO: {total_organizadas} imagens organizadas por anos")
    else:
        total_previsao = sum(len(imgs) for imgs in imagens_por_ano.values())
        print(f"📊 PREVISÃO: {total_previsao} imagens seriam organizadas")
    print("─" * 70)
    
    return dict(imagens_por_ano)


class Evento:
    def __init__(self, data: str, descricao: str):
        self.data = data  # No formato DDMMAAAA
        self.descricao = descricao


def solicitar_eventos() -> dict[str, str]:
    """Solicita ao usuário informações sobre eventos nas fotos."""
    eventos = {}
    print("\n" + "─" * 50)
    print("🎉 CONFIGURAÇÃO DE EVENTOS")
    print("─" * 50)
    print("📝 Defina eventos especiais para as datas das fotos.")
    print("💡 Formato da data: DD/MM/AAAA")
    print("🔚 Para finalizar: deixe a data em branco e pressione Enter")
    print("─" * 50)
    
    contador = 1
    while True:
        data = input(f"\n📅 Data do evento #{contador} (DD/MM/AAAA): ").strip()
        if not data:
            break
            
        try:
            # Converte a data para o formato padronizado
            data_obj = datetime.strptime(data, '%d/%m/%Y')
            data_fmt = data_obj.strftime('%d%m%Y')
            descricao = input("🏷️  Descrição do evento: ").strip()
            if descricao:
                eventos[data_fmt] = descricao
                print(f"✅ Evento registrado: {data} - {descricao}")
                contador += 1
        except ValueError:
            print("❌ Data inválida! Use o formato DD/MM/AAAA")
    
    if eventos:
        print(f"\n🎊 {len(eventos)} evento(s) configurado(s) com sucesso!")
    else:
        print("\n📝 Nenhum evento configurado.")
    
    return eventos


def agrupar_por_data(imagens: list[InfoImagem]) -> dict:
    """Agrupa imagens por data e atribui números sequenciais."""
    grupos: dict[str, list[InfoImagem]] = {}
    for img in imagens:
        data = (img.data_exif or img.data_mod).strftime('%d%m%Y')
        if data not in grupos:
            grupos[data] = []
        grupos[data].append(img)
    return grupos


def detectar_eventos_nos_arquivos(
    imagens: list[InfoImagem]
) -> dict[str, list[str]]:
    """
    Detecta eventos nos nomes dos arquivos já organizados.
    Retorna um dicionário com evento -> lista de arquivos
    """
    eventos_detectados = defaultdict(list)
    
    for img in imagens:
        # Verifica se o arquivo já está organizado e tem evento
        if esta_organizada(img.arquivo):
            # Extrai o evento do nome se existir
            # Formato: MM - IMG DDMMAAAA(XX) - EVENTO.ext
            nome_sem_ext = Path(img.arquivo).stem
            if ' - ' in nome_sem_ext:
                partes = nome_sem_ext.split(' - ')
                # Tem pelo menos MM, IMG DDMMAAAA(XX), EVENTO
                if len(partes) >= 3:
                    # Pega tudo após o segundo " - "
                    evento = ' - '.join(partes[2:])
                    eventos_detectados[evento].append(img.arquivo)
    
    return dict(eventos_detectados)


def organizar_por_pastas_evento(
    diretorio: str,
    eventos_detectados: dict[str, list[str]],
    simular: bool = True
) -> None:
    """
    Organiza as fotos em pastas baseadas nos eventos detectados.
    """
    if not eventos_detectados:
        print("📁 Nenhum evento detectado nos nomes dos arquivos.")
        return
    
    if simular:
        print("\n🔄 SIMULAÇÃO: Organizando por pastas de eventos...")
    else:
        print("\n📁 ORGANIZANDO POR PASTAS DE EVENTOS...")
    
    print("─" * 70)
    
    total_movidos = 0
    
    for evento, arquivos in eventos_detectados.items():
        pasta_evento = os.path.join(diretorio, evento)
        
        print(f"\n📂 Evento: {evento}")
        print(f"   📊 {len(arquivos)} arquivo(s) encontrado(s)")
        
        if simular:
            print(f"   📁 Criaria pasta: {evento}/")
            for arquivo in arquivos:
                print(f"   📤 Moveria: {arquivo}")
        else:
            # Cria a pasta se não existir
            if not os.path.exists(pasta_evento):
                os.makedirs(pasta_evento)
                print(f"   ✅ Pasta criada: {evento}/")
            
            # Move os arquivos
            for arquivo in arquivos:
                origem = os.path.join(diretorio, arquivo)
                destino = os.path.join(pasta_evento, arquivo)
                
                try:
                    shutil.move(origem, destino)
                    total_movidos += 1
                    print(f"   📤 Movido: {arquivo}")
                except (IOError, OSError) as e:
                    print(f"   ❌ Erro ao mover {arquivo}: {e}")
    
    print("─" * 70)
    if not simular:
        print(f"📊 RESULTADO: {total_movidos} arquivos organizados em pastas")
    else:
        total_previsao = sum(len(arquivos) for arquivos in eventos_detectados.values())
        print(f"📊 PREVISÃO: {total_previsao} arquivos seriam organizados")
    print("─" * 70)


def gerar_novo_nome(
    info: InfoImagem,
    numero_sequencial: int = 0,
    eventos: dict[str, str] | None = None
) -> str:
    """Gera um novo nome para o arquivo baseado no padrão fornecido."""
    data = info.data_exif or info.data_mod
    
    # Calcula o mês do bebê
    mes_bebe = calcular_mes_bebe(data)
    
    # Gera o novo nome no formato solicitado
    novo_nome = (
        f"{mes_bebe:02d} - IMG "
        f"{data.strftime('%d%m%Y')}"
    )
    
    # Adiciona o número sequencial
    # Se tem mais de uma foto no dia, adiciona (00), (01), etc
    # Se tem só uma foto no dia, adiciona (00)
    novo_nome = f"{novo_nome}({numero_sequencial:02d})"
    
    # Adiciona a descrição do evento se existir para esta data
    if eventos:
        data_fmt = data.strftime('%d%m%Y')
        if data_fmt in eventos:
            novo_nome = f"{novo_nome} - {eventos[data_fmt]}"
    
    # Adiciona a extensão original
    return novo_nome + Path(info.arquivo).suffix


def renomear_imagens(
    imagens: list[InfoImagem],
    diretorio: str,
    eventos: dict[str, str] | None = None,
    simular: bool = True
) -> None:
    """Renomeia as imagens de acordo com o formato especificado."""
    if simular:
        print("\n🔄 SIMULAÇÃO: Renomeando arquivos...")
        print("─" * 60)
    else:
        print("\n✨ RENOMEANDO ARQUIVOS...")
        print("─" * 60)
    
    # Agrupa as imagens por data
    grupos = agrupar_por_data(imagens)
    
    total_renomeados = 0
    total_erros = 0
    
    # Para cada data
    for _, imgs_do_dia in grupos.items():
        # Ordena as imagens do dia por hora
        imgs_do_dia.sort(key=lambda x: x.data_exif or x.data_mod)
        
        # Para cada imagem do dia
        for idx, img in enumerate(imgs_do_dia):
            caminho_atual = os.path.join(diretorio, img.arquivo)
            novo_nome = gerar_novo_nome(
                img,
                numero_sequencial=idx,
                eventos=eventos
            )
            novo_caminho = os.path.join(diretorio, novo_nome)
            
            if simular:
                print(f"📄 {img.arquivo}")
                print(f"   ➡️  {novo_nome}")
            else:
                print(f"📄 Renomeando: {img.arquivo}")
            
            if not simular:
                try:
                    shutil.move(caminho_atual, novo_caminho)
                    total_renomeados += 1
                    print(f"   ✅ Sucesso: {novo_nome}")
                except (IOError, OSError) as e:
                    total_erros += 1
                    print(f"   ❌ Erro: {e}")
    
    if not simular:
        print("─" * 60)
        print("📊 RESULTADO:")
        print(f"   ✅ Renomeados com sucesso: {total_renomeados}")
        print(f"   ❌ Erros: {total_erros}")
        print("─" * 60)


def ler_dados_imagens(diretorio: str, renomear: bool = False):
    # Coleta informações de todas as imagens
    imagens = []
    imagens_ja_organizadas = []
    
    for arquivo in os.listdir(diretorio):
        caminho = os.path.join(diretorio, arquivo)
        if os.path.isfile(caminho):
            info = get_info_imagem(caminho)
            if info:
                if esta_organizada(info.arquivo):
                    imagens_ja_organizadas.append(info)
                else:
                    imagens.append(info)
    
    # Ordena as imagens por data
    # Usa data EXIF se disponível, senão usa data de modificação
    imagens.sort(key=lambda x: x.data_exif or x.data_mod)
    imagens_ja_organizadas.sort(key=lambda x: x.data_exif or x.data_mod)
    
    # Mostra estatísticas
    total_imagens = len(imagens) + len(imagens_ja_organizadas)
    print("\n📊 ESTATÍSTICAS:")
    print(f"Total de imagens encontradas: {total_imagens}")
    print(f"Já organizadas: {len(imagens_ja_organizadas)}")
    print(f"Precisam ser organizadas: {len(imagens)}")
    
    if imagens_ja_organizadas:
        print(f"\n✅ IMAGENS JÁ ORGANIZADAS ({len(imagens_ja_organizadas)}):")
        for img in imagens_ja_organizadas:
            print(f"  - {img.arquivo}")
    
    if not imagens:
        print("\n🎉 Todas as imagens já estão organizadas!")
        return
    
    print(f"\n📋 IMAGENS PARA ORGANIZAR ({len(imagens)}):")
    # Exibe as informações ordenadas
    for img in imagens:
        data = img.data_exif or img.data_mod
        mes_bebe = calcular_mes_bebe(data)
        
        print(f"Arquivo: {img.arquivo}")
        print(f"Formato: {img.formato}")
        print(f"Dimensões: {img.dimensoes}")
        print(f"Modo: {img.modo}")
        print(f"Tamanho (bytes): {img.tamanho}")
        print(
            f"Data de modificação: "
            f"{img.data_mod.strftime('%d/%m/%Y %H:%M:%S')}"
        )
        if img.data_exif:
            print(
                f"Data EXIF: "
                f"{img.data_exif.strftime('%d/%m/%Y %H:%M:%S')}"
            )
        print(f"Mês do bebê: {mes_bebe:02d}")
        print("-" * 40)
    
    # Procura por duplicatas
    duplicadas = encontrar_duplicadas(imagens)
    if duplicadas:
        # Primeiro simula para mostrar as mudanças
        mover_duplicadas(duplicadas, diretorio, simular=True)
        
        if input(
            "\nDeseja mover as duplicatas para a pasta 'duplicadas'? (s/N): "
        ).lower() == 's':
            mover_duplicadas(duplicadas, diretorio, simular=False)
    
    if renomear and imagens:  # Só renomeia se há imagens não organizadas
        # Solicita informações sobre eventos
        eventos = solicitar_eventos()
        
        # Primeiro simula para mostrar as mudanças
        renomear_imagens(imagens, diretorio, eventos, simular=True)
        
        if input("\nConfirma as alterações? (s/N): ").lower() == 's':
            renomear_imagens(imagens, diretorio, eventos, simular=False)
            
            # Se foram adicionados eventos, oferece organização por pastas
            if eventos:
                print("\n🎉 EVENTOS DETECTADOS NA RENOMEAÇÃO!")
                print("💡 Quer organizar as fotos em pastas por evento?")
                
                if input("\n📁 Organizar por pastas de eventos? (s/N): ").lower() == 's':
                    # Recarrega as imagens para detectar os novos eventos
                    imagens_atualizadas = []
                    for arquivo in os.listdir(diretorio):
                        caminho = os.path.join(diretorio, arquivo)
                        if os.path.isfile(caminho):
                            info = get_info_imagem(caminho)
                            if info:
                                imagens_atualizadas.append(info)
                    
                    eventos_detectados = detectar_eventos_nos_arquivos(imagens_atualizadas)
                    if eventos_detectados:
                        organizar_por_pastas_evento(diretorio, eventos_detectados, simular=True)
                        if input("\n❓ Confirma a organização? (s/N): ").lower() == 's':
                            backup_file = criar_backup_operacao(diretorio, "organizar_pos_renomeacao")
                            print(f"💾 Backup criado: {os.path.basename(backup_file)}")
                            organizar_por_pastas_evento(diretorio, eventos_detectados, simular=False)
    elif renomear and not imagens:
        print("\n✅ Nenhuma imagem precisa ser renomeada!")


def exibir_menu_inicial():
    """Exibe um menu inicial bonito e retorna as opções escolhidas."""
    print("=" * 70)
    print("🖼️  ORGANIZADOR DE FOTOS - MARIA ANTÔNIA  🖼️")
    print("=" * 70)
    print()
    print("📋 FUNCIONALIDADES DISPONÍVEIS:")
    print("   1️⃣  Analisar e listar imagens")
    print("   2️⃣  Detectar e mover duplicatas") 
    print("   3️⃣  Renomear imagens por data")
    print("   4️⃣  Fazer tudo (análise + duplicatas + renomeação)")
    print("   5️⃣  Relatório detalhado")
    print("   6️⃣  Buscar fotos por período")
    print("   7️⃣  Organizar por pastas de eventos")
    print("   8️⃣  Organizar por anos do bebê")
    print("   9️⃣  Criar backup do estado atual")
    print()
    print("🎯 FORMATO DE NOMENCLATURA:")
    print("   📅 MM - IMG DDMMAAAA(XX) [- evento]")
    print("   📝 Onde: MM=mês do bebê, DD/MM/AAAA=data, XX=sequencial")
    print("   🗓️ Organização automática por anos a partir de 01/01/2025")
    print()
    print("=" * 70)
    
    while True:
        try:
            opcao = input("\n🔢 Escolha uma opção (1-9): ").strip()
            if opcao in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return int(opcao)
            else:
                print("❌ Opção inválida! Digite 1, 2, 3, 4, 5, 6, 7, 8 ou 9.")
        except KeyboardInterrupt:
            print("\n\n👋 Operação cancelada pelo usuário.")
            exit(0)


def solicitar_diretorio():
    """Solicita o diretório das fotos."""
    print("\n📁 CONFIGURAÇÃO DO DIRETÓRIO:")
    
    while True:
        caminho = input("📁 Digite o caminho do diretório: ").strip()
        if caminho and os.path.exists(caminho):
            return caminho
        elif not caminho:
            print("❌ Por favor, digite um caminho válido!")
        else:
            print("❌ Diretório não encontrado! Tente novamente.")


def executar_opcao(opcao: int, diretorio: str):
    """Executa a opção escolhida pelo usuário."""
    print("\n" + "=" * 70)
    
    # Coleta imagens uma vez para usar em várias opções
    imagens_todas = []
    imagens_nao_organizadas = []
    
    for arquivo in os.listdir(diretorio):
        caminho = os.path.join(diretorio, arquivo)
        if os.path.isfile(caminho):
            info = get_info_imagem(caminho)
            if info:
                imagens_todas.append(info)
                if not esta_organizada(info.arquivo):
                    imagens_nao_organizadas.append(info)
    
    if opcao == 1:
        print("📊 ANALISANDO IMAGENS...")
        ler_dados_imagens(diretorio, renomear=False)
        
    elif opcao == 2:
        print("🔍 DETECTANDO E MOVENDO DUPLICATAS...")
        duplicadas = encontrar_duplicadas(imagens_todas)
        if duplicadas:
            mover_duplicadas(duplicadas, diretorio, simular=True)
            if input("\n❓ Confirma mover duplicatas? (s/N): ").lower() == 's':
                # Cria backup antes da operação
                backup_file = criar_backup_operacao(diretorio, "mover_duplicatas")
                print(f"💾 Backup criado: {os.path.basename(backup_file)}")
                mover_duplicadas(duplicadas, diretorio, simular=False)
        else:
            print("✅ Nenhuma duplicata encontrada!")
            
    elif opcao == 3:
        print("📝 RENOMEANDO IMAGENS...")
        if imagens_nao_organizadas:
            # Cria backup antes da operação
            backup_file = criar_backup_operacao(diretorio, "renomear_imagens")
            print(f"💾 Backup criado: {os.path.basename(backup_file)}")
        ler_dados_imagens(diretorio, renomear=True)
        
    elif opcao == 4:
        print("🚀 EXECUTANDO PROCESSO COMPLETO...")
        # Cria backup antes da operação
        backup_file = criar_backup_operacao(diretorio, "processo_completo")
        print(f"💾 Backup criado: {os.path.basename(backup_file)}")
        ler_dados_imagens(diretorio, renomear=True)
        
    elif opcao == 5:
        print("📊 GERANDO RELATÓRIO DETALHADO...")
        gerar_relatorio_detalhado(imagens_todas)
        
    elif opcao == 6:
        print("🔍 BUSCAR FOTOS POR PERÍODO...")
        print("📅 Digite o período desejado:")
        data_inicio = input("   📆 Data início (DD/MM/AAAA): ").strip()
        data_fim = input("   📆 Data fim (DD/MM/AAAA): ").strip()
        
        fotos_periodo = buscar_fotos_periodo(imagens_todas, data_inicio, data_fim)
        
        if fotos_periodo:
            print(f"\n📋 ENCONTRADAS {len(fotos_periodo)} FOTOS NO PERÍODO:")
            print("─" * 50)
            for img in fotos_periodo:
                data = img.data_exif or img.data_mod
                mes_bebe = calcular_mes_bebe(data)
                print(f"📷 {img.arquivo}")
                print(f"   📅 Data: {data.strftime('%d/%m/%Y %H:%M')}")
                print(f"   👶 Mês do bebê: {mes_bebe:02d}")
                print(f"   📏 Dimensões: {img.dimensoes}")
                print()
        else:
            print("❌ Nenhuma foto encontrada no período especificado.")
            
    elif opcao == 7:
        print("� ORGANIZANDO POR PASTAS DE EVENTOS...")
        eventos_detectados = detectar_eventos_nos_arquivos(imagens_todas)
        
        if eventos_detectados:
            print(f"\n🎉 EVENTOS DETECTADOS ({len(eventos_detectados)}):")
            for evento, arquivos in eventos_detectados.items():
                print(f"   📂 {evento}: {len(arquivos)} arquivo(s)")
            
            # Mostra a simulação
            organizar_por_pastas_evento(diretorio, eventos_detectados, simular=True)
            
            # Pergunta se quer prosseguir
            resposta = input("\n❓ Confirma a organização por pastas? (s/N): ").lower()
            if resposta == 's':
                # Cria backup antes da operação
                backup_file = criar_backup_operacao(diretorio, "organizar_pastas")
                print(f"💾 Backup criado: {os.path.basename(backup_file)}")
                organizar_por_pastas_evento(diretorio, eventos_detectados, simular=False)
        else:
            print("📋 Nenhum evento detectado nos nomes dos arquivos.")
            print("💡 Dica: Adicione eventos aos nomes usando a opção de renomeação.")
            
    elif opcao == 8:
        print("�💾 CRIANDO BACKUP DO ESTADO ATUAL...")
        backup_file = criar_backup_operacao(diretorio, "backup_manual")
        print("✅ Backup criado com sucesso!")
        print(f"📁 Arquivo: {backup_file}")
        print(f"📊 {len(imagens_todas)} imagens registradas no backup.")
    
    print("\n" + "=" * 70)
    print("✅ OPERAÇÃO CONCLUÍDA!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        opcao = exibir_menu_inicial()
        diretorio = solicitar_diretorio()
        executar_opcao(opcao, diretorio)
    except KeyboardInterrupt:
        print("\n\n👋 Programa encerrado pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("🔧 Verifique o diretório e tente novamente.")
