import requests

from gamest.errors import InvalidConfigurationError
from gamest.plugins import NotificationService

class DiscordNotificationService(NotificationService):
    SETTINGS_TAB_NAME = "Discord"
    def __init__(self, application):
        super().__init__(application)

        self.logger.debug("DiscordNotificationService initialized."
            "\n\twebhooks: %r"
            "\n\tuser_name: %r"
            "\n\tdiscord_id: %r",
            self.webhooks, self.user_name, self.discord_id)

    @property
    def webhooks(self):
        return self.config.get('webhooks', fallback=None)

    @property
    def user_name(self):
        return self.config.get('user_name', fallback='Gamest User')

    @property
    def discord_id(self):
        return self.config.get('discord_id', fallback=None)

    @property
    def user_name_for_messages(self):
        return '<@{}>'.format(self.discord_id) if self.discord_id else self.user_name

    @classmethod
    def get_settings_template(cls):
        d = super().get_settings_template()
        d[(cls.__name__, 'webhooks')] = {
            'name' : 'Webhooks',
            'type' : 'list',
            'hint' : ("The URL of the webhook you wish to notify. To notify multiple webhooks, put "
                      "one webhook per line."),
        }
        d[(cls.__name__, 'user_name')] = {
            'name' : 'User name',
            'type' : 'text',
            'default' : 'Gamest User',
            'hint' : ("You should probably set this to your discord nickname, but it can be set to "
                      "anything. If you set a Discord ID then whenever a notification @mentions "
                      "you, it will still use your discord nickname instead of what you set here."),
        }
        d[(cls.__name__, 'discord_id')] = {
            'name' : 'Discord ID',
            'type' : 'text',
            'hint' : ("You should probably set this to your discord nickname, but it can be set to "
                      "anything. If you also set discord_id then whenever a notification @mentions "
                      "you, it will still use your discord nickname instead of what you set here."),
        }
        return d

    def notify(self, msg):
        self.logger.debug("Notify called.")
        data = { 'content' : msg.format(user_name=self.user_name_for_messages) }
        for url in self.webhooks:
            r = requests.post(url, data=data)
        try:
            r.raise_for_status()
        except:
            self.logger.exception("Failed to send Discord notification.")
