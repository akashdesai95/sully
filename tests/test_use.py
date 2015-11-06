import pytest

from sully import TaintAnalysis

# Below are simple objects we use for testing
# ==========

class constants:
    BAZ = 7

class Bar:
    x = 2
    y = [4, 5, 6]

    def helper(self, x):
        return x

    def foo(self):                    # 1
        y = [1, 2, 3]                 # 2
        x = 3 + y[1]                  # 3
        y[3] += 2 + self.x            # 4
        self.x = y[0]                 # 5
        self.y[1] = y[0]              # 6
        self.x = y[0]                 # 7
        x + 2 + constants.BAZ         # 8
        z = []                        # 9
        z.append(3)                   # 10
        a = 3                         # 11
        b = []                        # 12
        c = {}                        # 13
        self.helper(a, *b, **c)       # 14

# ==========

@pytest.fixture
def taint():
    return TaintAnalysis(Bar.foo)

def test_function_write(taint):
    assert taint.write_lines['z'] == [9, 10]

def test_simple_read(taint):
    assert taint.read_lines['x'] == [8]

def test_simple_write(taint):
    assert taint.write_lines['x'] == [3]

def test_self_read(taint):
    assert taint.read_lines[('self', 'x')] == [4]

def test_self_write(taint):
    assert taint.write_lines[('self', 'x')] == [5, 7]

def test_constaint(taint):
    assert taint.read_lines[('constants', 'BAZ')] == [8]

def test_array_read(taint):
    assert taint.read_lines['y'] == [4]

def test_array_write(taint):
    assert taint.write_lines['y'] == [2]

def test_parameter_read(taint):
    assert taint.read_lines['a'] == [14]
    assert taint.read_lines['b'] == [14]
    assert taint.read_lines['c'] == [14]
