def squares(n):
    res = []
    for i in range(n):
        res.append(i*i)
    return res

def nested_loop(data):
    out = []
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i] == data[j]:
                out.append(data[i])
    return out

def count_check(item, lst):
    return lst.count(item) > 0
