from django.db import models

# Create your models here.
class Customer(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=40)
    pwd = models.CharField(max_length=40)
    class Meta:
        db_table = 'customer'
    def __str__(self):
        return self.id+' '+self.pwd+' '+self.name
class Crop(models.Model):
    # 숫자가 자동 증가
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=40)
    category = models.CharField(max_length=40)
    condition = models.CharField(max_length=40)
    imgname = models.CharField(max_length=40)
    regday = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'crop'
    def __str__(self):
        return f"{self.id} - {self.userid} {self.imgname} {self.category} {self.condition}"

class Contact(models.Model):
    userid = models.CharField(max_length=20)
    username = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # table 이 자동 생성 시 테이블 명으로 지정
        db_table = 'mail'
    def __str__(self):
        return f"{self.userid} - {self.subject}"
