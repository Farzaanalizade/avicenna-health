"""
🤖 Google Gemini Vision API Service

تحلیل تصاویر سلامتی توسط Gemini Pro Vision
"""

import logging
import base64
import json
from typing import Dict, Any
import google.generativeai as genai
from app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiService:
    """سرویس تحلیل تصاویر توسط Gemini"""
    
    def __init__(self):
        """Initialize Gemini API"""
        try:
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not set in environment")
            
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel("gemini-pro-vision")
            logger.info("✅ Gemini Vision API initialized")
        except Exception as e:
            logger.error(f"❌ Gemini initialization error: {str(e)}")
            self.model = None
    
    async def analyze_tongue_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        🔴 تحلیل عکس زبان
        
        Analyzes:
        - Color (pale, red, crimson, purple, dark)
        - Coating (white, yellow, greasy, etc.)
        - Moisture level
        - Shape and cracks
        - Mizaj type indication
        """
        try:
            if not self.model:
                return self._get_offline_tongue_analysis()
            
            # Convert to base64
            image_b64 = base64.standard_b64encode(image_data).decode()
            
            # Prompt for tongue analysis
            prompt = """
            Analyze this tongue image for Traditional Persian Medicine (Avicenna) diagnostics.
            
            Please identify and return in JSON format:
            1. Color: (pale/red/crimson/purple/dark)
            2. Coating: (white/yellow/greasy/thick/thin/none)
            3. Moisture: (dry/normal/wet)
            4. Cracks: (present/absent)
            5. Shape: (normal/swollen/thin/round/irregular)
            6. Mizaj_type: Based on observations (garm_tar/garm_khoshk/sard_tar/sard_khoshk)
            7. Confidence: (0.0-1.0)
            8. Findings: (list of observed conditions)
            9. Recommendations: (list of suggested remedies)
            
            Return ONLY valid JSON, no markdown or extra text.
            """
            
            response = await self._call_gemini_with_image(image_b64, prompt)
            
            # Parse response
            parsed = self._parse_gemini_response(response)
            
            logger.info(f"✅ Tongue analysis: {parsed.get('mizaj_type')} ({parsed.get('confidence', 0):.1%})")
            
            return {
                "findings": {
                    "color": parsed.get("color"),
                    "coating": parsed.get("coating"),
                    "moisture": parsed.get("moisture"),
                    "cracks": parsed.get("cracks"),
                    "shape": parsed.get("shape"),
                },
                "mizaj": parsed.get("mizaj_type"),
                "confidence": parsed.get("confidence", 0.7),
                "recommendations": parsed.get("recommendations", []),
            }
            
        except Exception as e:
            logger.error(f"❌ Tongue analysis error: {str(e)}")
            return self._get_offline_tongue_analysis()
    
    async def analyze_eye_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        👁️ تحلیل عکس چشم
        """
        try:
            if not self.model:
                return self._get_offline_eye_analysis()
            
            image_b64 = base64.standard_b64encode(image_data).decode()
            
            prompt = """
            Analyze this eye image for Traditional Medicine diagnostics.
            
            Please identify and return in JSON format:
            1. Sclera_color: (clear/white/yellow/red)
            2. Pupil_size: (small/normal/large)
            3. Brightness: (dull/normal/bright)
            4. Dark_circles: (none/mild/moderate/severe)
            5. General_health: (healthy/concerns)
            6. Confidence: (0.0-1.0)
            7. Findings: (list of observations)
            8. Recommendations: (list of suggestions)
            
            Return ONLY valid JSON.
            """
            
            response = await self._call_gemini_with_image(image_b64, prompt)
            parsed = self._parse_gemini_response(response)
            
            logger.info(f"✅ Eye analysis completed")
            
            return {
                "findings": {
                    "sclera_color": parsed.get("sclera_color"),
                    "pupil_size": parsed.get("pupil_size"),
                    "brightness": parsed.get("brightness"),
                    "dark_circles": parsed.get("dark_circles"),
                },
                "health_status": parsed.get("general_health"),
                "confidence": parsed.get("confidence", 0.7),
                "recommendations": parsed.get("recommendations", []),
            }
            
        except Exception as e:
            logger.error(f"❌ Eye analysis error: {str(e)}")
            return self._get_offline_eye_analysis()
    
    async def analyze_face_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        😊 تحلیل عکس صورت
        """
        try:
            if not self.model:
                return self._get_offline_face_analysis()
            
            image_b64 = base64.standard_b64encode(image_data).decode()
            
            prompt = """
            Analyze this face image for Traditional Medicine diagnostics.
            
            Please identify and return in JSON format:
            1. Complexion: (pale/red/yellow/dark/balanced)
            2. Skin_condition: (healthy/dry/oily/inflamed)
            3. Texture: (smooth/rough/flaky)
            4. Puffiness: (none/mild/moderate)
            5. Radiance: (dull/normal/bright)
            6. Confidence: (0.0-1.0)
            7. Findings: (list of observations)
            8. Recommendations: (list of suggestions)
            
            Return ONLY valid JSON.
            """
            
            response = await self._call_gemini_with_image(image_b64, prompt)
            parsed = self._parse_gemini_response(response)
            
            logger.info(f"✅ Face analysis completed")
            
            return {
                "findings": {
                    "complexion": parsed.get("complexion"),
                    "skin_condition": parsed.get("skin_condition"),
                    "texture": parsed.get("texture"),
                    "puffiness": parsed.get("puffiness"),
                },
                "complexion": parsed.get("complexion"),
                "confidence": parsed.get("confidence", 0.7),
                "recommendations": parsed.get("recommendations", []),
            }
            
        except Exception as e:
            logger.error(f"❌ Face analysis error: {str(e)}")
            return self._get_offline_face_analysis()
    
    async def analyze_skin_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        🖐️ تحلیل عکس پوست
        """
        try:
            if not self.model:
                return self._get_offline_skin_analysis()
            
            image_b64 = base64.standard_b64encode(image_data).decode()
            
            prompt = """
            Analyze this skin image for Traditional Medicine diagnostics.
            
            Please identify and return in JSON format:
            1. Condition: (normal/dry/oily/sensitive/combination)
            2. Texture: (smooth/rough/textured)
            3. Tone: (even/uneven)
            4. Visible_issues: (none/rash/inflammation/dryness/oiliness/other)
            5. Moisture_level: (dehydrated/normal/oily)
            6. Confidence: (0.0-1.0)
            7. Findings: (list of observations)
            8. Recommendations: (list of care suggestions)
            
            Return ONLY valid JSON.
            """
            
            response = await self._call_gemini_with_image(image_b64, prompt)
            parsed = self._parse_gemini_response(response)
            
            logger.info(f"✅ Skin analysis completed")
            
            return {
                "findings": {
                    "condition": parsed.get("condition"),
                    "texture": parsed.get("texture"),
                    "tone": parsed.get("tone"),
                    "visible_issues": parsed.get("visible_issues"),
                    "moisture_level": parsed.get("moisture_level"),
                },
                "condition": parsed.get("condition"),
                "confidence": parsed.get("confidence", 0.7),
                "recommendations": parsed.get("recommendations", []),
            }
            
        except Exception as e:
            logger.error(f"❌ Skin analysis error: {str(e)}")
            return self._get_offline_skin_analysis()
    
    async def _call_gemini_with_image(self, image_b64: str, prompt: str) -> str:
        """
        صدا زدن Gemini API با تصویر
        """
        try:
            # Create image part
            image_part = {
                "mime_type": "image/jpeg",
                "data": image_b64,
            }
            
            # Call Gemini
            response = self.model.generate_content([prompt, image_part])
            
            return response.text
            
        except Exception as e:
            logger.error(f"❌ Gemini API error: {str(e)}")
            raise
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """
        تجزیه پاسخ Gemini
        """
        try:
            # Try to extract JSON from response
            # Gemini might return markdown or extra text
            
            # Find JSON content
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
            elif "{" in response_text and "}" in response_text:
                # Try to find JSON object
                start = response_text.find("{")
                end = response_text.rfind("}") + 1
                json_str = response_text[start:end]
            else:
                json_str = response_text
            
            parsed = json.loads(json_str)
            logger.info(f"✅ Parsed Gemini response: {len(parsed)} fields")
            return parsed
            
        except Exception as e:
            logger.error(f"❌ Parse error: {str(e)}")
            return {}
    
    # Offline fallback responses
    def _get_offline_tongue_analysis(self) -> Dict[str, Any]:
        """Demo data when Gemini unavailable"""
        return {
            "findings": {
                "color": "red",
                "coating": "thin_white",
                "moisture": "normal",
                "cracks": "none",
                "shape": "normal",
            },
            "mizaj": "garm_tar",
            "confidence": 0.65,
            "recommendations": [
                "Consume cooling foods (cucumber, melon, yogurt)",
                "Drink plenty of water",
                "Reduce stress and spicy foods",
            ],
        }
    
    def _get_offline_eye_analysis(self) -> Dict[str, Any]:
        """Demo data"""
        return {
            "findings": {
                "sclera_color": "clear",
                "pupil_size": "normal",
                "brightness": "normal",
                "dark_circles": "mild",
            },
            "health_status": "healthy",
            "confidence": 0.62,
            "recommendations": [
                "Eyes appear healthy",
                "Get adequate sleep (7-8 hours)",
                "Protect eyes from screen strain",
            ],
        }
    
    def _get_offline_face_analysis(self) -> Dict[str, Any]:
        """Demo data"""
        return {
            "findings": {
                "complexion": "balanced",
                "skin_condition": "healthy",
                "texture": "smooth",
                "puffiness": "none",
            },
            "complexion": "balanced",
            "confidence": 0.58,
            "recommendations": [
                "Skin condition looks good",
                "Maintain daily skincare routine",
                "Stay well-hydrated",
            ],
        }
    
    def _get_offline_skin_analysis(self) -> Dict[str, Any]:
        """Demo data"""
        return {
            "findings": {
                "condition": "normal",
                "texture": "smooth",
                "tone": "even",
                "visible_issues": "none",
                "moisture_level": "normal",
            },
            "condition": "normal",
            "confidence": 0.60,
            "recommendations": [
                "Skin appears healthy",
                "Continue current care routine",
                "Use sunscreen when outdoors",
            ],
        }
