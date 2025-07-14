from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from CampSiteApp.models import UserModel, DateCampModel, CommentModel, BookingModel, RecipientModel, \
    ConfirmedBookingsModel, DateCampPhotoModel
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, \
    HTTP_404_NOT_FOUND
from CampSiteApp.serializer import (AdminUserSerializer, UserLoginSerializer, CommentSerializer,
                                    DateCampModelSerializer,
                                    BookingSerializerCrypt, RecipientSerializer, UpdateDatePlacesCampSerializer,
                                    BookingEmailSerializer, BookingConfirmSerializer, StatusBookingSerializer,
                                    BookingShortSerializer, CommentShortSerializer, DateCampShortSerializer,
                                    UserSerializer, DateCampPhotoSerializer, DateCampPhotoGetSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
import logging
from django.shortcuts import redirect
from urllib.parse import urlencode
from CampSiteApp.authentication.keycloak import KeycloakAuthentication
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from CampSiteApp.authentication.TokenLifeTime import ExpiringTokenAuthentication
import requests
from django.conf import settings
import json
from CampSiteApp.models import ExpiringToken


logger = logging.getLogger(__name__)


class LoginInKeycloak(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'username': username,
            'password': password,
            'client_id': settings.CLIENT_ID,
            'grant_type': 'password',
        }

        if settings.CLIENT_SECRET:
            data['client_secret'] = settings.CLIENT_SECRET

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            resp = requests.post(settings.KEYCLOAK_LOGIN, data=data, headers=headers)

            # Проверка: вдруг тело пустое
            if not resp.text:
                return Response({'error': 'Пустой ответ от Keycloak'}, status=resp.status_code)

            # Попробуем распарсить
            try:
                token_data = resp.json()
            except ValueError as e:
                return Response({'error': 'Ошибка при парсинге JSON', 'details': resp.text}, status=resp.status_code)

            if resp.status_code == 200:
                return Response(token_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Ошибка авторизации', 'details': token_data}, status=resp.status_code)

        except Exception as e:
            return Response({'error': 'Ошибка при обращении к Keycloak', 'details': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class KeycloakRegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not all([username, email, password]):
            return Response({"error": "username, email и password обязательны"}, status=400)

        # Шаг 1: Получение admin token через client_credentials
        token_url = f"{settings.KEYCLOAK_HOST}/auth/realms/myrealm/protocol/openid-connect/token"
        token_data = {
            "grant_type": "client_credentials",
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
        }

        token_resp = requests.post(token_url, data=token_data)
        if token_resp.status_code != 200:
            return Response({"error": "Не удалось получить admin токен"}, status=500)

        access_token = token_resp.json().get("access_token")
        if not access_token:
            return Response({"error": "Token отсутствует в ответе"}, status=500)

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Шаг 2: Создание пользователя
        user_payload = {
            "username": username,
            "email": email,
            "enabled": True,
            "emailVerified": False,  # можно включить авто-подтверждение, если нужно
            "credentials": [
                {
                    "type": "password",
                    "value": password,
                    "temporary": False
                }
            ]
        }

        create_url = f"{settings.KEYCLOAK_HOST}/auth/admin/realms/{settings.REALM}/users"
        user_resp = requests.post(create_url, json=user_payload, headers=headers)

        if user_resp.status_code == 201:
            return Response({"message": "Пользователь успешно создан"}, status=201)
        elif user_resp.status_code == 409:
            return Response({"error": "Пользователь уже существует"}, status=409)
        else:
            return Response({
                "error": "Ошибка создания",
                "details": user_resp.text
            }, status=user_resp.status_code)


class MeViewForKeycloak(APIView):
    """End-point для получения информации о пользователе из Keycloak"""

    #
    def get(self, request):
        # Попытка получить токен из заголовка Authorization
        auth_header = request.headers.get('Authorization', '')
        access_token = None
        if auth_header.startswith('Bearer '):
            access_token = auth_header[len('Bearer '):].strip()
        # Если токена нет в заголовке, пытаемся получить из сессии
        if not access_token:
            access_token = request.session.get('oidc_access_token')
        if not access_token:
            return Response({"detail": "Access token not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_info_url = settings.OIDC_OP_USER_ENDPOINT
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.get(user_info_url, headers=headers)
            if response.status_code != 200:
                return Response({"detail": "Unable to fetch user info from Keycloak"},
                                status=status.HTTP_400_BAD_REQUEST)
            user_info = response.json()
            username = user_info.get('preferred_username', 'Unknown')
            email = user_info.get('email', 'No email')
            return Response({
                "token": access_token,
                "username": username,
                "email": email
            })
        except requests.exceptions.RequestException as e:
            return Response({"detail": f"Error fetching user info: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def logout_view(request):
    """Представление для выхода из приложения и Keycloak."""
    # Получаем id_token из сессии (если он был сохранён при аутентификации)
    id_token = request.session.get('oidc_id_token') or request.data.get('id_token')
    if not id_token:  # Проверка на вал
        # Если id_token не найден, перенаправляем на главную страницу или страницу ошибки
        return redirect(settings.LOGOUT_REDIRECT_URL)
    # Очистка текущей сессии
    request.session.flush()
    # Формируем URL для логаута с параметром id_token_hint
    logout_url = f"{settings.OIDC_OP_LOGOUT_ENDPOINT}?id_token_hint={id_token}&post_logout_redirect_uri={settings.LOGOUT_REDIRECT_URL}"
    # Перенаправляем на страницу логаута в Keycloak
    return redirect(logout_url)


class MeViewForUsernameView(APIView):
    """end-point для просмотра всех админов."""
    authentication_classes = [KeycloakAuthentication]

    def get(self, request):
        all_staff = UserModel.objects.filter(is_staff=True)  # Фильтрация по status.
        return Response({'Все админы :': all_staff})


class MeView(APIView):
    """end-point Для получение данных из drf-token (работает для admin-view)
    Используется: для frontend """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Создание объект
        return Response({
                        'email': user.email,
                        'is_staff': user.is_staff,
                        'is_root': user.is_root
                        })


class HomeView(APIView):
    """end-point Для главной страницы"""
    authentication_classes = [KeycloakAuthentication]

    def get(self, request):
        """Возврат ответа"""
        return Response({'message': 'hello '}, HTTP_200_OK)


class AboutView(APIView):
    """ end-point для страницы 'О нас' """

    def get(self, request):
        """Возврат ответа """
        return Response(HTTP_200_OK)


def oidc_logout(request):
    """emd-point для logout keycloak"""
    logger.info("Logging out...")  # Логирование
    request.session.flush()  # Очистка сессии

    keycloak_logout_url = 'http://localhost:8080/realms/myrealm/protocol/openid-connect/logout/'  # Маршрут logout
    redirect_uri = 'http://localhost:8000/'  # переадресация
    params = urlencode({'redirect_uri': redirect_uri})  # переадресация

    logger.info(f"Redirecting to Keyclnoak logout: {keycloak_logout_url}?{params}")  # Логирование

    return redirect(f'{keycloak_logout_url}?{params}')  # Возврат ответа (редерект)


class ProtectedView(APIView):
    """Защищенный end-point для проверки авторизации  """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Возврат ответа """
        return Response({"message": f"Привет, {request.user.username}!"})


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    """ end-point для авторизации администратора """

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            # Создаём/получаем токен через ExpiringToken, чтобы использовать модель с временем создания
            token, created = ExpiringToken.objects.get_or_create(user=user)
            if not created:
                # Если токен уже есть, обновим поле created (обновим время создания токена)
                token.delete()
                token = ExpiringToken.objects.create(user=user)
            return Response({'token': token.key}, status=HTTP_200_OK)
        return Response(serializer.errors, status=400)

class LogoutView(APIView):
    """end-point для logout (работает для админов)"""
    permission_classes = [IsAuthenticated]  # Защита end-point

    def post(self, request):
        try:
            """Удаление токена """
            request.user.auth_token.delete()  # Удаление токена
            return Response({"detal": "Вы вышли из системы "}, HTTP_204_NO_CONTENT)
        except Exception as e:
            """Ответ в случае ошибки """
            return Response({"error": str(e)}, HTTP_400_BAD_REQUEST)


class RecipientListView(APIView):
    permission_classes = [IsAuthenticated]
    """
    POST: добавить email в список получателей
    DELETE: удалить email из списка получателей
    """

    def post(self, request):
        # Проверка admin
        if not getattr(request.user, 'is_staff', False):
            return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
        serializer = RecipientSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if RecipientModel.objects.filter(email=email).exists():
                return Response({"error": "Email уже в списке"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if not getattr(request.user, 'is_staff', False):
            return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email обязателен для удаления"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            recipient = RecipientModel.objects.get(email=email)
            recipient.delete()
            return Response({"message": "Email удалён из списка"}, status=status.HTTP_204_NO_CONTENT)
        except RecipientModel.DoesNotExist:
            return Response({"error": "Email не найден в списке"}, status=status.HTTP_404_NOT_FOUND)


class DateCampCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        datecamp_fields = ["name", "full_name", "part", "date", "places", "price", "text"]
        image_fields = ["image", "camp"]
        image_data = {}
        datecamp_data = {}
        for key, value in request.data.items():
            if key in datecamp_fields:
                print(key)
                datecamp_data[key] = value
            elif key in image_fields:
                image_data[key] = value

        print(datecamp_data)
        print(image_data)
        # Проверка прав root
        if not getattr(request.user, 'is_staff', False):
            return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
        # Создание даты смены: ожидаем поля, характерные для DateCampModelSerializer
        serializer = DateCampModelSerializer(data=datecamp_data)
        if serializer.is_valid():
            instance = serializer.save()
            if not image_data:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            new_id = instance.id
            if not 'camp' in image_data:
                print('maybe not')
                image_data['camp'] = str(new_id)
            serializer = DateCampPhotoSerializer(data=image_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = DateCampPhotoSerializer(data=image_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProtectedViewAdmin(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Проверка прав staff
        if not getattr(request.user, 'is_staff', False):
            return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        admin_add_fields = ['email', 'password', 'username']
        if all(field in data for field in admin_add_fields):
            # Проверка прав root
            if not getattr(request.user, 'is_root', False):
                return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
            serializer = AdminUserSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save(is_staff=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': '''Неверные данные. Предоставьте email, password, username для создания админа либо 
    name, full_name, part, date, places, price, text для создания date_camp'''}, status=status.HTTP_400_BAD_REQUEST)

    # Удаление админа: ожидаем только email
    def delete(self, request):
        data = request.data
        if 'email' in data and len(data) == 1:
            # Проверка рута
            if not getattr(request.user, 'is_root', False):
                return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
            email = data.get('email')
            try:
                user = UserModel.objects.get(email=email)
                print(user)
                user.delete()
                return Response({"message": "Пользователь успешно удалён!"}, status=status.HTTP_204_NO_CONTENT)
            except UserModel.DoesNotExist:
                return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        # Удаление комментария: ожидаем только comment_id
        elif 'comment_id' in data and len(data) == 1:
            comment_id = data.get('comment_id')
            try:
                comment = CommentModel.objects.get(id=comment_id)
                comment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except CommentModel.DoesNotExist:
                return Response({'error': 'Комментарий не найден'}, status=status.HTTP_404_NOT_FOUND)
        # Удаление даты смены: ожидаем только id
        elif 'name' in data and len(data) == 1:
            datecamp_name = data.get('name')
            try:
                datecamp = DateCampModel.objects.get(name=datecamp_name)
                datecamp.delete()
                return Response({"message": "Успешно удалено!"}, status=status.HTTP_204_NO_CONTENT)
            except DateCampModel.DoesNotExist:
                return Response({"error": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                                'error': 'Неизвестная операция или неверные данные (name) = удаление смены; (comment_id) удаление коммента; (email) удаление админа!'},
                            status=status.HTTP_400_BAD_REQUEST)

    # Обновление даты смены через PATCH
    def patch(self, request):
        # Проверка рута
        if not getattr(request.user, 'is_staff', False):
            return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
        # обновление смены
        date_camp_name = request.data.get('name')
        if not date_camp_name:
            return Response({'error': "Поле 'name' обязательно для обновления"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            date_camp = DateCampModel.objects.get(name=date_camp_name)
        except DateCampModel.DoesNotExist:
            return Response({"error": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DateCampModelSerializer(date_camp, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DateCampView(APIView):
    """end-point для создание новой смены """

    def get(self, request):
        date_camp = DateCampModel.objects.all()
        serializer = DateCampModelSerializer(date_camp, many=True)
        photos = DateCampPhotoModel.objects.all()
        serializer_photo = DateCampPhotoGetSerializer(photos, many=True)
        return Response({"date_camps": f"{serializer.data}",
                        "photos": f'{serializer_photo.data}'})


class UserCreateCommentView(APIView):
    """Endpoint для создания комментариев"""
    authentication_classes = [KeycloakAuthentication]

    def post(self, request):
        try:
            access_token = request.session.get('oidc_access_token') or request.headers.get('Authorization', '').replace(
                'Bearer ', '')
            user_info_url = settings.OIDC_OP_USER_ENDPOINT
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(user_info_url, headers=headers)
            if response.status_code != 200:
                return Response({"detail": "Unable to fetch user info from Keycloak"},
                                status=status.HTTP_400_BAD_REQUEST)
            user_info = response.json()
            username = user_info.get('preferred_username', 'Unknown')
            serializer = CommentSerializer(data=request.data, context={'request': request, 'username': username})
            if serializer.is_valid():
                # Передаем user и username явно в create()
                serializer.save(user=request.user, username=username)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException as e:
            return Response({"detail": f"Error fetching user info: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserCommentView(APIView):
    """end-point для просмотра комментов"""
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            comments = CommentModel.objects.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"Ошибка: {e}")
            return Response({'error': 'Internal Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AllBookingView(APIView):
    """ Просмотр всех броней """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Проверка staff
        if not getattr(request.user, 'is_staff', False):
            return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
        # Можно добавить фильтрацию по date_camp через query params, если нужно
        date_camp_id = request.query_params.get('date_camp')
        bookings = BookingModel.objects.all()
        if date_camp_id:
            bookings = bookings.filter(date_camp_id=date_camp_id)
        serializer = BookingSerializerCrypt(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class BookingView(APIView):
    """end-point для бронирования"""
    authentication_classes = [KeycloakAuthentication]

    def post(self, request):
        # Получение access token
        access_token = (
                request.session.get('oidc_access_token')
                or request.headers.get('Authorization', '').replace('Bearer ', '').strip()
        )
        user_info_url = settings.OIDC_OP_USER_ENDPOINT
        headers = {'Authorization': f'Bearer {access_token}'}

        # Логируем токен и endpoint
        logger.info("Получен access token: %s", access_token)
        logger.info("Userinfo endpoint: %s", user_info_url)

        # Запрос к /userinfo
        response = requests.get(user_info_url, headers=headers)

        # Логируем ответ
        logger.info("Ответ от /userinfo: %s", response.status_code)
        logger.debug("Тело ответа от /userinfo: %s", response.text)

        # Обработка ошибки
        if response.status_code != 200:
            return Response(
                {"detail": "Unable to fetch user info from Keycloak"},
                status=response.status_code
            )

        user_info = response.json()
        username = user_info.get('preferred_username', 'Unknown')
        logger.info("Извлечен username: %s", username)

        request.data['username'] = username

        # Сериализация и валидация
        serializer = BookingSerializerCrypt(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Формируем поля для отладки/письма
            fields = BookingSerializerCrypt.Meta.fields
            data = request.data
            lines = []
            for field in fields:
                value = data.get(field, '[Отсутствует]')
                lines.append(f"{field}: {value if value else '[Отсутствует]'}")

            logger.info("Успешно сохранена бронь для: %s", username)

            return Response({"message": "Ваша бронь оставлена!"}, status=status.HTTP_201_CREATED)

        # Логируем ошибки валидации
        logger.warning("Ошибка валидации данных: %s", serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # message_body = "\n".join(lines)
        # recipient_list = list(RecipientModel.objects.values_list('email', flat=True))
        # """if not recipient_list:
        # Если список пуст, можно вернуть ошибку или отправить на дефолтный email
        # return Response({"error": "Список получателей пуст"}, status=status.HTTP_400_BAD_REQUEST)"""
        # send_mail(
        #     subject='Новая бронь',
        #     message=message_body,
        #     from_email='', # ДОБАВЬТЕ МЫЛО СЮДА
        #     recipient_list=recipient_list,
        #     fail_silently=False,
        # )
        # return Response({"message": "Ваша бронь оставлена!"}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DatePlacesAdminView(APIView):
    """ Изменение мест на смену """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Проверка staff
        if not getattr(request.user, 'is_staff', False):
            return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
        # обновление смены
        date_camp_name = request.data.get('name')
        if not date_camp_name:
            return Response({'error': "Поле 'name' обязательно для обновления"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            date_camp = DateCampModel.objects.get(name=date_camp_name)
        except DateCampModel.DoesNotExist:
            return Response({"error": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND)
        places = date_camp.places
        data = {
            "name": f'{date_camp_name}',
            "places": f'{places}'
        }
        operation = str(request.data.get('operation'))
        if not operation:
            return Response({'error': "Должна быть указана операция inc или dec"}, status=status.HTTP_400_BAD_REQUEST)
        if operation.lower() == 'inc':
            data['places'] = places + 1
        elif operation.lower() == 'dec':
            data['places'] = places - 1
            if data['places'] <= 0:
                return Response({'message': 'Количество мест не может быть меньше нуля'},
                                status=status.HTTP_400_BAD_REQUEST)
        serializer = DateCampModelSerializer(date_camp, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Успешно обновленно'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DatePlacesView(APIView):
    """Просмотр мест на смену """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        name = request.query_params.get('name')
        date_camp = DateCampModel.objects.get(name=name)
        if not date_camp:
            return Response({'message': 'Смена с таким именем не найдена'}, status=status.HTTP_400_BAD_REQUEST)
        places = date_camp.places
        return Response({'message': f'{places}'}, status=status.HTTP_200_OK)


class BookingConfirmationAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Проверка staff
        if not getattr(request.user, 'is_staff', False):
            return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
        try:
            all_booking_confirms = ConfirmedBookingsModel.objects.all()
        except NameError:
            return Response({'message': 'На данный момент в базе данных отсутсвуют подтверждения'},
                            status=status.HTTP_200_OK)
        serilized_data = BookingConfirmSerializer(all_booking_confirms, many=True)
        return Response({'message' f'{serilized_data.data}'}, status=status.HTTP_200_OK)

    def post(self, request):
        # Проверка staff
        if not getattr(request.user, 'is_staff', False):
            return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
        username = str(request.data.get('username'))
        confirmed_booking = ConfirmedBookingsModel.objects.filter(username=username)
        if not confirmed_booking:
            return Response({"message": "Нету подтвреждения букинга или букингов по такому пользователю"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': f'{confirmed_booking}'}, status=status.HTTP_200_OK)

    def patch(self, request):

        # Проверка staff
        if not getattr(request.user, 'is_staff', False):
            return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
        id = request.data.get('name')
        if not id:
            return Response({'error': "Поле 'name' обязательно для обновления"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            booking_confirmation = BookingModel.objects.get(name=id)
        except DateCampModel.DoesNotExist:
            return Response({"error": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookingConfirmSerializer(booking_confirmation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # BREAK STAFF, ARASAKA IM COMING


class UpdateStatusBookingView(APIView):
    """end-point для обновления стутса.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """Put запрос """
        id = request.data.get('id')  # Поучение id из запроса
        if not id:  # Проверка на наличие id в запросе
            return Response({"error": "Поле id обязательно"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            booking = BookingModel.objects.get(id=id)  # Поиск по данным
            print(booking)

        except BookingModel.DoesNotExist:
            return Response({"error": "Бронь с таким именем не найдена"},
                            status=status.HTTP_404_NOT_FOUND)  # ответ, если нет брони

        serializer = StatusBookingSerializer(instance=booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # вызовет метод update в сериализаторе
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DateCampParentEmailsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Проверка staff
        if not getattr(request.user, 'is_staff', False):
            return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
        # Получаем все бронирования
        bookings = BookingModel.objects.all()
        serializer = BookingEmailSerializer(bookings, many=True)
        emails = [item['email_parent'] for item in serializer.data if item.get('email_parent')]
        unique_emails = list(set(emails))
        if not unique_emails:
            return Response({'message': 'Email адреса не найдены'}, status=status.HTTP_404_NOT_FOUND)
        return Response(unique_emails)


class BookingDeletionAdminView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        # Проверка staff
        if not getattr(request.user, 'is_staff', False):
            return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
        id = request.data.get('id')
        try:
            booking = BookingModel.objects.get(id=id)
            print(booking.status)
            if booking.status:
                return Response({"error": "Нельзя удалить подтвержденную бронь"}, status=status.HTTP_403_FORBIDDEN)
            booking.delete()
            return Response({"message": "Успешно удалено!"}, status=status.HTTP_204_NO_CONTENT)
        except DateCampModel.DoesNotExist:
            return Response({"error": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND)


# commit whoora


class AllAdminsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_users = UserModel.objects.filter(is_staff=True)
        serializer = UserSerializer(all_users, many=True)
        return Response({'users': serializer.data}, status=status.HTTP_200_OK)


# CRUD для фото смены лагеря
class DateCampPhotoDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        return get_object_or_404(DateCampPhotoModel, pk=pk)

    def get(self, request, pk):
        photo = self.get_object(pk)
        serializer = DateCampPhotoSerializer(photo)
        return Response(serializer.data)

    def put(self, request, pk):
        # Проверка admin
        if not getattr(request.user, 'is_staff', False):
            return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
        photo = self.get_object(pk)
        serializer = DateCampPhotoSerializer(photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        # Проверка admin
        if not getattr(request.user, 'is_staff', False):
            return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
        photo = self.get_object(pk)
        serializer = DateCampPhotoSerializer(photo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Проверка admin
        if not getattr(request.user, 'is_staff', False):
            return Response({"error": "Нет прав!"}, status=status.HTTP_403_FORBIDDEN)
        photo = self.get_object(pk)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
