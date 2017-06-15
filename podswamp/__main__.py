"""Entry point for Podswamp"""

from __future__ import print_function
import argparse
import os

from podswamp.process import process_from_config
from podswamp.configuration import Config

def main(args=None):
    """Entry point function for Stone"""
    install_location = os.path.dirname(__file__)

    parser = argparse.ArgumentParser(
        prog='podswamp', description='Podswamp podcast site generator')

    # Add general arguments after subparsers so the order makes sense
    parser.add_argument("project_root", help='Podswamp project root directory')
    args = parser.parse_args()

    if not os.path.isdir(args.project_root):
        print("[ERROR] %s is not a directory" % args.site_root)
        parser.print_help()
        return 1

    config = Config(args.project_root, install_location)
    process_from_config(config)

if __name__ == '__main__':
    main()
