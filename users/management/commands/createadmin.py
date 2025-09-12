from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = get_user_model()
        user = user.objects.create(
            email="skystore.blog@mail.ru", first_name="Den", last_name="Yukin"
        )
        user.set_password("1234")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created admin user with email {user.email}"
            )
        )
