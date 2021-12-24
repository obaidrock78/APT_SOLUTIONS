import uuid
from django.core.mail import send_mail
from django.conf import settings

from .models import User, Profile

def user_allow_admin(user):
    return user.is_superuser

def create_user(full_name, username, password, verified=True, is_superuser=False) -> User:
    if is_superuser:
        user = User.objects.create_superuser(
            username=username,
            first_name=full_name,
            password=password
        )
    else:
        user = User.objects.create_user(
            username=username,
            first_name=full_name,
            password=password
        )

    uid = uuid.uuid4()
    pro_obj = Profile(user=user, token=uid)
    pro_obj.verify = verified
    pro_obj.save()

    return user

def user_has_permission(user: User, perm: str):
    role = user.role
    if role is None:
        return False

    return role.has_permission(perm)


def send_email_after_registration(email, token):
    subject = 'Verify Email'
    message = f'Click on the link to verify your account http://infinityapp.pythonanywhere.com/account_verify/{token}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
