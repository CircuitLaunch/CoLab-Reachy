import argparse
import configparser
import os
from .speechrecognition import DeepSpeech
from .....util import get_curr_resource_dir

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--env', dest='env', type=str, help="environment [reachy|dev]")
    args = parser.parse_args()

    resource_dir = get_curr_resource_dir(__file__)

    config = configparser.ConfigParser()
    config_file = os.path.join(resource_dir, "config")
    config.read(config_file)

    vad_aggressiveness = int(config[args.env]['vad_aggressiveness'])
    input_device_index = int(config[args.env]['input_device_index'])
    rate = int(config[args.env]['rate'])

    node = None
    try:
        node = DeepSpeech("deepspeech", vad_aggressiveness=vad_aggressiveness,
                            input_device_index=input_device_index ,
                            rate=rate)
        node.run()
    except KeyboardInterrupt:
        if node is not None:
            node.stop()

if __name__ == "__main__":
    main()