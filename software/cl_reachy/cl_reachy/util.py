import platform
import pyaudio

INTEL = "intel"
RASPBERRYPI = "raspberry pi"
UNKNOWN = "unknown"

def get_platform():
    if platform.uname().processor == 'x86_64':
        return INTEL
    elif platform.uname().machine == 'armv7l':
        return RASPBERRYPI
    else:
        raise UNKNOWN

def get_input_devices():
    audio = pyaudio.PyAudio()

    input_devices = {}
    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            input_devices[i] = audio.get_device_info_by_host_api_device_index(0, i).get('name')

    return input_devices

def is_valid_input_device(input_device_index):
    input_devices = get_input_devices()

    return (input_device_index in input_devices.keys())
