from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django_mongoengine.mongo_auth.models import User as MongoUser

from .serializers import *
from core.models import *

User = get_user_model()

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token = Token.objects(user=user).upsert_one(user=user).save()

        return Response({
            'token': token.key,
            'id': str(user.pk),
            'username': user.username,
            'email': user.email
        })


class ListUsers(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class CreateUser(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCreateSerializer


class EditUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()


class UserChangePassword(APIView):

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except Exception:
            return Response(status=404)

        form = ChangePasswordForm(request.data)

        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return Response({'status': 'OK'}, status=200)

        for key in form.errors:
            form.errors[key] = ' '.join(form.errors[key])

        return Response(form.errors, status=401)
