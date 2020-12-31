from .speechrecognition import SpeechRecognition

def main():
    node = None
    try:
        node = SpeechRecognition("speechrecognition")
        node.run()
    except KeyboardInterrupt:
        if node is not None:
            node.stop()

if __name__ == "__main__":
    main()