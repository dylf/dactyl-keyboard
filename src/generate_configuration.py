import sys
import getopt
import os
import json


pi = 3.14159
d2r = pi / 180
r2d = 180 / pi

shape_config = {

    'ENGINE': 'solid', # 'solid' = solid python / OpenSCAD, 'cadquery' = cadquery / OpenCascade
    # 'ENGINE':  'cadquery', # 'solid' = solid python / OpenSCAD, 'cadquery' = cadquery / OpenCascade


    ######################
    ## Shape parameters ##
    ######################

    'save_dir': '.',
    'config_name':  "DM",

    'show_caps':  False,

    'nrows':  5, #5,  # key rows
    'ncols':  6, #6,  # key columns

    'alpha':  pi / 12.0,  # curvature of the columns
    'beta':  pi / 36.0,  # curvature of the rows
    'centercol':  3,  # controls left_right tilt / tenting (higher number is more tenting)
    'centerrow_offset':  3,  # rows from max, controls front_back tilt
    'tenting_angle':  pi / 12.0,  # or, change this for more precise tenting control

    # symmetry states if it is a symmetric or asymmetric bui.  If asymmetric it doubles the generation time.
    'symmetry':  "symmetric",  # "asymmetric" or "symmetric"

    'column_style_gt5':  "orthographic",
    'column_style':  "standard",  # options include :standard, :orthographic, and :fixed

    'thumb_offsets':  [6, -3, 7],
    'keyboard_z_offset':  (
        11  # controls overall height# original=9 with centercol=3# use 16 for centercol=2
    ),

    ##############################
    # THUMB PARAMETERS
    ##############################
    'thumb_style': 'MINIDOX',  # 'DEFAULT' 6-key, 'MINI' 5-key, 'CARBONFET' 6-key, 'MINIDOX' 3-key
    'default_1U_cluster': True, # only used with default, makes top right thumb cluster key 1U
    'minidox_Usize': 1.6
    , # Thumb key size.  May need slight oversizing, check w/ caps.  Additional spacing will be automatically added for larger keys.

    # Thumb plate rotations, anything other than 90 degree increments WILL NOT WORK.
    'thumb_plate_tr_rotation': 0.0,  # Top right plate rotation tweaks as thumb cluster is crowded for hot swap, etc.
    'thumb_plate_tl_rotation': 0.0,  # Top left plate rotation tweaks as thumb cluster is crowded for hot swap, etc.
    'thumb_plate_mr_rotation': 0.0,  # Mid right plate rotation tweaks as thumb cluster is crowded for hot swap, etc.
    'thumb_plate_ml_rotation': 0.0,  # Mid left plate rotation tweaks as thumb cluster is crowded for hot swap, etc.
    'thumb_plate_br_rotation': 0.0,  # Bottom right plate rotation tweaks as thumb cluster is crowded for hot swap, etc.
    'thumb_plate_bl_rotation': 0.0,  # Bottom right plate rotation tweaks as thumb cluster is crowded for hot swap, etc.

    ##############################
    # EXPERIMENTAL PARAMETERS
    ##############################
    'pinky_1_5U': False,  # LEAVE AS FALSE, CURRENTLY BROKEN
    'first_1_5U_row': 0,
    'last_1_5U_row': 5,
    ##############################


    'extra_width':  2.5,  # extra space between the base of keys# original= 2
    'extra_height':  1.0,  # original= 0.5

    'wall_z_offset':  15,  # length of the first downward_sloping part of the wall
    'wall_x_offset':  5,  # offset in the x and/or y direction for the first downward_sloping part of the wall (negative)
    'wall_y_offset':  6,  # offset in the x and/or y direction for the first downward_sloping part of the wall (negative)
    'left_wall_x_offset':  12,  # specific values for the left side due to the minimal wall.
    'left_wall_z_offset':  3,  # specific values for the left side due to the minimal wall.
    'left_wall_lower_y_offset': 0,  # specific values for the lower left corner.
    'left_wall_lower_z_offset': 0,
    'wall_thickness':  4.5,  # wall thickness parameter used on upper/mid stage of the wall
    'wall_base_y_thickness':  4.5,  # wall thickness at the lower stage
    'wall_base_x_thickness':  4.5,  # wall thickness at the lower stage

    'wall_base_back_thickness':  4.5,  # wall thickness at the lower stage in the specifically in back for interface.

    ## Settings for column_style == :fixed
    ## The defaults roughly match Maltron settings
    ##   http://patentimages.storage.googleapis.com/EP0219944A2/imgf0002.png
    ## fixed_z overrides the z portion of the column ofsets above.
    ## NOTE: THIS DOESN'T WORK QUITE LIKE I'D HOPED.
    'fixed_angles':  [d2r * 10, d2r * 10, 0, 0, 0, d2r * -15, d2r * -15],
    'fixed_x':  [-41.5, -22.5, 0, 20.3, 41.4, 65.5, 89.6],  # relative to the middle finger
    'fixed_z':  [12.1, 8.3, 0, 5, 10.7, 14.5, 17.5],
    'fixed_tenting':  d2r * 0,

    #################
    ## Switch Hole ##
    #################

    # plate options are
    # 'HOLE' = a square hole.  Also useful for applying custom plate files.
    # 'NUB' = original side nubs.
    # 'UNDERCUT' = snap fit undercut.  May require CLIP_THICKNESS and possibly CLIP_UNDERCUT tweaking
    #       and/or filing to get proper snap.
    # 'NOTCH' = snap fit undercut only near switch clip.  May require CLIP_THICKNESS and possibly CLIP_UNDERCUT
    #       tweaking and/or filing to get proper snap.
    # 'HS_NUB' = hot swap underside with nubs.
    # 'HS_UNDERCUT' = hot swap underside with undercut. Does not generate properly.  Hot swap step needs to be modified.
    # 'HS_NOTCH' = hot swap underside with notch.  Does not generate properly.  Hot swap step needs to be modified.
    # 'plate_style':  'NUB',
    'plate_style': 'NOTCH',

    'hole_keyswitch_height':  14.0,
    'hole_keyswitch_width':  14.0,

    'nub_keyswitch_height':  14.4,
    'nub_keyswitch_width':  14.4,

    'undercut_keyswitch_height':  14.0,
    'undercut_keyswitch_width':  14.0,
    'notch_width': 5.0, # If using notch, it is identical to undecut, but only locally by the switch clip

    'sa_profile_key_height':  12.7,
    'sa_length': 18.5,
    'sa_double_length': 37.5,
    'plate_thickness':  4+1.1,

    'plate_rim': 1.5 + 0.5,
    # Undercut style dimensions
    'clip_thickness':  1.4,
    'clip_undercut':  1.0,
    'undercut_transition':  .2,  # NOT FUNCTIONAL WITH OPENSCAD, ONLY WORKS WITH CADQUERY

    # Custom plate step file
    'plate_file':  None,
    'plate_offset':  0.0,

    ##########################
    ## OLED Mount Location
    ##########################
    # Initial pass will be manual placement.  Can be used to create other mounts as well.
    # Mount type options:
    # None or 'NONE' = No OLED mount
    # 'UNDERCUT' = Simple rectangle with undercut for clip in item
    # 'SLIDING' = Features to slide the OLED in place and use a pin or block to secure from underneath.
    # 'CLIP' = Features to set the OLED in a frame a snap a bezel down to hold it in place.

    'oled_mount_type':  'CLIP',
    'oled_center_row': 1.25, # if not None, this will override the oled_mount_location_xyz and oled_mount_rotation_xyz settings
    'oled_translation_offset': (0, 0, 4), # Z offset tweaks are expected depending on curvature and OLED mount choice.
    'oled_rotation_offset': (0, 0, 0),

    'oled_configurations': {
        'UNDERCUT':{
            # Common parameters
            'oled_mount_width': 15.0,
            'oled_mount_height': 35.0,
            'oled_mount_rim': 3.0,
            'oled_mount_depth': 6.0,
            'oled_mount_cut_depth': 20.0,
            'oled_mount_location_xyz': (-80.0, 20.0, 45.0), # will be overwritten if oled_center_row is not None
            'oled_mount_rotation_xyz': (13.0, 0.0, -6.0), # will be overwritten if oled_center_row is not None
            'oled_left_wall_x_offset_override': 28.0,
            'oled_left_wall_z_offset_override': 0.0,
            'oled_left_wall_lower_y_offset': 12.0,
            'oled_left_wall_lower_z_offset': 5.0,

            # 'UNDERCUT' Parameters
            'oled_mount_undercut': 1.0,
            'oled_mount_undercut_thickness': 2.0,
        },
        'SLIDING': {
            # Common parameters
            'oled_mount_width': 12.5,  # width of OLED, plus clearance
            'oled_mount_height': 25.0,  # length of screen
            'oled_mount_rim': 2.5,
            'oled_mount_depth': 8.0,
            'oled_mount_cut_depth': 20.0,
            'oled_mount_location_xyz': (-78.0, 10.0, 41.0), # will be overwritten if oled_center_row is not None
            'oled_mount_rotation_xyz': (6.0, 0.0, -3.0), # will be overwritten if oled_center_row is not None
            'oled_left_wall_x_offset_override': 24.0,
            'oled_left_wall_z_offset_override': 0.0,
            'oled_left_wall_lower_y_offset': 12.0,
            'oled_left_wall_lower_z_offset': 5.0,

            # 'SLIDING' Parameters
            'oled_thickness': 4.2,  # thickness of OLED, plus clearance.  Must include components
            'oled_edge_overlap_end': 6.5,  # length from end of viewable screen to end of PCB
            'oled_edge_overlap_connector': 5.5,  # length from end of viewable screen to end of PCB on connection side.
            'oled_edge_overlap_thickness': 2.5,  # thickness of material over edge of PCB
            'oled_edge_overlap_clearance': 2.5,  # Clearance to insert PCB before laying down and sliding.
            'oled_edge_chamfer': 2.0,
        },
        'CLIP': {
            # Common parameters
            'oled_mount_width': 12.5,  # whole OLED width
            'oled_mount_height': 39.0,  # whole OLED length
            'oled_mount_rim': 2.0,
            'oled_mount_depth': 7.0,
            'oled_mount_cut_depth': 20.0,
            'oled_mount_location_xyz': (-78.0, 20.0, 42.0), # will be overwritten if oled_center_row is not None
            'oled_mount_rotation_xyz': (12.0, 0.0, -6.0), # will be overwritten if oled_center_row is not None
            'oled_left_wall_x_offset_override': 24.0,
            'oled_left_wall_z_offset_override': 0.0,
            'oled_left_wall_lower_y_offset': 12.0,
            'oled_left_wall_lower_z_offset': 5.0,

            # 'CLIP' Parameters
            'oled_thickness': 4.2,  # thickness of OLED, plus clearance.  Must include components
            'oled_mount_bezel_thickness': 3.5,  # z thickness of clip bezel
            'oled_mount_bezel_chamfer': 2.0,  # depth of the 45 degree chamfer
            'oled_mount_connector_hole': 6.0,
            'oled_screen_start_from_conn_end': 6.5,
            'oled_screen_length': 24.5,
            'oled_screen_width': 10.5,
            'oled_clip_thickness': 1.5,
            'oled_clip_width': 6.0,
            'oled_clip_overhang': 1.0,
            'oled_clip_extension': 5.0,
            'oled_clip_width_clearance': 0.5,
            'oled_clip_undercut': 0.5,
            'oled_clip_undercut_thickness': 2.5,
            'oled_clip_y_gap': .2,
            'oled_clip_z_gap': .2,
        }
    },
    'web_thickness':  4.0,
    'post_size':  0.1,
    # post_adj':  post_size / 2
    'post_adj':  0,
    'screws_offset': 'INSIDE', #'OUTSIDE', 'INSIDE', 'ORIGINAL'

    'screw_insert_height': 3.8,
    'screw_insert_bottom_radius': 5.31 / 2,
    'screw_insert_top_radius': 5.1 / 2,

    # Does anyone even use these?  I think they just get in the way.
    'wire_post_height': 7,
    'wire_post_overhang': 3.5,
    'wire_post_diameter': 2.6,

    ###################################
    ## Controller Mount / Connectors ##
    ###################################
    # connector options are
    # 'RJ9_USB_WALL' = Standard internal plate with RJ9 opening and square cutout for connection.
    # 'USB_WALL' = Standard internal plate with a square cutout for connection, no RJ9.
    # 'RJ9_USB_TEENSY' = Teensy holder
    # 'USB_TEENSY' = Teensy holder, no RJ9
    # 'EXTERNAL' = square cutout for a holder such as the one from lolligagger.
    # 'NONE' = No openings in the back.
    'controller_mount_type':  'EXTERNAL',

    'external_holder_height':  12.5,
    'external_holder_width':  28.75,
    'external_holder_xoffset': -5.0,


    # Offset is from the top inner corner of the top inner key.

    ###################################
    ## Bottom Plate Dimensions
    ###################################
    # COMMON DIMENSION
    'screw_hole_diameter': 2,
    # USED FOR CADQUERY ONLY
    'base_thickness': 3.0, # thickness in the middle of the plate
    'base_offset': 3.0, # Both start flat/flush on the bottom.  This offsets the base up (if positive)
    'base_rim_thickness': 5.0,  # thickness on the outer frame with screws
    'screw_cbore_diameter': 4.0,
    'screw_cbore_depth': 2.0,

    # Offset is from the top inner corner of the top inner key.

    ###################################
    ## EXPERIMENTAL
    ###################################
    'plate_holes':  False,
    'plate_holes_xy_offset': (0.0, 0.0),
    'plate_holes_width': 14.3,
    'plate_holes_height': 14.3,
    'plate_holes_diameter': 1.7,
    'plate_holes_depth': 20.0,

    ###################################
    ## COLUMN OFFSETS
    ####################################

    'column_offsets':  [
        [0, 0, 0],
        [0, 0, 0],
        [0, 2.82, -4.5],
        [0, 0, 0],
        [0, -6, 5],# REDUCED STAGGER
        [0, -6, 5],# REDUCED STAGGER
        [0, -6, 5],# NOT USED IN MOST FORMATS (7th column)
    ],

}

    ####################################
    ## END CONFIGURATION SECTION
    ####################################

def save_config():
    # Check to see if the user has specified an alternate config
    opts, args = getopt.getopt(sys.argv[1:], "", ["config="]);
    for opt, arg in opts:
        if opt in ('--config'):
            # If a config file was specified, set the config_name and save_dir
            shape_config['save_dir'] = arg
            shape_config['config_name'] = arg

    # Write the config to ./configs/<config_name>.json
    with open(os.path.join(r"..", "configs", shape_config['config_name'] + '.json'), mode='w') as fid:
        json.dump(shape_config, fid, indent=4)


if __name__ == '__main__':
    save_config()