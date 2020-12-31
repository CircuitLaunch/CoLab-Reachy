from .speechrecognition import DeepSpeech

def main():
    node = None
    try:
        node = DeepSpeech("deepspeech", vad_aggressiveness=0, device=1, rate=16000)
        node.run()
    except KeyboardInterrupt:
        if node is not None:
            node.stop()

if __name__ == "__main__":
    main()