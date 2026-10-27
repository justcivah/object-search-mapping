from types import SimpleNamespace

import numpy as np

from osm_exploration.map_utils import (
    GridInfo, cell_to_world, in_bounds, occupancy_grid_to_array, world_to_cell)

INFO = GridInfo(resolution=0.05, origin_x=-1.0, origin_y=-2.0, width=40, height=80)


def test_cell_to_world_is_cell_center():
    x, y = cell_to_world(INFO, row=0, col=0)
    assert np.isclose(x, -1.0 + 0.025)
    assert np.isclose(y, -2.0 + 0.025)


def test_world_to_cell_roundtrip():
    rows = np.array([0, 5, 79])
    cols = np.array([0, 12, 39])
    x, y = cell_to_world(INFO, rows, cols)
    r, c = world_to_cell(INFO, x, y)
    assert np.array_equal(r, rows)
    assert np.array_equal(c, cols)


def test_in_bounds():
    assert in_bounds(INFO, 0, 0)
    assert in_bounds(INFO, 79, 39)
    assert not in_bounds(INFO, 80, 0)
    assert not in_bounds(INFO, 0, -1)


def test_occupancy_grid_to_array_layout():
    # data is row-major: the second value is row 0, col 1
    msg = SimpleNamespace(data=[0, 100, -1, 0, 0, 0],
                          info=SimpleNamespace(width=3, height=2))
    grid = occupancy_grid_to_array(msg)
    assert grid.shape == (2, 3)
    assert grid[0, 1] == 100
    assert grid[0, 2] == -1
