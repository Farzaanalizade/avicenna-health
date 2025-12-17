"""
Internationalization (i18n) service for FastAPI
Provides translation support for Persian, English, and Arabic
"""

import json
import logging
from typing import Optional, Dict, Any
from pathlib import Path
from functools import lru_cache

logger = logging.getLogger(__name__)

class I18nService:
    """Internationalization service for multi-language support"""
    
    SUPPORTED_LANGUAGES = ["fa", "en", "ar"]
    DEFAULT_LANGUAGE = "en"
    
    def __init__(self, translations_dir: str = "backend/translations"):
        """
        Initialize i18n service
        
        Args:
            translations_dir: Directory containing translation JSON files
        """
        self.translations_dir = Path(translations_dir)
        self.translations: Dict[str, Dict[str, Any]] = {}
        self._load_translations()
    
    def _load_translations(self):
        """Load all translation files"""
        for lang in self.SUPPORTED_LANGUAGES:
            try:
                file_path = self.translations_dir / f"{lang}.json"
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.translations[lang] = json.load(f)
                    logger.info(f"✓ Loaded {lang} translations")
                else:
                    logger.warning(f"⚠ Translation file not found: {file_path}")
            except Exception as e:
                logger.error(f"Error loading {lang} translations: {e}")
    
    def translate(self, key: str, language: str = None, **kwargs) -> str:
        """
        Get translated string
        
        Args:
            key: Translation key (dot notation, e.g., "auth.login")
            language: Target language (fa, en, ar)
            **kwargs: Format arguments for string interpolation
        
        Returns:
            Translated string or original key if not found
        """
        if language is None:
            language = self.DEFAULT_LANGUAGE
        
        if language not in self.SUPPORTED_LANGUAGES:
            language = self.DEFAULT_LANGUAGE
        
        try:
            # Navigate nested keys
            translation_dict = self.translations.get(language, {})
            for part in key.split('.'):
                translation_dict = translation_dict.get(part, {})
            
            if isinstance(translation_dict, str):
                # Format string if kwargs provided
                if kwargs:
                    return translation_dict.format(**kwargs)
                return translation_dict
            
            return key  # Return key if not found
        except Exception as e:
            logger.error(f"Translation error for key {key}: {e}")
            return key
    
    def get_translations(self, language: str = None) -> Dict[str, Any]:
        """
        Get all translations for a language
        
        Args:
            language: Target language
        
        Returns:
            Full translation dictionary
        """
        if language is None:
            language = self.DEFAULT_LANGUAGE
        
        if language not in self.SUPPORTED_LANGUAGES:
            language = self.DEFAULT_LANGUAGE
        
        return self.translations.get(language, {})
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get list of supported languages
        
        Returns:
            Dictionary with language codes and names
        """
        return {
            "fa": "فارسی",
            "en": "English",
            "ar": "العربية",
        }
    
    def get_rtl_languages(self) -> list:
        """Get list of right-to-left languages"""
        return ["fa", "ar"]
    
    def is_rtl(self, language: str) -> bool:
        """Check if language is right-to-left"""
        return language in self.get_rtl_languages()
    
    def validate_language(self, language: str) -> bool:
        """Validate if language is supported"""
        return language in self.SUPPORTED_LANGUAGES


# Global i18n instance
_i18n_service: Optional[I18nService] = None

def init_i18n(translations_dir: str = "backend/translations") -> I18nService:
    """Initialize global i18n service"""
    global _i18n_service
    _i18n_service = I18nService(translations_dir)
    return _i18n_service

def get_i18n() -> I18nService:
    """Get global i18n service"""
    global _i18n_service
    if _i18n_service is None:
        _i18n_service = I18nService()
    return _i18n_service

def _(key: str, language: str = None, **kwargs) -> str:
    """Shorthand for translate function"""
    return get_i18n().translate(key, language, **kwargs)


__all__ = [
    "I18nService",
    "init_i18n",
    "get_i18n",
    "_",
]
