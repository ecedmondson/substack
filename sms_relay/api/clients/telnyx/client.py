import telnyx
from settings.relay_settings import TelnyxSettings

telnyx.log = 'debug'


class TelnyxClient:
    def __init__(self):
        self.settings = TelnyxSettings()
        telnyx.api_key = self.settings.TELNYX_API_KEY.get_secret_value()
    
    def list_profiles(self):
        return telnyx.MessagingProfile.list()
    
    def get_message(self, uuid):
        return telnyx.Message.retrieve(uuid)

client = TelnyxClient()

print(client.get_message("8b622800-64f7-4513-8491-9440136d33af"))