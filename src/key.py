from geom import *
from part import Part


SIZES = {
    "MX": {"w": 14, "h": 14, "d": 10},
    "ALPS": {"w": 15.5, "h": 12.8, "d": 10}
}

KEY_NONE = None

class Key(Part):
    type = "MX"
    hole = "NOTCH"
    plate_rot_z = 0

    def __init__(self, key_id, parent_locals, key_type="MX", hole_type="NOTCH"):
        super().__init__(key_id)
        self.type = key_type
        self.hole = hole_type
        self.w = SIZES[key_type]["w"]
        self.h = SIZES[key_type]["h"]
        self.d = SIZES[key_type]["d"]
        if parent_locals is not None:
            for item in parent_locals:
                globals()[item] = parent_locals[item]

    def __str__(self):
        return f'K-{self.get_id()}'

    def tr(self, add_x=0, add_y=0):
        offset = rotate_deg([(mount_width / 2.0) + add_x, (mount_height / 2) + add_y, 0], self._rot)
        return add_translate(self._pos, offset)

    def tl(self, add_x=0, add_y=0):
        offset = rotate_deg([-(mount_width / 2.0) - add_x, (mount_height / 2) + add_y, 0], self._rot)
        return add_translate(self._pos, offset)

    def br(self, add_x=0, add_y=0):
        offset = rotate_deg([(mount_width / 2.0) + add_x, -(mount_height / 2) - add_y, 0], self._rot)
        return add_translate(self._pos, offset)

    def bl(self, add_x=0, add_y=0):
        offset = rotate_deg([-(mount_width / 2.0) - add_x, -(mount_height / 2) - add_y, 0], self._rot)
        return add_translate(self._pos, offset)

    def top_edge(self):
        return [self.tl(), self.tr()]

    def bottom_edge(self):
        return [self.bl(), self.br()]

    def inner_edge(self, side="right"):
        if side == "right":
            return [self.tl(), self.bl()]

        return [self.tr(), self.br()]

    def outer_edge(self, side="right"):
        if side == "left":
            return self.inner_edge(side="right")
        return self.inner_edge(side="left")

    def is_none(self):
        return self._id == "none"

    def closest_corner(self, rel_pos):
        dist = 99999999999.0
        all_dist = [
            distance(rel_pos, self.tl()),
            distance(rel_pos, self.tr()),
            distance(rel_pos, self.bl()),
            distance(rel_pos, self.br())
        ]

        index = -1

        for i in range(4):
            if all_dist[i] < dist:
                index = i
                dist = all_dist[i]

        if index == 0:
            return self.tl()
        elif index == 1:
            return self.tr()
        elif index == 2:
            return self.bl()

        return self.br()

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
        if plate_style == "MXLEDBIT":
            pcb_width = 19
            pcb_length = 19
            pcb_height = 1.6

            # degrees = np.degrees(alpha / 2)
            # frame = box(pcb_width + 2, pcb_length + 2, pcb_height * 2)
            # cutout = union([box(pcb_width - 1, pcb_length - 1, pcb_height * 4),
            #                 translate(box(pcb_width + 0.2, pcb_height + 0.2, pcb_height * 2), (0, 0, -(pcb_height / 2)))])
            # # # frame = difference(frame, [box(pcb_width - 1, pcb_length - 1, pcb_height * 4)])
            # frame = difference(frame, [cutout])
            # connector = translate(rotate(box(pcb_width + 2, extra_height * 2, pcb_height * 2), (degrees, 0, 0)), (0, (pcb_length / 2), 0))
            # frame = union([frame, connector])

            degrees = np.degrees(alpha / 2)
            frame = box(21, 21, 3)
            # # frame = difference(frame, [box(pcb_width - 1, pcb_length - 1, pcb_height * 4)])
            frame = difference(frame, [box(18.5, 18.5, 5)])
            frame = difference(frame, [box(19.5, 19.5, 2.5)])
            connector = translate(rotate(box(21, 4, 2.5), (degrees, 0, 0)), (0, 11.5, 0))
            plate = translate(union([frame, connector]), (0, 0, -5))
            # return frame

        elif plate_style in ['NUB', 'HS_NUB']:
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
        if self.plate_rot_z != 0:
            plate = rotate(plate, [0, 0, self.plate_rot_z])
        plate = translate(plate, self.pos)

        return plate


class KeyFactory(object):

    NONE_KEY = Key("none", None)

    KEYS_BY_ID = {
        "none": NONE_KEY
    }

    MAX_ROW = -1
    MAX_COL = -1

    MATRIX = None
    ROWS = None
    WALL_KEYS = None

    @staticmethod
    def get_key_by_id(key_id: str) -> Key:
        if key_id not in KeyFactory.KEYS_BY_ID.keys():
            return KeyFactory.KEYS_BY_ID["none"]
        return KeyFactory.KEYS_BY_ID[key_id]

    @classmethod
    def get_key_by_row_col(cls, row, col) -> Key:
        return cls.get_key_by_id(cls.get_rc_id(row, col))

    @staticmethod
    def get_rc_id(row, col):
        return "r" + str(row) + "c" + str(col)

    @classmethod
    def build_matrix(cls):
        if len(cls.KEYS_BY_ID) <= 1:
            raise Exception("No keys present to build matrix.")

        cls.MATRIX = []
        top_wall = [cls.KEYS_BY_ID["none"] for x in range(cls.MAX_COL + 1)]
        bottom_wall = [cls.KEYS_BY_ID["none"] for x in range(cls.MAX_COL + 1)]
        inner_wall = [cls.KEYS_BY_ID["none"] for x in range(cls.MAX_ROW + 1)]
        outer_wall = [cls.KEYS_BY_ID["none"] for x in range(cls.MAX_ROW + 1)]
        all_rows = [[] for x in range(0, cls.MAX_COL + 1)]

        for col in range(cls.MAX_COL + 1):
            column_keys = []
            for row in range(cls.MAX_ROW + 1):
                key = cls.get_key_by_row_col(row, col)
                column_keys.append(key)
                all_rows[col].append(key)

                if key.get_id() != "none":
                    if top_wall[col].get_id() == "none":
                        top_wall[col] = key
                    if inner_wall[row].get_id() == "none":
                        inner_wall[row] = key
                    bottom_wall[col] = key
                    outer_wall[row] = key

            cls.MATRIX.append(column_keys)

        cls.WALL_KEYS = {
            "top": top_wall,
            "bottom": bottom_wall,
            "inner": inner_wall,
            "outer": outer_wall
        }

        cls.ROWS = all_rows

        print("KeyFactory: Matrix built.")

    @classmethod
    def get_column(cls, col) -> [Key]:
        return cls.MATRIX[col]

    @classmethod
    def get_row(cls, row) -> [Key]:
        return cls.ROWS[row]

    @classmethod
    def inner_keys(cls):
        return cls.WALL_KEYS["inner"]

    @classmethod
    def outer_keys(cls):
        return cls.WALL_KEYS["outer"]

    @classmethod
    def top_keys(cls):
        return cls.WALL_KEYS["top"]

    @classmethod
    def bottom_keys(cls):
        return cls.WALL_KEYS["bottom"]

    @staticmethod
    def clear_keys():
        KeyFactory.KEYS_BY_ID = {"none": Key("none", None)}
        KeyFactory.MAX_ROW = -1
        KeyFactory.MAX_COL = -1
        KeyFactory.MATRIX = None
        KeyFactory.ROWS = None
        KeyFactory.WALL_KEYS = None

    @classmethod
    def new_key(cls, key_id: str, parent_locals, key_type="MX", hole_type="NOTCH"):
        key = Key(key_id, parent_locals, key_type=key_type, hole_type=hole_type)
        if key_id in cls.KEYS_BY_ID:
            print("WARNING: key_id already in keys list", key_id)
        else:
            cls.KEYS_BY_ID[key_id] = key
        return key

    @classmethod
    def new_key_by_row_column(cls, row: int, col: int, parent_locals, key_type="MX", hole_type="NOTCH"):
        if row > cls.MAX_ROW:
            cls.MAX_ROW = row
        if col > cls.MAX_COL:
            cls.MAX_COL = col

        return cls.new_key(cls.get_rc_id(row, col), parent_locals, key_type=key_type, hole_type=hole_type)

