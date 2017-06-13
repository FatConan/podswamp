"""Entry point for Podswamp"""

from __future__ import print_function
import argparse
import os

from podswamp.process import process_from_config


def main(args=None):
    """Entry point function for Stone"""
    parser = argparse.ArgumentParser(
        prog='podswamp', description='Podswamp podcast site generator')

    # Add general arguments after subparsers so the order makes sense
    parser.add_argument("site_root", help='website root directory')
    args = parser.parse_args()

    if not os.path.isdir(args.site_root):
        print("[ERROR] %s is not a directory" % args.site_root)
        parser.print_help()
        return 1

    process_from_config(args.site_root)

if __name__ == '__main__':
    main()
