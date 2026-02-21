import base64

def mermaid_to_image_url(mermaid_text: str, fmt: str = "png") -> str:
    encoded = base64.b64encode(mermaid_text.encode("utf-8")).decode("utf-8")
    return f"https://mermaid.ink/img/{encoded}"
