from django.db import models

# Create your models here.

class login(models.Model):
     username = models.CharField(max_length = 20,default='ding')
#    password = models.CharField(max_length = 20)
    #loginstatus = models.CharField(max_length = 20)
#    #authsession = models.CharField(max_length = 20)
    
class usersmessagemysqldb(models.Model):
    openid = models.CharField(max_length = 60)
    loginstatus = models.CharField(max_length = 20)
    authsession = models.CharField(max_length = 60)
    nickname = models.CharField(max_length = 20,default='testname')
    
    #idusermessge

    name = models.CharField(max_length = 20,default='')
    sex = models.CharField(max_length = 20,default='')
    age = models.CharField(max_length = 20,default='')
    department = models.CharField(max_length = 20,default='')
    telephone = models.CharField(max_length = 20,default='')
   
    #patient case
    caseimg = models.CharField(max_length = 50,default='')
    # def __str__(self):
    #    return 'username:'+ self.username
