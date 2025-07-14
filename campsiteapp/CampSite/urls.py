"""
URL configuration for CampSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from CampSiteApp.views import (ProtectedViewAdmin,UserLoginView, ProtectedView,LogoutView, UserCommentView, DateCampView,
                                BookingView,MeView,logout_view,MeViewForKeycloak,HomeView,AllBookingView,KeycloakRegisterView,
                                RecipientListView, DatePlacesView, DatePlacesAdminView, BookingConfirmationAdminView,
                                UpdateStatusBookingView, DateCampParentEmailsView, UserCreateCommentView, BookingDeletionAdminView,AllAdminsView,KeycloakRegisterView,LoginInKeycloak,
                                DateCampCreateView,DateCampPhotoDetailAPIView)

from mozilla_django_oidc.views import OIDCAuthenticationRequestView

urlpatterns = [
    path('auth', OIDCAuthenticationRequestView.as_view(), name='oidc_authentication_init'), # keycloak
    path('api/v1/allcomments/',UserCommentView.as_view(),name='allcomments'), # Создание комментов
    path('api/v1/home/',HomeView.as_view(),name='home'), # Главная страница
    path('api/me/v1/keycloak/',MeViewForKeycloak.as_view(),name='keycloakme'), #Получение данных из jwt-token
    path('auth', include('mozilla_django_oidc.urls')), # Keycloak
    path('api/v1/logout/', logout_view, name='logout'),# Выход из keycloak
    path('api/v1/me/', MeView.as_view(), name='me'), # Для получения данных через токен(работает только для админ-панели)
    path('api/v1/protected/', ProtectedView.as_view(), name='protected-view'), # Защищенная страница
    path('api/v1/comment/', UserCommentView.as_view(), name='comment-view'), # Для просмотра отзывов
    path('api/v1/datecamp/', DateCampView.as_view(), name='camp-view'), # Для просмотра смен
    path('api/v1/user/booking/', BookingView.as_view(), name='user-booking-view'), # (Для бронирования путевок)
    path('api/v1/protected/recipient/', RecipientListView.as_view(), name='recipient-view'), # Получение пользователей с рассылкой
    path('api/v1/dateplaces/',DatePlacesView.as_view(), name='dateplaces-view'), # Получение свободных мест для авторизованных пользователей
    path('api/v1/admin/', ProtectedViewAdmin.as_view(), name='protected-view-admin'), # Страница с пользователями в админке
    path('api/v1/admin/bookings/delete/', BookingDeletionAdminView.as_view(), name='delete-booking-admin'),
    path('api/v1/admin/login/', UserLoginView.as_view(), name='login-admin'), #Авторизация в админку
    path('api/v1/admin/dateplaces/', DatePlacesAdminView.as_view(), name='dateplaces-admin'), # Добавление мест на смену
    path('api/v1/admin/bookings/', AllBookingView.as_view(),name='allbooking'), # Все брони путевок
    path('api/v1/admin/bookings/confirms/', BookingConfirmationAdminView.as_view(), name='bookings-admin'), # Страница для проверки подтверждения бронированния админами
    path('api/v1/admin/logout/', LogoutView.as_view(), name='logout-admin'), # logout для адмикнки
    path('api/v1/admin/update/status/bookings/', UpdateStatusBookingView.as_view(), name='update-status-bookings'), # Подтверждение броней
    path('api/v1/parent-emails/', DateCampParentEmailsView.as_view(), name='all-parent-emails'), # Рассылка
    path('api/v1/comment/leave/', UserCreateCommentView.as_view(), name='comment-leave'), # Создание отзыва
    path('api/v1/admin/alladmin/',AllAdminsView.as_view(),name='alladmin'), # Просмотр всех админов
    path('api/v1/registr/',KeycloakRegisterView.as_view(),name='registr'), # Регистрация в keycloak
    path('api/v1/login/keycloak/',LoginInKeycloak.as_view(),name='loginkeycloak'), # Логин в keycloak
    path('api/v1/datecampphotos/<int:pk>/', DateCampPhotoDetailAPIView.as_view(), name='datecampphoto-detail'), # Создание смены с фотками
    path('api/v1/admin/datecamp/', DateCampCreateView.as_view(), name="datecamp-create"), # Создание смены без фотки
    path('api/date-camp-photos/<int:pk>/', DateCampPhotoDetailAPIView.as_view(), name='date-camp-photo-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Для хранения фоток

