from base_plugin import BasePlugin, MethodHook

from ui.settings import (
    Custom,
    Divider,
    EditText,
    Header,
    Input,
    Selector,
    SimpleSettingFactory,
    Switch,
    Text,
)

__id__ = "no_sensetive_info"
__name__ = "No Sensetive Info"
__description__ = "Before sending text, checks whether it contains sensetive info"
__author__ = "@gin_tonik_drink"
__icon__ = "exteraIcons/3"
__app_version__ = ">=12.5.1"
__version__ = "1.0.0"

