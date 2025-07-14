import re
import base64
from . import crypt
from rest_framework import serializers
from CampSiteApp.models import UserModel, DateCampModel, CommentModel, BookingModel, RecipientModel, \
    ConfirmedBookingsModel, DateCampPhotoModel
from django.contrib.auth.hashers import make_password
from django.db.models import F


class AdminUserSerializer(serializers.ModelSerializer):
    """Серелизатор для Админ-панели"""

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'password', 'is_root', 'is_staff']  # Обязательные поля в API запросе
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'username': {'required': False},
            'email': {'required': False},
            'is_root': {'read_only': True, 'required': False},
            'is_staff': {'read_only': True},
        }

    def create(self, validated_data):
        """Метод для создания нового админа"""

        password = validated_data.pop('password')  # Получаем пароль

        if not password:
            raise serializers.ValidationError("Пароль обязателен!")
        if UserModel.objects.filter(email=validated_data['email']).exists():
            """Поиск пользователя по email, если такой есть - возврат сообщения об ошибке """
            raise serializers.ValidationError('Пользователь с таким email уже существует.')
        if UserModel.objects.filter(username=validated_data['username']).exists():
            """Поиск пользователя по username, если такой есть - возврат сообщения об ошибке """
            raise serializers.ValidationError('Пользователь с таким username уже существует.')
        validated_data['password'] = make_password(password)  # Создание пароля по алгоритму bcrypt
        user = UserModel.objects.create(**validated_data)  # Передача аргументов в модель
        return user  # Возврат объекта user

    def validate_email(self, value):
        """Проверка на наличие такого пользователя."""
        if UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError('Такой пользователь уже существует!')
        return value


class UserLoginSerializer(serializers.Serializer):
    """Серелизатор для авторизации в админ-панель """
    username = serializers.CharField()  # Получение username
    password = serializers.CharField(write_only=True)  # Получение пароля

    def validate(self, data):
        """Проверка на валидность данных """
        username = data['username']
        password = data['password']

        user = UserModel.objects.filter(username=username).first()

        if not user:
            raise serializers.ValidationError("Неверные данные!")

        if user.check_password(password):
            return user  # Возврат объекта user
        else:
            raise serializers.ValidationError("Неверные данные!")


class DateCampModelSerializer(serializers.ModelSerializer):
    """serializer для создания смены"""

    class Meta:
        model = DateCampModel
        fields = ['id', 'name', 'full_name', 'part', 'date', 'places', 'price', 'text']


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для создания комментариев"""
    username = serializers.CharField(read_only=True)

    class Meta:
        model = CommentModel
        fields = ['id', 'text', 'created_at', 'stars', 'username']

    def validate(self, data):
        # Получаем username из контекста (передается из вьюхи)
        username = self.context.get('username') or self.context['request'].user.username  # Тут username
        # Проверка на наличие хотя бы одной подтверждённой брони
        has_confirmed = BookingModel.objects.filter(username=username, status=True).exists()
        if not has_confirmed:
            raise serializers.ValidationError(f"У вас нет подтверждённой путёвки.{username}")
        return data

    def create(self, validated_data, username=None):
        username = self.context.get('username') or self.context['request'].user.username  # Тут username
        validated_data.pop('username', None)
        validated_data.pop('user', None)
        booking_qs = BookingModel.objects.filter(
            username=username,
            status=True,
            quantity__gte=1
        ).order_by('id')
        if not booking_qs.exists():
            raise serializers.ValidationError("У вас нет доступных путёвок для написания комментария. p")
        booking = booking_qs.first()
        if booking.quantity < 1:
            raise serializers.ValidationError("У вас нет доступных путёвок для написания комментария.")
        comment = CommentModel.objects.create(username=username, **validated_data)
        booking.quantity -= 1
        booking.save()
        return comment
# КАК ПОФИКСИТЬ ПРОБЛЕМУ В 1 СТРОЧКУ КОДА !!!!!!

class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipientModel
        fields = ['id', 'email']


class UpdateDatePlacesCampSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateCampModel
        fields = ['places', 'date_camp']


class BookingConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmedBookingsModel
        fields = ['username', 'quantity']
        extra_kwargs = {
            'status': {'required': False},
            'quantity': {'required': False},
        }


class BookingSerializerCrypt(serializers.ModelSerializer):
    """serializer для бронирования """
    date_camp = serializers.PrimaryKeyRelatedField(queryset=DateCampModel.objects.all())

    class Meta:
        model = BookingModel

        fields = [
            'id', 'date_camp', 'surname_parent', 'username', 'patronymic_parent',
            'email_parent', 'number_parent', 'series_passport_parent',
            'issued_passport_parent', 'date_of_issue', 'registration_address_parent',
            'surname_child', 'name_child', 'patronymic_child',
            'date_of_birth', 'address_child', 'passport_child',
            'issued_passport', 'date_of_issue_child', 'series_and_number',
            'comment', 'status'
        ]
        extra_kwargs = {
            'id': {'required': False},
            'status': {'required': False},
            'username': {'required': True},
            'surname_parent': {'required': True},
            'name_parent': {'required': True},
            'patronymic_parent': {'required': True},
            'email_parent': {'required': True},
            'number_parent': {'required': True},
            'series_passport_parent': {'required': True},
            'issued_passport_parent': {'required': True},
            'date_of_issue': {'required': False},
            'registration_address_parent': {'required': True},
            'surname_child': {'required': True},
            'name_child': {'required': True},
            'patronymic_child': {'required': True},
            'date_of_birth': {'required': True},
            'address_child': {'required': True},
            'passport_child': {'required': False},
            'issued_passport': {'required': False},
            'date_of_issue_child': {'required': False},
            'series_and_number': {'required': False},
            'comment': {'required': False}
        }

    def validate_series_passport_parent(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise serializers.ValidationError("Введите 10 цифр: 4 серии и 6 номера без пробелов.")
        return value

    def validate_series_and_number(self, value):
        if value and not re.fullmatch(r'\d{10}', value):
            raise serializers.ValidationError("Введите 10 цифр: 4 серии и 6 номера без пробелов.")
        return value

    def validate(self, data):
        string_fields = [
            'surname_parent', 'name_parent', 'patronymic_parent',
            'issued_passport_parent', 'registration_address_parent',
            'surname_child', 'name_child', 'patronymic_child',
            'address_child', 'passport_child', 'issued_passport', 'comment'
        ]
        for field in string_fields:
            value = data.get(field)
            if value and re.search(r'[a-zA-Z]', value):
                raise serializers.ValidationError({
                    field: "Поля не должны содержать латинские буквы."
                })
        return data

    def validate_date_camp(self, value):

        if not isinstance(value, DateCampModel):
            raise serializers.ValidationError("Неверный формат смены лагеря.")
        if value.places <= 0:
            raise serializers.ValidationError("Нет мест!")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        encrypted_data = {}
        dont_crypt = ['date_camp', 'date_of_issue', 'date_of_issue_child', 'date_of_birth', 'username', 'status']

        for field, value in validated_data.items():
            if field in dont_crypt:
                encrypted_data[field] = value
            else:
                if value is None:
                    encrypted_data[field] = None
                else:
                    encrypted_bytes = crypt.crypting(str(value).encode('utf-8'))
                    encrypted_data[field] = base64.b64encode(encrypted_bytes).decode('utf-8')

        # Сохраняем в базу через модель BookingModel (важно!)
        booking = BookingModel.objects.create(**encrypted_data)

        ConfirmedBookingsModel.objects.create(username=username)

        return booking

    fields_to_decrypt = [
        'surname_parent', 'name_parent', 'patronymic_parent',
        'email_parent', 'number_parent', 'series_passport_parent',
        'issued_passport_parent', 'registration_address_parent',
        'surname_child', 'name_child', 'patronymic_child',
        'address_child', 'passport_child',
        'issued_passport', 'series_and_number',
        'comment'
    ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        decrypted_data = {}
        for field, value in representation.items():
            if value is None:
                decrypted_data[field] = None
            elif field in self.fields_to_decrypt:
                try:
                    encrypted_bytes = base64.b64decode(value)
                    decrypted_value = crypt.decrypting(encrypted_bytes)
                    decrypted_data[field] = decrypted_value
                except Exception:
                    decrypted_data[field] = value
            else:
                decrypted_data[field] = value
        return decrypted_data


class StatusBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingModel
        fields = ['status', 'quantity']  # только поле status для обновления

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance


class DateCampShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateCampModel
        fields = ['id', 'name', 'date']


class BookingShortSerializer(serializers.ModelSerializer):
    date_camp = DateCampShortSerializer()

    class Meta:
        model = BookingModel
        fields = [
            'id', 'status', 'date_camp',
            'surname_child', 'name_child', 'patronymic_child',
            'comment'
        ]


class CommentShortSerializer(serializers.ModelSerializer):
    date_camp = DateCampShortSerializer()

    class Meta:
        model = CommentModel
        fields = ['id', 'text', 'created_at']


class BookingEmailSerializer(serializers.ModelSerializer):
    fields_to_decrypt = ['email_parent']

    class Meta:
        model = BookingModel
        fields = ['email_parent']  # Только поле email_parent

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        decrypted_data = {}
        for field, value in representation.items():
            if value is None:
                decrypted_data[field] = None
            elif field in self.fields_to_decrypt:
                try:
                    encrypted_bytes = base64.b64decode(value)
                    decrypted_value = crypt.decrypting(encrypted_bytes)
                    decrypted_data[field] = decrypted_value
                except Exception:
                    decrypted_data[field] = value
            else:
                decrypted_data[field] = value
        return decrypted_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', "is_root"]  # добавь другие поля, если нужно


class DateCampPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateCampPhotoModel
        fields = ['id', 'image', 'uploaded_at', 'camp']


class DateCampPhotoGetSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = DateCampPhotoModel
        fields = ['id', 'image', 'uploaded_at', 'camp']
