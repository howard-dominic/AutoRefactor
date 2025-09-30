from autorefactor.rules_nested_loop import find_nested_loops

def test_range_len_pattern():
    src = "for i in range(len(x)):\\n    print(x[i])\\n"
    results = find_nested_loops(src)
    assert any("enumerate" in r["message"] or "range(len" in r["message"] for r in results)

def test_nested_loop_detection():
    src = "for i in range(3):\\n    for j in range(3):\\n        pass\\n"
    results = find_nested_loops(src)
    assert any("Nested loop" in r["message"] for r in results)

def test_count_usage():
    src = "lst = [1,2,3]\\nif lst.count(2) > 0:\\n    pass\\n"
    results = find_nested_loops(src)
    assert any("count" in r["message"].lower() for r in results)
