import argparse
import configparser
import os
from ....util import get_curr_resource_dir
from .wakeword import WakeWord

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--env', dest='env', type=str, default="reachy", help="environment")
    args = parser.parse_args()

    resource_dir = get_curr_resource_dir(__file__)

    config = configparser.ConfigParser()
    config_file = os.path.join(resource_dir, "config")
    config.read(config_file)

    wakeword_sensitivity = float(config[args.env]['wakeword_sensitivity'])
    input_device_index = int(config[args.env]['input_device_index'])

    node = None
    try:
        # TODO: move these params to config
        node = WakeWord("wakeword", wakeword_sensitivity=wakeword_sensitivity,
                            input_device_index=input_device_index)
        node.run()
    except KeyboardInterrupt:
        if node is not None:
            node.stop()

if __name__ == "__main__":
    main()