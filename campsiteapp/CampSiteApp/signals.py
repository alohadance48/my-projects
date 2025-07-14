from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_migrate)
def create_root_user(sender, **kwargs):
    User = get_user_model()

    if not User.objects.filter(username='root').exists():
        root_user = User.objects.create_superuser(
            username='root',
            email='root@example.com',
            password=r']b\q,W^G$[DTvi]fZ7FAN?6:ipdg?jgMQo@S)3:–',
            is_staff=True
        )
        # Если есть кастомные поля, установите их здесь
        if hasattr(root_user, 'is_root'):
            root_user.is_root = True
        if hasattr(root_user, 'operation'):
            root_user.operation = 'system'
        root_user.save()

        print('Root user created successfully:')
        print(f"Username: {root_user.username}")
        print(f"Email: {root_user.email}")
        print(f"Is root: {getattr(root_user, 'is_root', 'N/A')}")
        print(f"Is staff: {root_user.is_staff}")
        print(f"Operation: {getattr(root_user, 'operation', 'N/A')}")
    else:
        print('Root user already exists.')
