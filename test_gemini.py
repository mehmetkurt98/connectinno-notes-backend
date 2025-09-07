import asyncio
from ai_service import AIService

async def test_gemini():
    try:
        print("Gemini AI Service test ediliyor...")
        ai_service = AIService()
        print("✅ AI Service başarıyla oluşturuldu")
        
        # Test içeriği
        test_content = "Bu bir test notudur. Flutter ile mobil uygulama geliştirme hakkında bilgiler içeriyor. AI özetleme özelliği test ediliyor."
        
        print("AI özetleme test ediliyor...")
        result = await ai_service.summarize_note(test_content)
        
        print("✅ AI özetleme başarılı!")
        print(f"Özet: {result['summary']}")
        print(f"Anahtar noktalar: {result['keyPoints']}")
        print(f"Kelime sayısı: {result['wordCount']}")
        print(f"Orijinal kelime sayısı: {result['originalWordCount']}")
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gemini())
