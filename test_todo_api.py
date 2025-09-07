import requests
import json

def test_todo_api():
    try:
        url = "http://localhost:8000/api/notes/extract-todos"
        headers = {"Content-Type": "application/json"}
        data = {
            "content": "Yarın sunum dosyasını tamamla ve Ali'ye gönder"
        }
        
        print("Todo Extraction API test ediliyor...")
        print(f"URL: {url}")
        print(f"Data: {data}")
        
        response = requests.post(url, headers=headers, json=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API başarılı!")
            print(f"Yapılacak iş var mı: {result.get('hasTodos', 'N/A')}")
            print(f"Yapılacak işler: {result.get('todos', 'N/A')}")
        else:
            print("❌ API hatası!")
            
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_todo_api()
