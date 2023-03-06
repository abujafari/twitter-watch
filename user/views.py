import random

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from core import settings
from core.redis_client import get_redis_connection
from core.services.sms import send_otp
from user.models import User, LoginLog
from user.services import get_ip


# Create your views here.
class OtpRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(allow_null=False, required=True)


class VerifyOtpRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(allow_null=False, required=True)
    code = serializers.CharField(allow_null=False, required=True)


class OtpView(APIView):

    def post(self, request, **kwargs):
        serializer = OtpRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, new_user = User.objects.get_or_create(phone=serializer.data['phone'])
        otp = random.randint(1000, 9999)
        redis_con = get_redis_connection()
        if not redis_con.get(f"otp_{user.phone}"):
            redis_con.setex(f"otp_{user.phone}", 5 * 60, otp)
            send_otp(user.phone, otp)

        return Response({
            "message": "لطفا کد ارسالی به شماره همراه خود را وارد کنید",
            "new_user": new_user
        })


class VerifyOtpView(APIView):

    def post(self, request, **kwargs):
        serializer = VerifyOtpRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(phone=serializer.data['phone'])
        except ObjectDoesNotExist:
            return Response({
                "message": "درخواست مورد نظر اجرایی نیست",
            }, status=400)

        redis_con = get_redis_connection()
        code = redis_con.get(f"otp_{user.phone}")
        if not code:
            return Response({
                "message": "کد منقضی شده است"
            }, status=400)

        if serializer.data['code'] != code:
            return Response({
                "message": "کد اشتباه است"
            }, status=400)

        if not user.is_verified:
            # TODO send welcome sms if new user
            user.is_verified = True

        user.last_login = timezone.now()
        user.save()
        LoginLog.objects.create(user=user, ip=get_ip.get_ip_address(request))

        refresh = RefreshToken.for_user(user)
        response = Response({
            "message": "باموفقیت وارد شدید",
        })

        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=str(refresh.access_token),
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            max_age=3600 * 24 * 30
        )
        return response
