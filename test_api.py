import requests
import json

def test_api():
    try:
        url = "http://localhost:8000/api/notes/summarize"
        headers = {"Content-Type": "application/json"}
        data = {
            "content": "Bu bir test notudur. Flutter ile mobil uygulama geliştirme hakkında bilgiler içeriyor. AI özetleme özelliği test ediliyor."
        }
        
        print("API test ediliyor...")
        print(f"URL: {url}")
        print(f"Data: {data}")
        
        response = requests.post(url, headers=headers, json=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API başarılı!")
            print(f"Özet: {result.get('summary', 'N/A')}")
            print(f"Anahtar noktalar: {result.get('keyPoints', 'N/A')}")
        else:
            print("❌ API hatası!")
            
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api()
