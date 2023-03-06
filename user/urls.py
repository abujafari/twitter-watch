from django.urls import path

from user.views import OtpView, VerifyOtpView

urlpatterns = [
    path('otp', OtpView.as_view()),
    path('verify-otp', VerifyOtpView.as_view()),
]
