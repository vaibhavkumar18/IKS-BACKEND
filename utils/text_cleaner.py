import re

def clean_text(text: str) -> str:
    if not text:
        return text

    # remove markdown bold **text**
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)

    # remove numbering like "1. ", "2. "
    text = re.sub(r"^\d+\.\s*", "", text)

    return text.strip()
