from mozilla_django_oidc.contrib.drf import OIDCAuthentication



class KeycloakAuthentication(OIDCAuthentication):
    """Проверка авторизации через Keycloak"""
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        # Если нет заголовка авторизации — ничего не делаем (DRF попробует другие классы)
        if not auth_header:
            return None

        # Если заголовок есть, но не Bearer — тоже пропускаем, не обрабатываем
        if not auth_header.startswith('Bearer '):
            return None

        # Если Bearer-токен есть — проверяем через OIDC
        return super().authenticate(request)
