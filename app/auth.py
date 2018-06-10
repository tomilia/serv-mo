from .models import CustomUser
from django.db.models import Q


class Auth(object):
    def authenticate(self,username=None,password=None):
        try:
            user=CustomUser.objects.get(Q(email=username) | Q(phone_num=username))
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
                return None
    def get_user(self,user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            print(user_id)
            if user.is_active:
                return user
            return None
        except CustomUser.DoesNotExist:
            return None
