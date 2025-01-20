import shodan

def получить_ключ():
    print("=" * 50)
    print("1. Зарегистрируйтесь на Shodan.io")
    print("2. В личном кабинете найдите свой API-ключ")
    print("=" * 50)
    return input("Введите ваш Shodan API-ключ: ").strip()

def создать_запрос():
    страна = input("Страна (например, RU/US/CN или Enter для всех): ") 
    порт = input("Порт (по умолчанию 554): ") or "554"
    фильтр = input("Фильтр (rtsp/webcam/dvr или Enter): ") or "rtsp"
    return f"{фильтр} port:{порт} country:{страна}" if страна else f"{фильтр} port:{порт}"

def main():
    api_key = получить_ключ()
    if not api_key:
        print("[!] API-ключ обязателен!")
        return

    try:
        api = shodan.Shodan(api_key)
        запрос = создать_запрос()
        print(f"\n[+] Идёт сканирование: {запрос}...")
        результаты = api.search(запрос)
        
        for dev in результаты['matches']:
            print("\n" + "-" * 40)
            print(f"IP: {dev['ip_str']}:{dev['port']}")
            print(f"Организация: {dev.get('org', 'N/A')}")
            print(f"RTSP: rtsp://{dev['ip_str']}:{dev['port']}/live")
            
    except shodan.APIError as e:
        print(f"[!] Ошибка Shodan: {e}")
    except Exception as e:
        print(f"[!] Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
