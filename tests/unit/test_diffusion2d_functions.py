"""
Tests for functions in class SolveDiffusion2D
"""

import numpy as np
import pytest

from diffusion2d import SolveDiffusion2D


@pytest.fixture
def solver():
    return SolveDiffusion2D()


@pytest.mark.parametrize('w, h, dx, dy, nx, ny', [(20., 20., 0.2, 0.5, 100, 40),
                                                  (12., 18., 0.4, 0.4, 30, 45),
                                                  (108., 112., 0.3, 0.3, 360, 373)])
def test_initialize_domain(solver, w, h, dx, dy, nx, ny):
    """
    Check function SolveDiffusion2D.initialize_domain
    """
    solver.initialize_domain(w, h, dx, dy)
    assert solver.nx == nx
    assert solver.ny == ny


@pytest.mark.parametrize('d, dt', [(6., 0.001666666), (14., 0.0007142857)])
def test_initialize_physical_parameters(solver, d, dt):
    """
    Checks function SolveDiffusion2D.initialize_domain
    """
    # Only parametrize d, since T_cold and T_hot has no influence on calculating dt.
    solver.dx = 0.2
    solver.dy = 0.2
    solver.initialize_physical_parameters(d, 350., 500.)
    assert solver.dt == pytest.approx(dt, rel=0.000001)


def test_set_initial_condition(solver):
    """
    Checks function SolveDiffusion2D.get_initial_function
    """
    solver.dx = 0.7
    solver.dy = 0.7
    solver.nx = 200
    solver.ny = 200
    solver.T_cold = 400.
    solver.T_hot = 800.

    actual = solver.set_initial_condition()

    idx = np.array([5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9])
    idy = np. array([6, 7, 8, 9, 5, 6, 7, 8, 9, 5, 6, 7, 8, 9, 5, 6, 7, 8, 9, 5, 6, 7, 8, 9])
    expected = np.ones((200, 200))
    expected[:, :] = 400.
    expected[idx, idy] = 800.

    assert (actual == expected).all()
