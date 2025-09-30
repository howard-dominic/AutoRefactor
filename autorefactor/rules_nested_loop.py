import ast

def find_nested_loops(src):
    results = []
    try:
        tree = ast.parse(src)
    except Exception:
        return results

    class Visitor(ast.NodeVisitor):
        def visit_For(self, node):
            for child in ast.walk(node):
                if child is not node and isinstance(child, ast.For):
                    results.append({
                        "line": node.lineno,
                        "code": ast.get_source_segment(src, node) or "for ...",
                        "message": "Nested loop detected; consider optimizing."
                    })
                    break
            if isinstance(node.iter, ast.Call) and getattr(node.iter.func, "id", "") == "range":
                if node.iter.args and isinstance(node.iter.args[0], ast.Call):
                    inner = node.iter.args[0]
                    if getattr(inner.func, "id", "") == "len":
                        results.append({
                            "line": node.lineno,
                            "code": ast.get_source_segment(src, node) or "for ...",
                            "message": "range(len(...)) pattern; consider enumerate or direct iteration."
                        })
            self.generic_visit(node)

    Visitor().visit(tree)
    return results
