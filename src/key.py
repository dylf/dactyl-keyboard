import json
import os
from geom import *

SIZES = {
    "MX": {"w": 14, "h": 14, "d": 10},
    "ALPS": {"w": 15.5, "h": 12.8, "d": 10}
}


class Key(object):
    _pos = [0, 0, 0]
    _rot = [0, 0, 0]
    _key_id = None
    type = "MX"
    w = SIZES["MX"]["w"]
    h = SIZES["MX"]["h"]
    d = SIZES["MX"]["d"]
    hole = "NOTCH"

    def __init__(self, key_id, parent_locals, key_type="MX", hole_type="NOTCH"):
        self._key_id = key_id
        self.type = key_type
        self.hole = hole_type
        self.w = SIZES[key_type]["w"]
        self.h = SIZES[key_type]["h"]
        self.d = SIZES[key_type]["d"]
        if parent_locals is not None:
            for item in parent_locals:
                globals()[item] = parent_locals[item]

    def set_pos(self, new_pos):
        self._pos = new_pos

    def get_pos(self):
        return self._pos

    pos = property(get_pos, set_pos)

    def set_rot(self, new_rot):
        self._rot = new_rot

    def get_rot(self):
        return self._rot

    rot = property(get_rot, set_rot)

    def get_id(self):
        return self._key_id

    def rotate_deg(self, rotate_by):
        self._rot = rotate_deg(self._rot, rotate_by)
        return self._rot

    def rotate_rad(self, rotate_by):
        self._rot = rotate_rad(self._rot, rotate_by)
        return self._rot

    def translate(self, position):
        self._pos = add_translate(self._pos, position)
        return self._pos

    def calculate_key_placement(self,
                                column,
                                row,
                                column_style="standard",
                                ):

        xrot = 0
        yrot = 0
        position = [0, 0, 0]

        column_angle = beta * (centercol - column)
        column_x_delta_actual = column_x_delta
        if (pinky_1_5U and column == lastcol):
            if row >= first_1_5U_row and row <= last_1_5U_row:
                column_x_delta_actual = column_x_delta - 1.5
                column_angle = beta * (centercol - column - 0.27)

        if column_style == "orthographic":
            column_z_delta = column_radius * (1 - np.cos(column_angle))
            position = add_translate(position, [0, 0, -row_radius])
            position = rotate_around_x(position, alpha * (centerrow - row))
            xrot += alpha * (centerrow - row)
            position = add_translate(position, [0, 0, row_radius])
            position = rotate_around_y(position, column_angle)
            yrot += column_angle
            position = add_translate(
                position, [-(column - centercol) * column_x_delta_actual, 0, column_z_delta]
            )
            position = add_translate(position, column_offset(column))

        elif column_style == "fixed":
            position = rotate_around_y(position, fixed_angles[column])
            yrot += fixed_angles[column]
            position = add_translate(position, [fixed_x[column], 0, fixed_z[column]])
            position = add_translate(position, [0, 0, -(row_radius + fixed_z[column])])
            position = rotate_around_x(position, alpha * (centerrow - row))
            xrot += alpha * (centerrow - row)
            position = add_translate(position, [0, 0, row_radius + fixed_z[column]])
            position = rotate_around_y(position, fixed_tenting)
            yrot += fixed_tenting
            position = add_translate(position, [0, column_offset(column)[1], 0])

        else:
            position = add_translate(position, [0, 0, -row_radius])
            position = rotate_around_x(position, alpha * (centerrow - row))
            xrot += alpha * (centerrow - row)
            position = add_translate(position, [0, 0, row_radius])
            position = add_translate(position, [0, 0, -column_radius])
            position = rotate_around_y(position, column_angle)
            yrot += column_angle
            position = add_translate(position, [0, 0, column_radius])
            position = add_translate(position, column_offset(column))

        position = rotate_around_y(position, tenting_angle)
        yrot += tenting_angle
        position = add_translate(position, [0, 0, keyboard_z_offset])

        self.pos = position
        self.rot = to_degrees([xrot, yrot, 0])
        return [self.pos, self.rot]

    def render(self, plate_file, side="right"):
        if plate_style in ['NUB', 'HS_NUB']:
            tb_border = (mount_height - keyswitch_height) / 2
            top_wall = box(mount_width, tb_border, plate_thickness)
            top_wall = translate(top_wall, (0, (tb_border / 2) + (keyswitch_height / 2), plate_thickness / 2))

            lr_border = (mount_width - keyswitch_width) / 2
            left_wall = box(lr_border, mount_height, plate_thickness)
            left_wall = translate(left_wall, ((lr_border / 2) + (keyswitch_width / 2), 0, plate_thickness / 2))

            side_nub = cylinder(radius=1, height=2.75)
            side_nub = rotate(side_nub, (90, 0, 0))
            side_nub = translate(side_nub, (keyswitch_width / 2, 0, 1))

            nub_cube = box(1.5, 2.75, plate_thickness)
            nub_cube = translate(nub_cube, ((1.5 / 2) + (keyswitch_width / 2), 0, plate_thickness / 2))

            side_nub2 = tess_hull(shapes=(side_nub, nub_cube))
            side_nub2 = union([side_nub2, side_nub, nub_cube])

            plate_half1 = union([top_wall, left_wall, side_nub2])
            plate_half2 = plate_half1
            plate_half2 = mirror(plate_half2, 'XZ')
            plate_half2 = mirror(plate_half2, 'YZ')

            plate = union([plate_half1, plate_half2])

        # elif plate_style in "AMOEBA":  # 'HOLE' or default, square cutout for non-nub designs.
        #     plate = box(mount_width, mount_height, mount_thickness)
        #     plate = translate(plate, (0.0, 0.0, mount_thickness / 2.0))
        #
        #     shape_cut = box(keyswitch_width + 2, keyswitch_height + 2, mount_thickness * 2 + .02)
        #     shape_cut = translate(shape_cut, (0.0, 0.0, mount_thickness - .01))
        #
        #     plate = difference(plate, [shape_cut])

        else:  # 'HOLE' or default, square cutout for non-nub designs.
            plate = box(mount_width, mount_height, mount_thickness)
            plate = translate(plate, (0.0, 0.0, mount_thickness / 2.0))

            shape_cut = box(keyswitch_width, keyswitch_height, mount_thickness * 2 + .02)
            shape_cut = translate(shape_cut, (0.0, 0.0, mount_thickness - .01))

            plate = difference(plate, [shape_cut])

        if plate_file is not None:
            socket = import_file(plate_file)
            socket = translate(socket, [0, 0, plate_thickness + plate_offset])
            plate = union([plate, socket])

        if plate_style in ['UNDERCUT', 'HS_UNDERCUT', 'NOTCH', 'HS_NOTCH', 'AMOEBA']:
            if plate_style in ['UNDERCUT', 'HS_UNDERCUT']:
                undercut = box(
                    keyswitch_width + 2 * clip_undercut,
                    keyswitch_height + 2 * clip_undercut,
                    mount_thickness
                )

            if plate_style in ['NOTCH', 'HS_NOTCH', 'AMOEBA']:
                undercut = box(
                    notch_width,
                    keyswitch_height + 2 * clip_undercut,
                    mount_thickness
                )
                undercut = union([undercut,
                                  box(
                                      keyswitch_width + 2 * clip_undercut,
                                      notch_width,
                                      mount_thickness
                                  )
                                  ])

            undercut = translate(undercut, (0.0, 0.0, -clip_thickness + mount_thickness / 2.0))

            if ENGINE == 'cadquery' and undercut_transition > 0:
                undercut = undercut.faces("+Z").chamfer(undercut_transition, clip_undercut)

            plate = difference(plate, [undercut])

        # if plate_file is not None:
        #     socket = import_file(plate_file)
        #
        #     socket = translate(socket, [0, 0, plate_thickness + plate_offset])
        #     plate = union([plate, socket])

        if plate_holes:
            half_width = plate_holes_width / 2.
            half_height = plate_holes_height / 2.
            x_off = plate_holes_xy_offset[0]
            y_off = plate_holes_xy_offset[1]
            holes = [
                translate(
                    cylinder(radius=plate_holes_diameter / 2, height=plate_holes_depth + .01),
                    (x_off + half_width, y_off + half_height, plate_holes_depth / 2 - .01)
                ),
                translate(
                    cylinder(radius=plate_holes_diameter / 2, height=plate_holes_depth + .01),
                    (x_off - half_width, y_off + half_height, plate_holes_depth / 2 - .01)
                ),
                translate(
                    cylinder(radius=plate_holes_diameter / 2, height=plate_holes_depth + .01),
                    (x_off - half_width, y_off - half_height, plate_holes_depth / 2 - .01)
                ),
                translate(
                    cylinder(radius=plate_holes_diameter / 2, height=plate_holes_depth + .01),
                    (x_off + half_width, y_off - half_height, plate_holes_depth / 2 - .01)
                ),
            ]
            plate = difference(plate, holes)

        if side == "left":
            plate = mirror(plate, 'YZ')

        plate = rotate(plate, self.rot)
        plate = translate(plate, self.pos)

        return plate