import platform

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
