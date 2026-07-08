import platform
import sys
from openvals import __version__
def get_version_info():

    return {

        "openvals": __version__,

        "python": platform.python_version(),

        "platform": platform.system(),

        "architecture": platform.machine()
    }