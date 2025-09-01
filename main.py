#!/usr/bin/env python3
"""
Organizador de Fotos
Versão refatorada seguindo princípios SOLID e Clean Code

Este arquivo é o ponto de entrada da aplicação.
Toda a lógica foi distribuída em módulos específicos seguindo
o princípio de Responsabilidade Única.
"""

from src.cli.photo_organizer_cli import PhotoOrganizerCLI


def main():
    """Função principal da aplicação."""
    app = PhotoOrganizerCLI()
    app.run()


if __name__ == "__main__":
    main()
