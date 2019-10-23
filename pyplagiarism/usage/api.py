from pyplagiarism.tool import plagiarism

a = """
def calculate():
    x = 6
    y = 5
    return x + y
"""

b = """
def calculate():
    return 5 + 6
"""

c = """
def calculate():
    x = 6
    y = 5
    return x + y
"""

data = {"a": a, "b": b, "c": c}

plagiarism(data, visualize_as_html=False, diff_of_files=False)
