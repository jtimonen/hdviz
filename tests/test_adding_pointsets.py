# Test adding multiple pointsets at once
import hdviz
import numpy as np


def test_adding_pointsets():
    a = hdviz.Plotter3d()
    x = 1.5 + 0.1 * np.random.normal(size=(100, 3))
    a.add_pointset(x, label="first group", marker="x")
    x = np.random.normal(size=(100, 3))
    categs = 10 * np.ones(100, dtype=int)
    categs[0:99] = np.random.choice(3, size=99)
    colors = dict(zip([0, 1, 2, 10], ["pink", "red", "orange", "black"]))
    a.add_pointsets(x, categs, categ_prefix="additional", colors=colors, alpha=0.5)
    assert a.num_pointsets() == 5
