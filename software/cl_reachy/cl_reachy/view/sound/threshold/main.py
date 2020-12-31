import argparse
from .threshold import Threshold

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--env', dest='env', type=str, help="environment [reachy|dev]")
    args = parser.parse_args()

    node = None

    try:
        node = Threshold("threshold", profile=args.env)
        node.run()
    except KeyboardInterrupt:
        if node is not None:
            node.stop()

if __name__ == "__main__":
    main()