from clusters.trackball_wilder import TrackballWild
import json
import os


class TrackballThree(TrackballWild):

    @staticmethod
    def name():
        return "TRACKBALL_THREE"


    def get_config(self):
        with open(os.path.join("src", "clusters", "json", "TRACKBALL_THREE.json"), mode='r') as fid:
            data = json.load(fid)

        superdata = super().get_config()

        # overwrite any super variables with this class' needs
        for item in data:
            superdata[item] = data[item]

        for item in superdata:
            if not hasattr(self, str(item)):
                print(self.name() + ": NO MEMBER VARIABLE FOR " + str(item))
                continue
            setattr(self, str(item), superdata[item])

        return superdata

    def __init__(self, parent_locals):
        super().__init__(parent_locals)
        for item in parent_locals:
            globals()[item] = parent_locals[item]


    def bl_place(self, shape):
        debugprint('thumb_bl_place()')
        shape = rotate(shape, [0, 0, 180])
        shape = rotate(shape, self.key_rotation_offsets[2])
        t_off = self.key_translation_offsets[2]
        shape = translate(shape, (t_off[0], t_off[1]+self.key_diameter/2, t_off[2]))
        shape = rotate(shape, [0, 0, -240])
        shape = self.track_place(shape)

        return shape

    def thumbcaps(self, side='right'):
        t1 = self.thumb_1x_layout(sa_cap(1), cap=True)
        if not default_1U_cluster:
            t1.add(self.thumb_15x_layout(sa_cap(2), cap=True))
        return t1

    def thumb(self, side="right"):
        print('thumb()')
        shape = self.thumb_1x_layout(rotate(single_plate(side=side), (0, 0, -90)))
        shape = union([shape, self.thumb_15x_layout(rotate(single_plate(side=side), (0, 0, 90)))])
        # shape = union([shape, self.thumb_15x_layout(double_plate(), plate=False)])

        return shape

    def thumb_1x_layout(self, shape, cap=False):
        debugprint('thumb_1x_layout()')
        return union([
            self.tl_place(rotate(shape, [0, 0, self.thumb_plate_tr_rotation])),
            self.mr_place(rotate(shape, [0, 0, self.thumb_plate_mr_rotation])),
            # self.bl_place(rotate(shape, [0, 0, self.thumb_plate_bl_rotation])),
        ])

    def thumb_15x_layout(self, shape, cap=False, plate=True):
        debugprint('thumb_15x_layout()')
        shape_list = []
        if plate:
            if cap:
                shape = rotate(shape, (0, 0, 90))
                cap_list = [self.bl_place(rotate(shape, [0, 0, self.thumb_plate_bl_rotation]))]
                # cap_list.append(self.tr_place(rotate(shape, [0, 0, self.thumb_plate_tr_rotation])))
                return add(cap_list)
            else:
                shape_list = [self.bl_place(rotate(shape, [0, 0, self.thumb_plate_bl_rotation]))]

                return union(shape_list)
        else:
            if cap:
                shape = rotate(shape, (0, 0, 90))
                shape_list = [
                    self.bl_place(shape),
                ]
                # shape_list.append(self.bl_place(shape))

                return add(shape_list)
            else:
                shape_list = [
                    self.bl_place(shape),
                ]
                # if not default_1U_cluster:
                #     shape_list.append(self.bl_place(shape))

                return union(shape_list)

    def thumb_connectors(self, side="right"):
        print('thumb_connectors()')
        hulls = []

        # bottom 2 to tb
        hulls.append(
            triangle_hulls(
                [
                    self.track_place(self.tb_post_l()),
                    self.bl_place(web_post_tl()),
                    self.track_place(self.tb_post_bl()),
                    self.bl_place(web_post_tr()),
                    self.br_place(web_post_tl()),
                    self.track_place(self.tb_post_bl()),
                    self.br_place(web_post_tr()),
                    self.track_place(self.tb_post_br()),
                    self.br_place(web_post_tr()),
                    self.track_place(self.tb_post_br()),
                    self.mr_place(web_post_br()),
                    self.track_place(self.tb_post_r()),
                    self.mr_place(web_post_bl()),
                    self.tl_place(web_post_br()),
                    self.track_place(self.tb_post_r()),
                    self.tl_place(web_post_bl()),
                    self.track_place(self.tb_post_tr()),
                    key_place(web_post_bl(), 0, cornerrow),
                    self.track_place(self.tb_post_tl()),
                ]
            )
        )

        # bottom left
        hulls.append(
            triangle_hulls(
                [
                    self.bl_place(web_post_tr()),
                    self.br_place(web_post_tl()),
                    self.bl_place(web_post_br()),
                    self.br_place(web_post_bl()),
                ]
            )
        )

        # bottom right
        hulls.append(
            triangle_hulls(
                [
                    self.br_place(web_post_tr()),
                    self.mr_place(web_post_br()),
                    self.br_place(web_post_br()),
                    self.mr_place(web_post_tr()),
                ]
            )
        )
        # top right
        hulls.append(
            triangle_hulls(
                [
                    self.mr_place(web_post_bl()),
                    self.tl_place(web_post_br()),
                    self.mr_place(web_post_tl()),
                    self.tl_place(web_post_tr()),
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    key_place(web_post_br(), 1, cornerrow),
                    key_place(web_post_tl(), 2, lastrow),
                    key_place(web_post_bl(), 2, cornerrow),
                    key_place(web_post_tr(), 2, lastrow),
                    key_place(web_post_br(), 2, cornerrow),
                    key_place(web_post_bl(), 3, cornerrow),
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    key_place(web_post_tr(), 3, lastrow),
                    key_place(web_post_br(), 3, lastrow),
                    key_place(web_post_tr(), 3, lastrow),
                    key_place(web_post_bl(), 4, cornerrow),
                ]
            )
        )

        return union(hulls)

        # todo update walls for wild track, still identical to orbyl

    def walls(self, side="right"):
        print('thumb_walls()')
        # thumb, walls
        shape = wall_brace(
            self.mr_place, .5, 1, web_post_tl(),
            (lambda sh: key_place(sh, 3, lastrow)), 0, -1, web_post_bl(),
        )
        shape = union([shape, wall_brace(
            self.mr_place, .5, 1, web_post_tl(),
            self.mr_place, .5, 1, web_post_tr(),
        )])
        # BOTTOM FRONT BETWEEN MR AND BR
        shape = union([shape, wall_brace(
            self.mr_place, .5, 1, web_post_tr(),
            self.br_place, 0, -1, web_post_br(),
        )])
        # BOTTOM FRONT AT BR
        shape = union([shape, wall_brace(
            self.br_place, 0, -1, web_post_br(),
            self.br_place, 0, -1, web_post_bl(),
        )])
        # BOTTOM FRONT BETWEEN BR AND BL
        shape = union([shape, wall_brace(
            self.br_place, 0, -1, web_post_bl(),
            self.bl_place, 0, -1, web_post_br(),
        )])
        # BOTTOM FRONT AT BL
        shape = union([shape, wall_brace(
            self.bl_place, 0, -1, web_post_br(),
            self.bl_place, -1, -1, web_post_bl(),
        )])
        # TOP LEFT BEHIND TRACKBALL
        shape = union([shape, wall_brace(
            self.track_place, -1.5, 0, self.tb_post_tl(),
            (lambda sh: left_key_place(sh, lastrow - 1, -1, side=ball_side, low_corner=True)), -1, 0, web_post(),
        )])
        # LEFT OF TRACKBALL
        shape = union([shape, wall_brace(
            self.track_place, -2, 0, self.tb_post_tl(),
            self.track_place, -2, 0, self.tb_post_l(),
        )])
        shape = union([shape, wall_brace(
            self.track_place, -2, 0, self.tb_post_l(),
            self.bl_place, -1, 0, web_post_tl(),
        )])
        shape = union([shape, wall_brace(
            self.track_place, -2, 0, self.tb_post_l(),
            self.bl_place, -1, 0, web_post_bl(),
        )])
        # BEFORE BTUS
        #
        # # LEFT OF TRACKBALL
        # shape = union([shape, wall_brace(
        #     self.track_place, -1.5, 0, self.tb_post_tl(),
        #     self.track_place, -1, 0, self.tb_post_l(),
        # )])
        # shape = union([shape, wall_brace(
        #     self.track_place, -1, 0, self.tb_post_l(),
        #     self.bl_place, -1, 0, web_post_tl(),
        # )])

        shape = union([shape, wall_brace(
            self.bl_place, -1, 0, web_post_tl(),
            self.bl_place, -1, -1, web_post_bl(),
        )])

        return shape

    def connection(self, side='right'):

        print('thumb_connection()')
        # clunky bit on the top left thumb connection  (normal connectors don't work well)
        hulls = []

        # ======= These two account for offset between plate and wall methods
        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_tl()),
                    self.tl_wall(web_post_tl()),
                    self.tl_place(web_post_tr()),
                    self.tl_place(web_post_tl())
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(web_post_tr()),
                    self.tl_wall(web_post_tr()),
                    self.tl_place(web_post_tl()),
                    self.tl_place(web_post_tr())
                ]
            )
        )
        #  ==========================

        hulls.append(
            triangle_hulls(
                [
                    key_place(web_post_bl(), 0, cornerrow),
                    left_key_place(web_post(), lastrow - 1, -1, side=side, low_corner=True),
                    # left_key_place(translate(web_post(), wall_locate1(-1, 0)), cornerrow, -1, low_corner=True),
                    self.track_place(self.tb_post_tl()),
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    key_place(web_post_bl(), 0, cornerrow),  # col 0 bottom, bottom left (at left side/edge)
                    self.tl_wall(web_post_bl()),  # top cluster key, bottom left (sort of top left)
                    key_place(web_post_bl(), 1, cornerrow),  # col 1 bottom, bottom left
                    self.tl_wall(web_post_tl())
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_wall(web_post_tl()),
                    key_place(web_post_bl(), 1, cornerrow),  # col 1 bottom, bottom right corner
                    key_place(web_post_br(), 1, cornerrow),  # col 1 bottom, bottom left corner
                    self.tl_wall(web_post_tl())
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_wall(web_post_tl()),
                    key_place(web_post_tl(), 2, lastrow),  # col 2 bottom, top left corner
                    key_place(web_post_bl(), 2, lastrow),  # col 2 bottom, bottom left corner
                    self.tl_wall(web_post_tl())
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_wall(web_post_tl()),
                    key_place(web_post_tl(), 2, lastrow),  # col 2 bottom, top left corner
                    key_place(web_post_br(), 1, cornerrow),  # col 2 bottom, bottom left corner
                    self.tl_wall(web_post_tl())
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_wall(web_post_tl()),
                    key_place(web_post_bl(), 2, lastrow),  # col 2 bottom, top left corner
                    self.tl_wall(web_post_tr()),  # col 2 bottom, bottom left corner
                    self.tl_wall(web_post_tl())
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_wall(web_post_tr()),
                    key_place(web_post_bl(), 2, lastrow),  # col 2 bottom, top left corner
                    key_place(web_post_br(), 2, lastrow),  # col 2 bottom, top left corner
                    self.tl_wall(web_post_tr())  # col 2 bottom, bottom left corner
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_wall(web_post_tr()),
                    key_place(web_post_br(), 2, lastrow),  # col 2 bottom, top left corner
                    key_place(web_post_bl(), 3, lastrow),  # col 2 bottom, top left corner
                    self.tl_wall(web_post_tr())  # col 2 bottom, bottom left corner
                ]
            )
        )

        hulls.append(
            triangle_hulls(
                [
                    self.tl_wall(web_post_tr()),
                    key_place(web_post_bl(), 3, lastrow),  # col 2 bottom, top left corner
                    self.mr_wall(web_post_tl()),
                    self.tl_wall(web_post_tr())  # col 2 bottom, bottom left corner
                ]
            )
        )

        # Duplicate of above, just offset by x: -0.5 to ensure wall thickness
        hulls.append(
            translate(triangle_hulls(
                [
                    self.tl_wall(web_post_tr()),
                    key_place(web_post_bl(), 3, lastrow),  # col 2 bottom, top left corner
                    self.mr_wall(web_post_tl()),
                    self.tl_wall(web_post_tr())  # col 2 bottom, bottom left corner
                ]
            ), [-0.5, 0, 0])
        )

        # hulls.append(
        #     triangle_hulls(
        #         [
        #             self.mr_wall(web_post_tr()),
        #             self.mr_wall(web_post_tl()),
        #             translate(self.mr_wall(web_post_tl()), [14, 15, -2]),
        #             self.mr_wall(web_post_tr()),
        #         ]
        #     )
        # )
        #
        # # Duplicate of above, just offset by x: -0.5 to ensure wall thickness
        # hulls.append(
        #     translate(triangle_hulls(
        #         [
        #             self.mr_wall(web_post_tr()),
        #             self.mr_wall(web_post_tl()),
        #             translate(self.mr_wall(web_post_tl()), [14, 15, -2]),
        #             self.mr_wall(web_post_tr()),
        #         ]
        #     ), [-0.5, 0, 0])
        # )

        hulls.append(
            triangle_hulls(
                [
                    key_place(web_post_br(), 2, lastrow),

                    key_place(web_post_bl(), 3, lastrow),
                    key_place(web_post_tr(), 2, lastrow),
                    key_place(web_post_tl(), 3, lastrow),
                    key_place(web_post_bl(), 3, cornerrow),
                    key_place(web_post_tr(), 3, lastrow),
                    key_place(web_post_br(), 3, cornerrow),
                    key_place(web_post_bl(), 4, cornerrow),
                ]
            )
        )
        shape = union(hulls)
        return shape


    def thumb_fx_layout(self, shape):
        return union([])

    def thumbcaps(self, side='right'):
        t1 = self.thumb_1x_layout(sa_cap(1))
        return t1
