# there's tons of magic numbers here because 
# exported a semi-done parametric version from clojure
# and didn't fix all the formulas for x and y translates....
# before getting it fully working and for getting how the working scad version
# diverged from the clojure version.......................
#
# sorry future person trying to change this, you will need 
# a strong dragon spear to modify any 'kinda adjustable' values 
from helpers_solid import *

reset_holder = True

usb_holder_x = 30.6       # kinda adjustable
usb_holder_y = 38.8       # kinda adjustable
usb_holder_z = 15 if reset_holder else 8.4        # kinda adjustable

usb_holder_border = 1.5   # kinda adjustable

#* this combination of controller and usb_c dimensions 
# friction fits both generations of elite-c controllers 
usb_elite_c_x = 18.7      # kinda adjustable
usb_elite_c_y = 33.4      # mostly adjustable
usb_elite_c_side_cut = 6  # adjustable

usb_c_x = 9.3             # adjustable
usb_c_z = 4.5             # kinda adjustable

trrs_x = 6.2              # mostly adjustable
trrs_y = 12.5             # kinda adjustable
trrs_r = 2.55             # adjustable

usb_holder_center_x = usb_holder_x / 2
usb_holder_center_y = usb_holder_y / 2
usb_holder_center_z = usb_holder_z / 2

usb_holder_notch_xy = usb_holder_border
usb_holder_notch_down = usb_holder_border * usb_holder_notch_xy
usb_holder_notch_half = usb_holder_notch_xy / 2

# $fn = 100

def basic_shape():
    left_cut_x = 2 * usb_holder_border
    left_cut_y = 3 * usb_holder_border

    bottom_cut_x = (left_cut_x + trrs_x)
    bottom_cut_y = (left_cut_x + trrs_x)

    cut1_x = (usb_holder_center_x - usb_holder_border)
    cut1_y = (usb_holder_center_y - (usb_holder_center_y - left_cut_y / 2))

    cut2_x = (usb_holder_center_x - (bottom_cut_x / 2))
    # cut2_y = (usb_holder_center_y - (- usb_holder_center_y(16.6 / 2)))
    top_cut_adjust = 1.75 * usb_holder_border if reset_holder is not None else usb_holder_border

    shape = difference(
      # basic starting shape to cut away from
      # cube([usb_holder_x, usb_holder_y, usb_holder_z], center=true)
      box(usb_holder_x, usb_holder_y, usb_holder_z),
      [
          union([
            translate(
                box(left_cut_x, (usb_holder_y - left_cut_y), 99),
                [-cut1_x, -cut1_y, 0]
            ),
            translate(
                box(bottom_cut_x, (usb_holder_y - 16.6), 99),
                [-cut2_x, -8.3, 0]
            ),
            rotate(
                translate(box(usb_holder_x, usb_holder_y, usb_holder_z), [0, -(usb_holder_border * 3), (usb_holder_z / top_cut_adjust)]),
                [8, 0, 0])
            ]
          )
        ]
    )
    
    # side notches that key into other object
    notch_x = (usb_holder_center_x - usb_holder_notch_half)
    notch_y = (usb_holder_center_y - usb_holder_notch_down)
    # shape = union([shape, translate(notch(), [notch_x, notch_y, 0])])
    shape = difference(shape, [translate(notch(), [-notch_x, notch_y, 0]), translate(notch(), [notch_x, notch_y, 0])])
    return shape
  

def notch():
    return box(usb_holder_notch_xy, usb_holder_notch_xy, 99)


def trrsCutouts():
    trrs_floor = 1
    trrs_squareCutoutHeight = 12
    trrs_squareCutoutHeightOffset = trrs_floor - usb_holder_center_z + trrs_squareCutoutHeight/2
    shape = translate(
        box(trrs_x, trrs_y, trrs_squareCutoutHeight),
        [-9.2, 11.65, trrs_squareCutoutHeightOffset]
    )

    trrsAngle_z_adjust = 0.5 if not reset_holder else 4
    trrsAngle_z_factor = 0.5 if not reset_holder else 1

    shape = union([
        shape,
        translate(
            rotate(
                box(trrs_x, trrs_y, usb_holder_z * trrsAngle_z_factor),
                [-72, 0, 0]),
            [-9.2, 11.65-trrs_y/3, trrsAngle_z_adjust * usb_holder_border]
        )
    ])


    trrs_y_offset = (usb_holder_center_y - (usb_holder_border / 2) +0.01)
    trrs_z_offset = (usb_holder_center_z - (trrs_floor + trrs_r))
    shape = union([
        shape,
        translate(
            rotate(cylinder(usb_holder_border * 2, trrs_r), [90, 0, 0]),
            [-9.1, trrs_y_offset, -trrs_z_offset]
        )
    ])

    return shape


def resetCutout():
    reset_xz = 7.1
    reset_y = 4.5
    reset_floor = usb_holder_z / 1.5
    reset_r = 1.75

    reset_x_offset = usb_holder_center_x - usb_elite_c_x / 2 - usb_holder_border
    reset_y_offset = usb_holder_center_y - usb_elite_c_y - usb_holder_border
    reset_z_offset = usb_holder_center_z - (reset_floor + reset_r)

    shape = translate (box(reset_xz, reset_y, reset_xz),
        [reset_x_offset, -reset_y_offset, -reset_z_offset])

    shape = union([
        shape,
        translate(
            rotate(cylinder(99, reset_r), [90, 0, 0]),
            [reset_x_offset, 0, -reset_z_offset]
        )
    ])

    return shape


def circuitBoardSlots():
    return box(usb_elite_c_side_cut, usb_elite_c_y, 99)


def usbPortCutout():
    usbPortCenter = ((usb_holder_center_x - (usb_elite_c_x/2)) - usb_holder_border)
    usbPortCenterCut = (usb_c_x - usb_c_z)
    usbPortSideOffset = usbPortCenterCut / 2
    usbPortCenterCutLength = 35

    shape = translate(
        rotate (
            cylinder (usbPortCenterCutLength, usb_c_z/2),
            [90, 0, 0]),
        [(usbPortCenter - usbPortSideOffset), 0, 0])



    shape = union([
        shape,
        translate(box(usbPortCenterCut, usbPortCenterCutLength, usb_c_z), [usbPortCenter, 0, 0]),
        translate(
            rotate(
                cylinder(usbPortCenterCutLength, usb_c_z/2),
                [90, 0, 0]),
            [(usbPortCenter + usbPortSideOffset), 0, 0]
        )
    ])

    return shape


def usbRecessCutout():
    usb_c_cover_plate = usb_holder_border
    recess_y = (usb_holder_y - usb_elite_c_y - usb_holder_border - usb_c_cover_plate)
    recess_z = 8
    shape = translate(
        union([
            translate(
                rotate(
                    cylinder(recess_y, 3.25),
                    [90, 0, 0]),
                [0, 0, 0]
            ),
            translate(
                box(12.5, recess_y, recess_z),
                [(+(usb_holder_center_x - (usb_elite_c_x / 2)) - usb_holder_border), 0, 0]
            ),
            translate(
                rotate(
                    cylinder(recess_y, 3.25),
                    [90, 0, 0]),
                [usb_c_x, 0, 0]
            )
        ]),
        [0, (usb_holder_center_y - (recess_y / 2) + 0.01), 0]
    )

    return shape


def eliteC():
    x_offset = ( (usb_holder_center_x - (usb_elite_c_x / 2)) - usb_holder_border)
    y_offset = (-(usb_holder_center_y - (usb_elite_c_y / 2)) + usb_holder_border)
    z_offset = usb_holder_border

    left_cut_x  = ((usb_holder_center_x - (usb_elite_c_x / 2)) - ((usb_elite_c_x / 2) - (usb_elite_c_side_cut / 2)) - usb_holder_border)
    right_cut_x = ((usb_holder_center_x - (usb_elite_c_x / 2)) + ((usb_elite_c_x / 2) - (usb_elite_c_side_cut / 2)) - usb_holder_border)

    usbPort_z_adjust = -3.6 if reset_holder else -0.3

    shape = translate(box(usb_elite_c_x, usb_elite_c_y, usb_holder_z),
                [x_offset, y_offset, z_offset])

    shape = union([
        shape,
        translate(circuitBoardSlots(), [left_cut_x , y_offset, 0]),
        translate(circuitBoardSlots(), [right_cut_x, y_offset, 0]),
        translate(
            union([usbPortCutout(), usbRecessCutout()]), [0, 0, usbPort_z_adjust])
    ])

    return shape


def usb_holder():
    # adjust origin to front fact, bottom, mostly to match existing STLs
    shape = basic_shape()
    shape = translate(shape, [0, -(usb_holder_y/2), (usb_holder_z/2)])
    shape = difference(shape,
                       [trrsCutouts(),
                        eliteC(),
                        resetCutout()]
                       )
    return shape


shape = usb_holder()

export_file(shape, "../things/holder_test.scad")
