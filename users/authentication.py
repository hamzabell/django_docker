from django.contrib.auth import get_user_model
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions


def generate_access_token(user):
    payload =  {
        'user_id': user.id,
        'exp': (datetime.utcnow() + timedelta(minutes=60)).timestamp(),
        'int': datetime.utcnow().timestamp(),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Unauthenticated')

        user  = get_user_model().objects.filter(id=payload['user_id']).first()


        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, None)



