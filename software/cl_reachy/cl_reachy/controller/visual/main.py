import argparse
import configparser
import os
from ...util import get_curr_resource_dir
from .camera import CameraController

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--env', dest='env', type=str, default="reachy", help="environment")
    args = parser.parse_args()

    resource_dir = get_curr_resource_dir(__file__)

    config = configparser.ConfigParser()
    config_file = os.path.join(resource_dir, "config")
    config.read(config_file)

    show_frames = int(config[args.env]['show_frames'])

    node = CameraController("camera", show_frames=show_frames)
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()
