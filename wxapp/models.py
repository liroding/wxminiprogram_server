from django.db import models

# Create your models here.

class login(models.Model):
     username = models.CharField(max_length = 20,default='ding')
#    password = models.CharField(max_length = 20)
    #loginstatus = models.CharField(max_length = 20)
#    #authsession = models.CharField(max_length = 20)
    
class usersmessagemysqldb(models.Model):
    openid = models.CharField(max_length = 60,default='')
    loginstatus = models.CharField(max_length = 20,default='')
    authsession = models.CharField(max_length = 60,default='')
    nickname = models.CharField(max_length = 20,default='testname')
    
    #idusermessge
    name = models.CharField(max_length = 20,default='')
    sex = models.CharField(max_length = 20,default='')
    age = models.CharField(max_length = 20,default='')
    department = models.CharField(max_length = 20,default='')
    telephone = models.CharField(max_length = 20,default='')
   
    #patient case
    #PE: physical examnination  case1-case4 caseimag
    #PE_ST : ST->status
    #PE_IMG : IMG-> image
    PEA = models.CharField(max_length = 50,default='')
    PEB = models.CharField(max_length = 50,default='')
    PEC = models.CharField(max_length = 50,default='')
    PED = models.CharField(max_length = 50,default='')
    PEIMG = models.CharField(max_length = 50,default='')  #image
    PEST = models.CharField(max_length = 10,default='0')  #status
    # def __str__(self):
    #    return 'username:'+ self.username
    #诊断 imp
    #处理 rx
