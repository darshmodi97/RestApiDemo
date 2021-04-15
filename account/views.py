from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import Http404
from django.contrib.auth.models import User

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

from account.paginations import CustomPagination
from account.permissions import IsTokenValid
from account.serializers import UserSerializer, UserLoginSerializer
from account.models import BlackListedToken


# Create your views here.
class UserLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token': serializer.data['token'],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class All_Users(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle]
    pagination_class = CustomPagination
    users = User.objects.all()

    def get_queryset(self):
        return self.users


class ShowProfile(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    
    def get_user(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        user = self.get_user(pk=pk)
        serializer = self.serializer_class(user, context={'request': request})

        return Response(
            {
                "success": "True",
                "data": serializer.data,
                "status": status.HTTP_200_OK
            }
        )


class UpdateProfile(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTokenValid]
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        serializer = self.serializer_class(user, data=request.data, context={'request':request})

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": "True",
                    "message": "User updated successfully.",
                    "data": serializer.data,
                    "status": status.HTTP_200_OK
                }
            )
        else:
            return Response(
                {
                    "success": "False",
                    "error message": serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST
                }
            )


class DeleteAccount(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTokenValid]
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        user.delete()
        return Response(
            {
                "success": "True",
                "status": status.HTTP_204_NO_CONTENT,
                "message": "User deleted successfully."
            }
        )


class SignUpView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

        return Response(
            data={
                "success": "True",
                "message": "User created successfully.",
                "status": status.HTTP_201_CREATED
            }
        )


class LogoutView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            BlackListedToken.objects.create(user=request.user, token=request.auth.decode("utf-8"))
        except IntegrityError:
            return Response({
                "message": "User can't logout."
            })

        return Response(
            {"message": "User logged out successfully."}
        )
