import shodan
import time
import requests

def bypass_403(api_key, query, retries=3, delay=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", 
        "Authorization": f"Shodan {api_key}"
    }
    
    for _ in range(retries):
        try:
            response = requests.get(
                f"https://api.shodan.io/shodan/host/search?query={query}&key={api_key}",
                headers=headers,
                timeout=15
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                print(f"[!] 403 Forbidden. Попытка {_+1}/{retries}...")
                time.sleep(delay)
        except Exception as e:
            print(f"[!] Ошибка: {e}")
    return None

def main():
    api_key = input("API-ключ Shodan: ").strip()
    query = input("Фильтр (например, 'rtsp'): ").strip() or "rtsp"
    
    data = bypass_403(api_key, query)
    
    if not data:
        print("[!] Ошибка 403: доступ запрещён. Решения:")
        print("- Проверьте API-ключ в [Shodan Dashboard](https://developer.shodan.io/dashboard)")
        print("- Смените IP-адрес (используйте VPN/прокси)")
        print("- Купите премиум-аккаунт Shodan")
        return
    
    print(f"\n[+] Устройств найдено: {data.get('total', 0)}")
    for result in data.get('matches', []):
        print(f"\nIP: {result['ip_str']}:{result['port']}")
        print(f"RTSP: rtsp://{result['ip_str']}:{result['port']}/live")

if __name__ == "__main__":
    main()
