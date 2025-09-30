from .rules_nested_loop import find_nested_loops

def run_all(src):
    results = []
    results.extend(find_nested_loops(src))
    return results
