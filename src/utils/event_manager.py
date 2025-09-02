from datetime import datetime
from typing import Dict

class EventManager:
    
    @staticmethod
    def request_events() -> Dict[str, str]:
        
        events = {}
        print("\n" + "─" * 50)
        print("🎉 CONFIGURAÇÃO DE EVENTOS")
        print("─" * 50)
        print("📝 Defina events especiais para as datas das fotos.")
        print("💡 Formato da date: DD/MM/AAAA")
        print("🔚 Para finalizar: deixe a date em branco e pressione Enter")
        print("─" * 50)
        
        counter = 1
        while True:
            date = input(f"\n📅 Data do evento #{counter} (DD/MM/AAAA): ").strip()
            if not date:
                break
                
            try:
                date_obj = datetime.strptime(date, '%d/%m/%Y')
                date_fmt = date_obj.strftime('%d%m%Y')
                description = input("🏷️  Descrição do evento: ").strip()
                if description:
                    events[date_fmt] = description
                    print(f"✅ Evento registrado: {date} - {description}")
                    counter += 1
            except ValueError:
                print("❌ Data inválida! Use o formato DD/MM/AAAA")
        
        if events:
            print(f"\n🎊 {len(events)} evento(s) configurado(s) com sucesso!")
        else:
            print("\n📝 Nenhum evento configurado.")
        
        return events