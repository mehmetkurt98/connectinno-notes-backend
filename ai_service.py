import os
import json
import asyncio
import google.generativeai as genai
from typing import Dict, List
from config import GEMINI_API_KEY

class AIService:
    def __init__(self):
        if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            raise ValueError("GEMINI_API_KEY is not set in environment variables")
        
        # Gemini API'yi yapılandır
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def summarize_note(self, content: str) -> Dict:
        """
        Not içeriğini Gemini AI ile özetler ve anahtar noktaları çıkarır
        """
        try:
            # İçerik uzunluğunu kontrol et
            word_count = len(content.split())
            
            if word_count < 3:
                return {
                    "summary": "İçerik çok kısa, özetleme için yeterli değil.",
                    "keyPoints": [],
                    "wordCount": word_count,
                    "originalWordCount": word_count
                }
            
            # Gemini'ye gönderilecek prompt
            prompt = f"""
            Aşağıdaki not içeriğini Türkçe olarak özetleyin ve anahtar noktaları çıkarın.
            
            İçerik:
            {content}
            
            Lütfen şu formatta yanıt verin:
            1. Özet: (2-3 cümlelik kısa özet)
            2. Anahtar Noktalar: (Her biri bir satırda, maksimum 5 adet)
            
            Özet kısa ve öz olsun, anahtar noktalar ise madde madde listelensin.
            """
            
            # Gemini API çağrısı
            try:
                response = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: self.model.generate_content(prompt)
                )
                
                ai_response = response.text
                
            except Exception as e:
                raise Exception(f"Gemini API error: {str(e)}")
            
            # AI yanıtını parse et
            summary, key_points = self._parse_ai_response(ai_response)
            
            return {
                "summary": summary,
                "keyPoints": key_points,
                "wordCount": len(summary.split()),
                "originalWordCount": word_count
            }
            
        except asyncio.TimeoutError:
            # Timeout durumunda basit özet döndür
            word_count = len(content.split())
            simple_summary = content[:200] + "..." if len(content) > 200 else content
            
            return {
                "summary": f"AI özetleme zaman aşımına uğradı. İçeriğin ilk 200 karakteri: {simple_summary}",
                "keyPoints": [],
                "wordCount": len(simple_summary.split()),
                "originalWordCount": word_count
            }
        except Exception as e:
            # Hata durumunda basit özet döndür
            word_count = len(content.split())
            simple_summary = content[:200] + "..." if len(content) > 200 else content
            
            return {
                "summary": f"AI özetleme hatası: {str(e)}. İçeriğin ilk 200 karakteri: {simple_summary}",
                "keyPoints": [],
                "wordCount": len(simple_summary.split()),
                "originalWordCount": word_count
            }
    
    def _parse_ai_response(self, response: str) -> tuple[str, List[str]]:
        """
        AI yanıtını parse eder ve özet ile anahtar noktaları ayırır
        """
        try:
            lines = response.strip().split('\n')
            summary = ""
            key_points = []
            
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if "özet:" in line.lower() or "summary:" in line.lower():
                    current_section = "summary"
                    # Özet kısmını al
                    summary_text = line.split(':', 1)[1].strip() if ':' in line else ""
                    if summary_text:
                        summary = summary_text
                elif "anahtar" in line.lower() or "key" in line.lower() or "nokta" in line.lower():
                    current_section = "key_points"
                elif current_section == "summary" and not summary:
                    summary = line
                elif current_section == "key_points" or (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                    # Anahtar nokta
                    point = line.lstrip('-•* ').strip()
                    if point and len(key_points) < 5:  # Maksimum 5 anahtar nokta
                        key_points.append(point)
                elif current_section == "summary" and summary:
                    # Özet devam ediyor
                    summary += " " + line
            
            # Eğer parse edilemediyse, basit özet oluştur
            if not summary:
                summary = response[:200] + "..." if len(response) > 200 else response
            
            return summary, key_points
            
        except Exception:
            # Parse hatası durumunda basit döndür
            return response[:200] + "..." if len(response) > 200 else response, []

    async def extract_todos(self, content: str) -> Dict:
        """
        Not içeriğinden yapılacak işleri (todo'ları) çıkarır
        """
        try:
            # İçerik uzunluğunu kontrol et
            word_count = len(content.split())
            
            if word_count < 3:
                return {
                    "hasTodos": False,
                    "todos": [],
                    "originalContent": content
                }
            
            # Gemini'ye gönderilecek prompt
            prompt = f"""
            Aşağıdaki metni analiz et ve yapılacak işleri (todo'ları) çıkar.
            
            Metin:
            {content}
            
            Lütfen şu formatta yanıt ver:
            1. Eğer yapılacak iş varsa: "TODOS:" yaz ve her birini ayrı satırda listele
            2. Eğer yapılacak iş yoksa: "NO_TODOS" yaz
            
            Örnek:
            "Yarın sunum dosyasını tamamla ve Ali'ye gönder"
            TODOS:
            - Sunum dosyasını tamamla
            - Ali'ye gönder
            
            Sadece yapılacak işleri çıkar, geçmiş olayları değil.
            """
            
            # Gemini API çağrısı
            try:
                response = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: self.model.generate_content(prompt)
                )
                
                ai_response = response.text
                
            except Exception as e:
                raise Exception(f"Gemini API error: {str(e)}")
            
            # AI yanıtını parse et
            todos = self._parse_todos_response(ai_response)
            
            return {
                "hasTodos": len(todos) > 0,
                "todos": todos,
                "originalContent": content
            }
            
        except Exception as e:
            # Hata durumunda boş döndür
            return {
                "hasTodos": False,
                "todos": [],
                "originalContent": content
            }
    
    def _parse_todos_response(self, response: str) -> List[str]:
        """
        AI yanıtından todo'ları parse eder
        """
        try:
            lines = response.strip().split('\n')
            todos = []
            
            in_todos_section = False
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if "TODOS:" in line.upper():
                    in_todos_section = True
                    continue
                elif "NO_TODOS" in line.upper():
                    break
                elif in_todos_section:
                    # Todo satırı
                    if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                        todo = line.lstrip('-•* ').strip()
                        if todo:
                            todos.append(todo)
                    elif line and not line.startswith('TODOS:'):
                        # Satır başında işaret yoksa da todo olabilir
                        todos.append(line)
            
            return todos
            
        except Exception:
            return []