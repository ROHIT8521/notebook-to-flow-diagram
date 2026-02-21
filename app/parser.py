import nbformat
import re
from typing import List, Tuple

DATBRICKS_CMD_RE = re.compile(r"^#\s*COMMAND\b")

def detect_format(filename: str, raw_bytes: bytes) -> str:
    name = filename.lower()
    if name.endswith('.ipynb'):
        return 'ipynb'
    if name.endswith('.dbc'):
        return 'dbc'
    text = raw_bytes.decode('utf-8', errors='ignore')
    if 'Databricks notebook source' in text:
        return 'databricks_py'
    if text.lstrip().startswith('{') and 'cells' in text:
        return 'ipynb'
    if name.endswith('.py'):
        return 'py'
    return 'text'

def extract_cells_from_ipynb(raw_bytes: bytes) -> List[Tuple[str, str]]:
    nb = nbformat.reads(raw_bytes.decode('utf-8'), as_version=4)
    cells = []
    for c in nb.cells:
        cells.append((c.cell_type, c.source))
    return cells

def split_databricks_source(text: str) -> List[str]:
    lines = text.splitlines()
    cells = []
    cur = []
    for line in lines:
        if DATBRICKS_CMD_RE.match(line):
            if cur:
                cells.append('\n'.join(cur).strip())
                cur = []
            continue
        cur.append(line)
    if cur:
        cells.append('\n'.join(cur).strip())
    return [c for c in cells if c]

def extract_cells_from_pytext(raw_bytes: bytes) -> List[Tuple[str, str]]:
    text = raw_bytes.decode('utf-8', errors='ignore')
    if 'Databricks notebook source' in text or '# COMMAND' in text:
        cells = split_databricks_source(text)
        return [('code', c) for c in cells]
    return [('code', text)]

def extract_cells(filename: str, raw_bytes: bytes):
    fmt = detect_format(filename, raw_bytes)
    if fmt == 'ipynb':
        return extract_cells_from_ipynb(raw_bytes)
    if fmt in ('databricks_py', 'py'):
        return extract_cells_from_pytext(raw_bytes)
    raise ValueError(f'Unsupported notebook format: {fmt}')
