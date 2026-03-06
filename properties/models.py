from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


class User(AbstractUser):
    # 定义角色常量
    ROLE_CHOICES = (
        ('user', 'Student User'),
        ('agency', 'Agency'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')


class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField(verbose_name="Price (£/week)")
    
    zip_code = models.CharField(max_length=10)
    image = models.ImageField(upload_to="properties/", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def price_pcm(self):
        """计算月租金 (Per Calendar Month)"""
        # 公式：周租金 * 52 / 12
        return round((self.price * 52) / 12)
    def __str__(self):
        return self.title
    
# properties/models.py

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property') # 确保一个用户只能给一个房源点一个赞


# properties/models.py

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='collected_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property') # 防止重复收藏

    def __str__(self):
        return f"{self.user.username} collected {self.property.title}"
