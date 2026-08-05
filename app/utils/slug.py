import re
import unicodedata


def slugify(text: str) -> str:
    """
    Convert a string title into a clean, URL-friendly slug.
    Example: "Gaming Laptop Pro 15!" -> "gaming-laptop-pro-15"
    """
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text
