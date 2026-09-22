from typing import Any, List
import re
from org.telegram.ui.Components import UItem
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
from ui.alert import AlertDialogBuilder
from client_utils import get_last_fragment

__id__ = "no_sensetive_info"
__name__ = "No Sensetive Info"
__description__ = "Before sending text, checks whether it contains sensetive info"
__author__ = "@tg"
__icon__ = "exteraIcons/3"
__app_version__ = ">=12.5.1"
__version__ = "0.0.1"
EN = {

}
RU = {
    "opt_h_locale": "Настройки локализации",
    "opt_h_datatype": "Настройки типов данных",
    "opt_h_filter": "Настройки фильтров",
    "opt_h_ai": "Настройки ИИ",
    "opt_se_language": "Язык",
    "opt_sw_prompt": "Если найдена личная информация при отправке, оповестить пользователя",
    "opt_sw_stext_prompt": "В отключённом состоянии отменяет сообщение с личной информацией",
    "opt_sw_verify_text": "Проверять текст",
    "opt_sw_verify_images": "Проверять фотки",
    "opt_sw_verify_voice": "Проверять голосовые сообщения",
    "opt_sw_verify_video": "Проверять видеосообщения",
    "opt_sw_st_ai_req": "Нужна ИИ-модель",
    "opt_sw_whitelist": "Включить белый список на текст",
    "opt_text_filter_hint": "",
    "opt_et_filter": "",
    "opt_et_nlp_api": "",
    "opt_et_image_api": "",
    "opt_et_audio_api": "",
    "opt_et_video_api": ""

}


class NSIPlugin(BasePlugin):
    
    def __init__(self):
        super().__init__()
        self.lang = self.get_setting("language_key")        
        self.prompt_user = self.get_setting("prompt_user_key")

        self.verify_text = self.get_setting("verify_text_key")
        self.verify_images = self.get_setting("verify_images_key")
        self.verify_voice_messages = self.get_setting("verify_voice_messages_key")
        self.verify_video_messages = self.get_setting("verify_video_messages_key")
        
        self.is_whitelist = self.get_setting("whitelist_key")
        self.raw_filter = self.get_setting("filter_key")

    def on_language_change(self, new):
        self.current_language = new

    def on_prompt_user_change(self, new):
        self.prompt_user = new

    def on_verify_text_change(self, new):
        self.verify_text = new
    
    def on_verify_images_change(self, new):
        self.verify_images = new
    
    def on_verify_voice_change(self, new):
        self.verify_voice_messages(self, new)
    
    def on_verify_video_change(self, new):
        self.verify_video_messages = new
    
    def on_whitelist_change(self, new):
        self.is_whitelist = new

    def on_plugin_load(self):
        pass

    def on_plugin_unload(self):
        self.verify_msg_text()
    
    def verify_msg_text(self) -> None:
        filters = [
            self.get_setting("name_filters_key"),
            self.get_setting("phone_filters_key"),
            self.get_setting("address_filters_key"),
            self.get_setting("email_filters_key"),
            self.get_setting("ip_filters_key"),
            self.get_setting("domain_filters_key"),
            self.get_setting("nicknames_filters_key"),
            self.get_setting("music_filters_key"),
            self.get_setting("other_filters_key"),
        ]
        self.log(filters)
        for filter in filters:
            pattern = re.compile(f"*{filter}*")
            self.log(f"{re.search(pattern)} detected")

    def create_settings(self) -> List[Any]:
        return [
            Header(text="Localization settings"),
            Selector(key="language_key",text="Language", items=["English", "Russian"],default=0,on_change=self.on_language_change),
            Divider(),

            Header(text="Interaction settings"),
            Switch(
                key="prompt_user_key",
                text="Prompt user, if found sensetive info", subtext="In disabled state cancels messages with sensetive info",
                default=True,
                on_change=self.on_prompt_user_change),
            Divider(),

            Header(text="Datatype settings"),
            Switch(
                key="verify_text_key",
                text="Verify text",
                default=True,
                on_change=self.on_verify_text_change),
            Switch(
                key="verify_images_key",
                text="Verify images",
                subtext="Requires AI-model",
                default=False,
                on_change=self.on_verify_images_change),
            Switch(
                key="verify_voice_messages_key",
                text="Verify voice messages",
                subtext="Requires AI-model",
                default=False,
                on_change=self.on_verify_voice_change),
            Switch(
                key="verify_video_messages_key",
                text="Verify video messages",
                subtext="Requires AI-model",
                default=False,
                on_change=self.on_verify_video_change),
            Divider(),

            Header(text="Filter settings"),
            Switch(key="whitelist_key", text="Turn on whitelist on text",default=False,on_change=self.on_whitelist_change),
            # Text(text="Show filtering guide"), TODO Open popup view with guide
            Input(key="name_filters_key",text="Name Filter",default="John|John*Williams|Williams",subtext="123"),
            Input(key="phone_filters_key",text="Phone Filter", default="+888*888*88*88"),
            Input(key="address_filters_key",text="Address Filter",default="green st|red st"),
            Input(key="email_filters_key",text="Email Filter", default="john@williams.me|mygoogle@gmail.com"),
            Input(key="ip_filters_key",text="IP Filter", default="1.2.3.4"),
            Input(key="domain_filters_key",text="Domain Filter",default="*williams.me||private.filter.com"),
            Input(key="nicknames_filters_key",text="Nickname Filter",default="heresjohnny|famous_nickname228"),
            Input(key="music_filters_key",text="Music Filter", default="metallica|dora"),
            Input(key="other_filters_key",text="Other Filters", default="etg|ayugram|ayu||exteragram|"),
            #TODO Instead of other_filters_key here should be "Add own regex class"

            Divider(),

            Header(text="AI settings"),
            EditText(key="nlp_model_api_key",hint="Enter api key for text processing"),
            EditText(key="image_model_api_key",hint="Enter api key for image processing"),
            EditText(key="audio_model_api_key",hint="Enter api key for voice message processing"),
            EditText(key="video_model_api_key",hint="Enter api key for video processing"),
            Text(text="Test regex", on_click=self.verify_msg_text)
            
        ]