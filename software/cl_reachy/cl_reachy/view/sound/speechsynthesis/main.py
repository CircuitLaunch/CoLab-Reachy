import argparse
import configparser
import os
from ....util import get_curr_resource_dir
from .speechsynthesis import SpeechSynthesis

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--env', dest='env', type=str, default="reachy", help="environment")
    args = parser.parse_args()

    resource_dir = get_curr_resource_dir(__file__)

    config = configparser.ConfigParser()
    config_file = os.path.join(resource_dir, "config")
    config.read(config_file)

    ouput_device_index = int(config[args.env]['ouput_device_index'])

    node = SpeechSynthesis("speechsynthesis")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()
