from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from StealthApp.views import LocationViews, LoginHistoryViews, ProfileViewSet, UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from StealthApplication.views import CustomObtainToken

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)


urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path("admin/", admin.site.urls),
    path("", include("authentication.urls")),
    path("main/", include("StealthApp.urls")),
    path("api/", include(router.urls)),
    path("api/locations/", LocationViews.as_view()),
    path("api/logout/", LoginHistoryViews.as_view()),
    path("api/profile/", ProfileViewSet.as_view({'get': 'retrieve'})),
    path("api-auth/token/", CustomObtainToken.as_view(), name="token_obtain_pair"),
    path("api-auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Example "Response" of route -> 'api-auth/token'
"""
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNTQwNzk2MywiaWF0IjoxNzA1MzIxNTYzLCJqdGkiOiI2NDZhOTU5ZDA1ZWY0OTNiOWE5Y2UzZjk4MTg1ZmQ5NyIsInVzZXJfaWQiOjF9.PNgoO3IGYuoUUpFKhL1Ldpzhww845ABFeGwvDgb83TU",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA1MzIxODYzLCJpYXQiOjE3MDUzMjE1NjMsImp0aSI6ImQzNmJkYjcwZTUxYjQ2ZmNhZGU0OWQ3ZTQ2YjczZDRlIiwidXNlcl9pZCI6MX0.q4oNdeL-XX6DUnfpOQt1NYTFj43_ZyCoh0c7zUFU0tY"
}
"""
