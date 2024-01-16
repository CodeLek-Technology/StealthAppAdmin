from django.db import models
from authentication.models import CustomUser


class Location(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=70)
    longitude = models.CharField(max_length=70)
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.latitude
    
    class Meta:
        ordering = ('-timestamp',)

SESSION_CHOICES = (
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout")
    )

class LoginHistorie(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session_type = models.CharField(max_length=20, choices=SESSION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} - {self.session_type}'
    
    class Meta:
        ordering = ('-timestamp',)
