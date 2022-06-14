from django.apps import AppConfig


class AwardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'award'

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # add this
    def ready(self):
        import signals  # noqa