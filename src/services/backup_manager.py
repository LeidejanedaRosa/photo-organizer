import os
import json
from datetime import datetime
from typing import List

from ..domain.image import ImageInfo


class BackupManager:
    """Responsável por criar backups das operações."""
    
    def create_backup(self, diretorio: str, operacao: str) -> str:
        """
        Cria um backup/log das operações realizadas.
        
        Args:
            diretorio: Diretório das imagens
            operacao: Nome da operação sendo executada
            
        Returns:
            Caminho do arquivo de backup criado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(diretorio, "backups")
        
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        backup_file = os.path.join(
            backup_dir, f"backup_{operacao}_{timestamp}.json"
        )
        
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
