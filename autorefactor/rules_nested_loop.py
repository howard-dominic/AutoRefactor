"""
AST-based rules:
- detect nested for-loops
- detect for i in range(len(x)) -> suggest enumerate
- detect list.count(item) usage -> suggest set membership
"""
import ast
from typing import List, Dict

def find_nested_loops(src: str) -> List[Dict]:
    results = []
    try:
        tree = ast.parse(src)
    except Exception:
        return results

    class Visitor(ast.NodeVisitor):
        def visit_For(self, node):
            # Nested loop detection
            for child in ast.walk(node):
                if child is not node and isinstance(child, ast.For):
                    snippet = ast.get_source_segment(src, node) or "for ... in ..."
                    results.append({
                        "line": node.lineno,
                        "code": snippet,
                        "message": "Nested loop detected. Consider refactoring."
                    })
                    break
            # Pattern: for i in range(len(x)):
            if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
                if node.iter.args and isinstance(node.iter.args[0], ast.Call):
                    inner = node.iter.args[0]
                    if isinstance(inner.func, ast.Name) and inner.func.id == 'len':
                        results.append({
                            "line": node.lineno,
                            "code": ast.get_source_segment(src, node) or "<for ...>",
                            "message": "Pattern 'for i in range(len(...))' detected. Use enumerate or iterate directly."
                        })
            self.generic_visit(node)

    class CountVisitor(ast.NodeVisitor):
        def visit_Call(self, node):
            # Robust count detection
            if isinstance(node.func, ast.Attribute) and node.func.attr == "count":
                if hasattr(node.func, "value"):
                    results.append({
                        "line": node.lineno,
                        "code": ast.get_source_segment(src, node) or ".count(...)",
                        "message": "Use of list.count() detected. Consider 'in' with a set for faster checks."
                    })
            self.generic_visit(node)

    Visitor().visit(tree)
    CountVisitor().visit(tree)
    return results
