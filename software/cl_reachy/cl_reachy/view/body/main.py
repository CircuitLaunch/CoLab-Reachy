import argparse
import os
from ...util import get_curr_resource_dir
from .body import Body

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--env', dest='env', type=str, help="environment [reachy|dev]")
    args = parser.parse_args()

    node = Body("body", env=args.env)
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()