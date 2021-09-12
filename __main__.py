"""
    forku CLI
    ====================================
    
    -l, --library
        name of target library in the virtual environment

"""

import argparse
import os

from . import forku


def parse_args():
    parser = argparse.ArgumentParser(add_help=False,
                                     prog="forku",
                                     usage="%(prog)s [options]",
                                     description="Fork a patched library from your virtual environment")
    parser.add_argument('-l', '--library', help="Attempts to make fork with patched changes", type=str)
    parser.add_argument('-h', '--help', action='store_true')  # launch the repo readme
    parser.add_argument('-p', '--path', help="change the path to the default venv", type=str)
    parser.add_argument('-v', '--version', action='store_true')
    return parser.parse_args()


def do_things(arguments):

    if arguments.library is not None:
        print('forku will attempt to make a fork with your patches:')
        forku.run(arguments.library)

    if arguments.path is not None:
        forku.DEFAULT_VENV = arguments.path
        
    if arguments.help is True:
        import webbrowser
        webbrowser.open_new("https://github.com/byteface/forku")

    if arguments.version is True:
        from forku import __version__
        print(__version__)
        return __version__


if __name__ == "__main__":
    args = parse_args()
    do_things(args)
