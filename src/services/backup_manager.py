import json
import os
from datetime import datetime


class BackupManager:
    def create_backup(self, directory: str, operacao: str) -> str:

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(directory, "backups")

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        backup_file = os.path.join(
            backup_dir, f"backup_{operacao}_{timestamp}.json"
        )

        current_files = []
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            if os.path.isfile(path) and not file.endswith(".json"):
                try:
                    stat = os.stat(path)
                    current_files.append(
                        {
                            "nome": file,
                            "tamanho": stat.st_size,
                            "modificado": datetime.fromtimestamp(
                                stat.st_mtime
                            ).isoformat(),
                        }
                    )
                except (OSError, IOError):
                    continue

        backup_data = {
            "operacao": operacao,
            "timestamp": timestamp,
            "directory": directory,
            "arquivos": current_files,
        }

        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)

        return backup_file
