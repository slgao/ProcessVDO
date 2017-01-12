import argparse

def get_args(args=None):
    parser = argparse.ArgumentParser(description = 'Write CSV files from VDOs and/or elvaluate the VDOs and/or' +
        ' save linear camera images for a given external counter range.')
    parser.add_argument("-C", "--use-cams", help="list of to be used cams (any combination from '60, 61, 62, 64, 65, 70, 71, 72, 74, 75, c50, c51')",
                        nargs='+'
                        )
    parser.add_argument("-D", "--debug", help="debug mode",
                        action="store_true")
    parser.add_argument("-E", "--eval", help="evaluate the output csv files",
                        action="store_true")
    parser.add_argument("-EM", "--eval-multi", help="evaluate the output csv files in multiple directories",
                        action="store_true")
    parser.add_argument("-L", "--load", help="load",
                        action="store_true")
    parser.add_argument("-CSV", "--write-csv", help="write csv data for vdo files",
                        action="store_true")    
    parser.add_argument("-CA", "--camera-all", help="select all camera IDs",
                        action="store_true")
    parser.add_argument("-S", "--save", help="save analyse graph",
                        nargs='*')
    parser.add_argument("-ImExp", "--img-export", help = "export images of given CamId (in cur dir if -d is not set)",
                        nargs = '*')
    parser.add_argument("-AE", "--AbExtCounter", help="Save the external count from which the rest of the external counts absent",
                        action="store_true")
    parser.add_argument("-J", "--Jumping", help="Save external counts whose next external counts have big jumps",
                        action="store_true")
    parser.add_argument("-F", "--FrameInfo", help="Save Frame numbers (should and real) for each camera",
                        action="store_true")
    parser.add_argument('arg', nargs = '+', type = str, 
                        help = 'Argument: [directory [directory [...]]]"')
    args = parser.parse_args(args=args)
    return args
