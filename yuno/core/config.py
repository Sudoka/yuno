"""Config controller. Other modules should `from yuno.core.config import config`
to get the settings as a global object. At some point early on, something
somewhere (normally yuno.py) needs to `load_default()` or `load_json()` to
load whatever settings it wants.
"""

import json

from yuno.core.errors import *
from yuno.core.util import decomment_json


class ConfigNamespace(object):
    """A kind-of-smart container for config settings that can throw the right
    exceptions when something goes wrong. That way people know what they did
    wrong when they delete a setting and the whole program explodes.
    """
    def __getattr__(cls, name):
        raise UndefinedConfigKey(name)


def load_json(filename):
    """Add the contents of the JSON file to the config object, overwriting
    the existing key on name collisions.
    """
    try:
        config_file = open(filename)
        settings = json.loads(decomment_json(config_file.read()))

        for k, v in settings.iteritems():
            setattr(config, k, v)

    except ValueError:
        # The message they'll get here is singularly useless. Herp derp, there's
        # an error somewhere in your file. Good luck!
        raise ConfigParseError(filename)
    except IOError:
        raise ConfigLoadError(filename)
    finally:
        config_file.close()


def load_default():
    load_json('settings/config.json')


# Run this out here so the first module to `import config` creates the real
# config object for others to import.
config = ConfigNamespace()
