import urllib.parse

def mermaid_to_image_url(mermaid_text: str, fmt: str = 'png') -> str:
    safe = urllib.parse.quote(mermaid_text, safe='')
    return f'https://mermaid.ink/img/{fmt}/{safe}'
