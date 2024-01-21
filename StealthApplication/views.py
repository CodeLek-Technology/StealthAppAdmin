from typing import Any, Dict
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from StealthApp.serializers import LoginHistorySerializer

from authentication.models import CustomUser


def update_login_history(user: CustomUser):
    loc = LoginHistorySerializer(data={"user": user.id, "session_type": "LOGIN"})
    if loc.is_valid(raise_exception=True):
        loc.save()


class CustomTokenObtainPairSerializer( TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        user: CustomUser = self.user
        update_login_history(self.user)

        data["phone"] = user.phone_no
        data["name"] = user.get_full_name()

        return data

class CustomObtainToken(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


