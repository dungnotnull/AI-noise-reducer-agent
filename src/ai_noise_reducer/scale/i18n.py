from __future__ import annotations


class LocalizationService:
    def __init__(self) -> None:
        self.supported_languages = ["en", "es", "fr", "de", "vi"]

    def localize_brief(self, text: str, language: str = "en") -> str:
        if language not in self.supported_languages:
            language = "en"
        # Placeholder translation strategy
        return f"[{language}] {text}"
