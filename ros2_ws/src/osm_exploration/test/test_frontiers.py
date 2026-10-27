import numpy as np

from osm_exploration.frontiers import find_frontiers, frontier_mask

UNK = -1
FREE = 0
OCC = 100


def test_frontier_between_free_and_unknown():
    grid = np.array([
        [FREE, FREE, FREE, UNK, UNK],
        [FREE, FREE, FREE, UNK, UNK],
        [FREE, FREE, FREE, UNK, UNK],
        [OCC, OCC, OCC, UNK, UNK],
    ], dtype=np.int8)
    expected = np.zeros_like(grid, dtype=bool)
    expected[0:3, 2] = True  # last free column; occupied cells are never frontiers
    assert np.array_equal(frontier_mask(grid), expected)


def test_no_unknown_means_no_frontiers():
    grid = np.full((5, 5), FREE, dtype=np.int8)
    grid[2, 2] = OCC
    assert not frontier_mask(grid).any()


def test_two_separate_frontiers():
    grid = np.array([
        [UNK, FREE, FREE, FREE, FREE, FREE, UNK],
        [UNK, FREE, FREE, FREE, FREE, FREE, UNK],
        [UNK, FREE, FREE, FREE, FREE, FREE, UNK],
    ], dtype=np.int8)
    frontiers = find_frontiers(grid)
    assert len(frontiers) == 2
    assert sorted(f.size for f in frontiers) == [3, 3]


def test_small_frontiers_are_dropped():
    grid = np.full((5, 5), FREE, dtype=np.int8)
    grid[0, 0] = UNK  # touches 3 free cells
    assert len(find_frontiers(grid, min_size=1)) == 1
    assert len(find_frontiers(grid, min_size=4)) == 0


def test_goal_cell_is_a_frontier_cell():
    # curved frontier: its centroid falls in unknown space, the goal must not
    grid = np.array([
        [FREE, FREE, FREE, FREE, FREE],
        [FREE, UNK, UNK, UNK, FREE],
        [FREE, UNK, UNK, UNK, FREE],
        [FREE, UNK, UNK, UNK, FREE],
    ], dtype=np.int8)
    (frontier,) = find_frontiers(grid)
    mask = frontier_mask(grid)
    assert mask[frontier.goal_cell]
