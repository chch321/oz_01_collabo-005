from django.shortcuts import render
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from app.user.serializers import UserRegisterSerializer, UserLoginSerializer


class UserRegisterAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token: Token = TokenObtainPairSerializer.get_token(user)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "registration success",
                    "token": {
                        "access": str(token.access_token),
                        "refresh": str(token),
                    },
                },
                status=status.HTTP_200_OK
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request: Request) -> Response:
        token_serializer = TokenObtainPairSerializer(data=request.data)
        if token_serializer.is_valid():
            user = token_serializer.user
            serializer = UserLoginSerializer(user)
            return Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": token_serializer.validated_data,
                },
                status=status.HTTP_200_OK
            )
        return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
