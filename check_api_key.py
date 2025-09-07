import requests
import os
from config import OPENAI_API_KEY

def check_openai_api_key():
    """OpenAI API anahtarının durumunu kontrol eder"""
    
    print(f"API Key (ilk 10 karakter): {OPENAI_API_KEY[:10]}...")
    
    # OpenAI API usage endpoint'ini kontrol et
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Usage endpoint'ini dene
        response = requests.get(
            "https://api.openai.com/v1/usage",
            headers=headers,
            timeout=10
        )
        
        print(f"Usage API Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ API anahtarı çalışıyor!")
            print(f"Response: {response.text}")
        else:
            print(f"❌ API anahtarı sorunu: {response.text}")
            
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
    
    # Basit bir test isteği yap
    try:
        test_payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Merhaba"}],
            "max_tokens": 10
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=test_payload,
            timeout=10
        )
        
        print(f"\nTest API Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Test isteği başarılı!")
        else:
            print(f"❌ Test isteği başarısız: {response.text}")
            
    except Exception as e:
        print(f"❌ Test isteği hatası: {e}")

if __name__ == "__main__":
    check_openai_api_key()
