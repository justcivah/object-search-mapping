"""Conversions between an OccupancyGrid and numpy, and between cells and meters.

Conventions used in the whole package:
- the grid is a 2D array of shape (height, width), indexed as grid[row, col]
- row grows with y, col grows with x (same layout as OccupancyGrid.data)
- a cell is identified by (row, col); a point in the map frame by (x, y)

The grid origin is assumed to have no rotation (true for slam_toolbox).
"""

from dataclasses import dataclass

import numpy as np

UNKNOWN = -1


@dataclass(frozen=True)
class GridInfo:
    """Geometry of the grid: everything needed to convert cells <-> meters."""

    resolution: float
    origin_x: float
    origin_y: float
    width: int
    height: int

    @classmethod
    def from_msg(cls, info):
        """Build from nav_msgs/MapMetaData (the .info field of an OccupancyGrid)."""
        return cls(
            resolution=info.resolution,
            origin_x=info.origin.position.x,
            origin_y=info.origin.position.y,
            width=info.width,
            height=info.height,
        )


def occupancy_grid_to_array(msg):
    """Return the OccupancyGrid data as an int8 array of shape (height, width)."""
    return np.asarray(msg.data, dtype=np.int8).reshape(msg.info.height, msg.info.width)


def cell_to_world(info, row, col):
    """Return the (x, y) of the center of a cell. Works on scalars and arrays."""
    x = info.origin_x + (np.asarray(col) + 0.5) * info.resolution
    y = info.origin_y + (np.asarray(row) + 0.5) * info.resolution
    return x, y


def world_to_cell(info, x, y):
    """Return the (row, col) of the cell containing (x, y). Works on scalars and arrays."""
    col = np.floor((np.asarray(x) - info.origin_x) / info.resolution).astype(int)
    row = np.floor((np.asarray(y) - info.origin_y) / info.resolution).astype(int)
    return row, col


def in_bounds(info, row, col):
    """Return True where (row, col) is inside the grid."""
    row = np.asarray(row)
    col = np.asarray(col)
    return (row >= 0) & (row < info.height) & (col >= 0) & (col < info.width)
