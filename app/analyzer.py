import ast
import re
from typing import List, Dict, Any

READ_PATTERNS = [r"spark\.read", r"pd\.read_csv", r"pd\.read_parquet", r"read_csv\(", r"read_parquet\("]
TRANSFORM_PATTERNS = [r"\.filter\(", r"\.where\(", r"\.select\(", r"\.join\(", r"\.groupBy\(", r"\.withColumn\("]
WRITE_PATTERNS = [r"\.write\.", r"\.to_parquet\(", r"\.to_csv\("]

def _first_match(patterns, text):
    for p in patterns:
        if re.search(p, text):
            return True
    return False

class Step:
    def __init__(self, id: str, label: str, type: str = 'process'):
        self.id = id
        self.label = label
        self.type = type

    def to_dict(self):
        return {'id': self.id, 'label': self.label, 'type': self.type}

def extract_steps_from_cells(cells: List[tuple]) -> List[Dict[str, Any]]:
    steps = []
    step_counter = 1
    var_map = {}

    for cell_idx, (ctype, src) in enumerate(cells):
        label = None
        typ = 'process'
        if _first_match(READ_PATTERNS, src):
            label = 'Read data'
            typ = 'io'
        elif _first_match(WRITE_PATTERNS, src):
            label = 'Write/Save data'
            typ = 'io'
        elif _first_match(TRANSFORM_PATTERNS, src):
            label = 'Transform / Select / Join'
            typ = 'process'

        try:
            tree = ast.parse(src)
            for node in ast.walk(tree):
                if isinstance(node, ast.If):
                    label = 'Condition' if label is None else label + ' + condition'
                    typ = 'decision'
        except Exception:
            pass

        assigned = []
        try:
            tree = ast.parse(src)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            assigned.append(target.id)
                        elif isinstance(target, ast.Tuple):
                            for elt in target.elts:
                                if isinstance(elt, ast.Name):
                                    assigned.append(elt.id)
        except Exception:
            pass

        if label is None:
            first_line = next((ln.strip() for ln in src.splitlines() if ln.strip()), '')
            label = (first_line[:80] + '...') if len(first_line) > 80 else first_line or 'Code block'

        sid = f's{step_counter}'
        step_counter += 1
        step = Step(id=sid, label=f'Cell {cell_idx+1}: {label}', type=typ)
        steps.append(step.to_dict())

        for v in assigned:
            var_map[v] = sid

    return steps
