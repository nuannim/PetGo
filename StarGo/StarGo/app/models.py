from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Users(models.Model):
    # username = models.CharField(max_length=100)
    # password = models.CharField(max_length=100)
    # role = models.CharField(max_length=50, blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    imageurl = models.FileField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.auth_user.username}"


class Celebrities(models.Model):
    # firstname = models.CharField(max_length=100) #!
    # lastname = models.CharField(max_length=100) #!
    nickname = models.CharField(max_length=100)
    imageurl = models.FileField(upload_to='images/', blank=True, null=True) # * ถ้า upload_to='' จะไปเก็บใน media เลย
    # addby_users = models.ForeignKey('Users', on_delete=models.CASCADE, blank=True, null=True)
    addby_auth_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='celebrities_addby_auth_user')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='celebrities_owner')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nickname}"


# (Bands model removed) 


class Places(models.Model):
    name = models.CharField(max_length=100)
    googlemaplink = models.CharField(max_length=300, blank=True, null=True)
    address = models.CharField(max_length=200)
    # addby_users = models.ForeignKey('Users', on_delete=models.CASCADE, blank=True, null=True)
    addby_auth_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    imageurl = models.FileField(upload_to='images/', blank=True, null=True) # * ถ้า upload_to='' จะไปเก็บใน media เลย
    created_at = models.DateTimeField(auto_now_add=True)

    # latitude = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True)
    # longtitude = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True)

    def __str__(self):
        return self.name


class Sightings(models.Model):
    celebrities = models.ForeignKey('Celebrities', on_delete=models.CASCADE)
    places = models.ForeignKey('Places', on_delete=models.CASCADE)
    arrivaldate = models.DateField()
    # addby_users = models.ForeignKey('Users', on_delete=models.CASCADE, blank=True, null=True)
    addby_auth_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Celebrities may no longer have firstname/lastname fields. Use the
        # Celebrities.__str__ representation which already falls back to nickname.
        celeb_str = str(self.celebrities)
        return f"{celeb_str} at {self.places} on {self.arrivaldate}"




class Comments(models.Model):
    # --- สิ่งที่ต้องมีเสมอ ---
    places = models.ForeignKey(Places, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # --- ฟิลด์ที่คุณถามถึง ---
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment_text = models.TextField(max_length=2000) # TextField สำหรับข้อความยาวๆ

    # --- ฟิลด์ที่ควรมีอย่างยิ่ง ---
    created_at = models.DateTimeField(auto_now_add=True) # วันเวลาที่สร้างคอมเมนต์
    updated_at = models.DateTimeField(auto_now=True)     # วันเวลาที่แก้ไขล่าสุด

    def __str__(self):
        return f'Comment by {self.user.username} on {self.places.name}'

