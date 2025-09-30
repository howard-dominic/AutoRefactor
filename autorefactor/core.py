import os
from .rules_registry import run_all
try:
    from radon.complexity import cc_visit
except ImportError:
    cc_visit = None

def analyze_file(path):
    suggestions = []
    files = [path] if os.path.isfile(path) else [
        os.path.join(root, f)
        for root, _, files in os.walk(path)
        for f in files if f.endswith(".py")
    ]

    for f in files:
        try:
            src = open(f, "r").read()
        except Exception:
            continue

        if cc_visit:
            try:
                blocks = cc_visit(src)
                for b in blocks:
                    if getattr(b, "complexity", 0) >= 10:
                        suggestions.append({
                            "file": f,
                            "line": getattr(b, "lineno", 1),
                            "message": f"High complexity ({b.complexity}) in {b.name}; consider splitting."
                        })
            except Exception:
                pass

        for r in run_all(src):
            r.update({"file": f})
            suggestions.append(r)

    return suggestions
