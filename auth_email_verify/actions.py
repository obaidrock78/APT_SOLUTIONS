import uuid
from .models import User, Profile

def user_allow_admin(user):
    return user.is_superuser

def create_user(full_name, username, password, verified = True, is_superuser=False):
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
