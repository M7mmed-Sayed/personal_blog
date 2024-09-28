from django.contrib.auth import authenticate, logout
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import AppUser
from .serializers import UserSerializer


@api_view(['POST'])
def login(request):
    if request.method == "POST":
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterNewAppUserView(CreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


register_new_user_view = RegisterNewAppUserView.as_view()


class UserProfileView(RetrieveAPIView):
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'


user_profile_view = UserProfileView.as_view()


class LogoutView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return Response(status=status.HTTP_200_OK)
        return Response({"detail": "User is not authenticated."}, status=status.HTTP_400_BAD_REQUEST)


logout_view = LogoutView.as_view()
