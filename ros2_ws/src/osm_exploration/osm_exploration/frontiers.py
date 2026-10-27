"""Frontier detection on an occupancy grid (numpy only, no ROS).

A frontier cell is a free cell with at least one unknown neighbour (8-connectivity).
Frontier cells that touch each other form a frontier (a cluster).
"""

from dataclasses import dataclass

import numpy as np

from osm_exploration.map_utils import UNKNOWN


@dataclass
class Frontier:
    cells: np.ndarray       # (N, 2) array of (row, col)
    goal_cell: tuple        # (row, col) where the robot should go to explore it
    size: int               # number of cells


def free_mask(grid, free_threshold=25):
    """Boolean mask of free cells: known (not -1) and occupancy below the threshold."""
    # TODO
    raise NotImplementedError


def unknown_mask(grid):
    """Boolean mask of unknown cells (value -1)."""
    # TODO
    raise NotImplementedError


def frontier_mask(grid, free_threshold=25):
    """Boolean mask of frontier cells: free cells with at least one unknown 8-neighbour.

    Hint: "has an unknown neighbour" == "is inside the unknown mask grown by one cell".
    """
    # TODO
    raise NotImplementedError


def cluster_frontiers(mask, min_size=1):
    """Group touching frontier cells (8-connectivity) and drop clusters smaller than min_size.

    Returns a list of Frontier. Hint: scipy.ndimage.label.
    """
    # TODO
    raise NotImplementedError


def find_frontiers(grid, free_threshold=25, min_size=1):
    """Full pipeline: grid -> list of Frontier."""
    return cluster_frontiers(frontier_mask(grid, free_threshold), min_size)
