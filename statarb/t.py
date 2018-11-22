import pandas as pd

def test():
    a = 1
    b = 'string'
    c = pd.DataFrame.from_dict({"A":[1, 2], "B":[3, 4]}, orient = 'index')
    return (c, a)

print(type(test()[1]))
