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
    #诊断 imp,会诊医师:consultant  医师:doctor  RA:result A
    IMP_Doctor_RA = models.CharField(max_length = 50,default='')
    IMP_Doctor_RB = models.CharField(max_length = 50,default='')
    IMP_Doctor_RC = models.CharField(max_length = 50,default='')
    
    IMP_Consultant_RA = models.CharField(max_length = 50,default='')
    IMP_Consultant_RB = models.CharField(max_length = 50,default='')
    IMP_Consultant_RC = models.CharField(max_length = 50,default='')
    #方案
    IMP_SCHEME = models.CharField(max_length = 5,default='')

 #   IMPST = models.CharField(max_length = 10,default='0')  #status
    #处理 rx
