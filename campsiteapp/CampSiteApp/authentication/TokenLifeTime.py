from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.timezone import now
from datetime import timedelta

class ExpiringTokenAuthentication(TokenAuthentication):
    TOKEN_EXPIRE_TIME = 900

    @property
    def model(self):
        from CampSiteApp.models import ExpiringToken  # ленивый импорт здесь
        return ExpiringToken

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)

        expiration_time = token.created + timedelta(seconds=self.TOKEN_EXPIRE_TIME)
        if expiration_time < now():
            token.delete()
            raise AuthenticationFailed('Token has expired')

        return (user, token)
