from datetime import datetime
from typing import Dict


class EventManager:
    """Responsável por gerenciar eventos de fotos."""
    
    @staticmethod
    def solicitar_eventos() -> Dict[str, str]:
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
