import numpy as np


def deg2rad(degrees: float) -> float:
    return degrees * np.pi / 180


def rad2deg(rad: float) -> float:
    return rad * 180 / np.pi


def to_degrees(rots):
    return [rad2deg(a) for a in rots]


def rotate_around_x(position, angle):
    # debugprint('rotate_around_x()')
    t_matrix = np.array(
        [
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)],
        ]
    )
    return np.matmul(t_matrix, position)


def rotate_around_y(position, angle):
    # debugprint('rotate_around_y()')
    t_matrix = np.array(
        [
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)],
        ]
    )
    return np.matmul(t_matrix, position)


def rotate_around_z(position, angle):
    # debugprint('rotate_around_y()')
    t_matrix = np.array(
        [
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1],
        ]
    )
    return np.matmul(t_matrix, position)


def rotate_rad(start, rotate_by):
    x_pos = rotate_around_x(start, rotate_by[0])[0]
    y_pos = rotate_around_y(start, rotate_by[1])[1]
    z_pos = rotate_around_z(start, rotate_by[2])[2]
    return [x_pos, y_pos, z_pos]


def rotate_deg(start, rotate_by):
    return [rad2deg(x) for x in rotate_rad(start, [deg2rad(y) for y in rotate_by])]


def add_translate(shape, xyz):
    vals = []
    for i in range(len(shape)):
        vals.append(shape[i] + xyz[i])
    return vals
