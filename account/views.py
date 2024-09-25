from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authtoken.models import Token
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView,CreateAPIView
from rest_framework.response import Response

from .models import AppUser
from .serializers import RegisterSerializer, LoginSerializer


@api_view(['POST'])
def login(request):
    if request.method == "POST":
        email = request.data['email']
        password = request.data['password']
        user = None
        if '@' in email:
            try:
                user = AppUser.objects.get(email=email)
            except ObjectDoesNotExist:
                pass
        if not user:
            user = authenticate(email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterNewAppUserView(ListCreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        serializer.save()


register_new_user_view = RegisterNewAppUserView.as_view()


class LoginAppUserView(CreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = LoginSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


login_app_user_view = LoginAppUserView.as_view()
