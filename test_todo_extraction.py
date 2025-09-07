import asyncio
from ai_service import AIService

async def test_todo_extraction():
    try:
        print("AI Todo Extraction test ediliyor...")
        ai_service = AIService()
        print("✅ AI Service başarıyla oluşturuldu")
        
        # Test içerikleri
        test_contents = [
            "Yarın sunum dosyasını tamamla ve Ali'ye gönder",
            "Bugün markete git, süt al ve ekmek al",
            "Bu hafta proje raporunu hazırla, toplantıya katıl",
            "Merhaba, nasılsın?",
            "Dün sinemaya gittim, çok güzeldi"
        ]
        
        for i, content in enumerate(test_contents, 1):
            print(f"\n--- Test {i} ---")
            print(f"İçerik: {content}")
            
            result = await ai_service.extract_todos(content)
            
            print(f"Yapılacak iş var mı: {result['hasTodos']}")
            if result['hasTodos']:
                print("Yapılacak işler:")
                for j, todo in enumerate(result['todos'], 1):
                    print(f"  {j}. {todo}")
            else:
                print("Yapılacak iş bulunamadı")
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_todo_extraction())
