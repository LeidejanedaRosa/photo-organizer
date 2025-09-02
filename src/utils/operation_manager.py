from typing import Any, Callable

from ..services.backup_manager import BackupManager


class OperationManager:

    def __init__(self, backup_manager: BackupManager):
        self.backup_manager = backup_manager

    def execute_with_backup(
        self,
        operation: Callable[..., Any],
        directory: str,
        operation_name: str,
        should_backup: bool = True,
        *args,
        **kwargs,
    ) -> Any:

        simulate = kwargs.get("simulate", True)

        if should_backup and not simulate:
            backup_file = self.backup_manager.create_backup(
                directory, operation_name
            )
            print(f"💾 Backup criado: {backup_file}")

        return operation(*args, **kwargs)
