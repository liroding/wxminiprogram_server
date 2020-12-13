from django.contrib import admin
import os,sys
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,render_to_response
from django.template.context import RequestContext
import requests
import hashlib
from wxapp.models import usersmessagemysqldb
import time
import logging
from django.core.cache import cache
#Get an instance of a loggger
logger = logging.getLogger('django')


#error:ascii codec can't encode characters
#import codecs
#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# wx test app
#appid='wx0e09ec16b9a52aaf'
#appsecret='0e972dcc055cd8f5c60d3fe12dbc822e'

#this is my other app 
appid='wxe3d8a1aee3eed9b6'
appsecret='13dbc41accb74b6e1a14d525ddeedec9'

WEIXIN_TOKEN = 'ding'

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_URL   = 'https://dingyinglai.site'

#appid='wxe3d8a1aee3eed9b6'
#appsecret='1c441d00be38e3ec66cd79ff287924ee'

url_code2Session='https://api.weixin.qq.com/sns/jscode2session?appid='+appid\
+'&secret='+appsecret+'&js_code='


url_accesstoken='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+appid+'&secret='+appsecret
#sever should to get access token value on time (2 hours)

#############################################
PEA_index = ['PEA-1','PEA-2','PEA-3','PEA-4']
PEB_index = ['PEB-1','PEB-2','PEB-3','PEB-4']
PEC_index = ['PEC-1','PEC-2','PEC-3','PEC-4','PEC-5','PEC-6','PEC-7','PEC-8','PEC-9','PEC-10','PEC-11']
#############################################
def get_accesstoken():
    print('[server-log]: to get access token value')
    res = requests.get(url_accesstoken)
    print(url_accesstoken)
    _dict = res.json()
    access_token = _dict['access_token'] #get session_key
    localtime = time.asctime( time.localtime(time.time()) )
    print('Now time is:',localtime)
    print(access_token)
    cache.set('access_token',access_token)

#-------------------------------------
# Function : to check authsession whether it match or not 
# Return   : {matchflag,openid,mathchdbid}
#------------------------------------

def checkauthsession(authsessioncode):
        retarg = {'matchflag':0,'openid':'','matchdbid':0}
        logger.debug('[server-log]: authsession = %s', authsessioncode)
        has_authsession = 0
        authsession = authsessioncode
        if(authsession):
            all_usersmessage = usersmessagemysqldb.objects.all()
            #to find whether db have authsession
            i = 0
            while i < len(all_usersmessage):
                if authsession in all_usersmessage[i].authsession:    
                    has_authsession = 1
                    retarg['matchflag'] = 1
                    retarg['openid'] = all_usersmessage[i].openid
                    retarg['matchdbid'] = i
                    logger.info('[server-log]: index = %d',i)
                    logger.info('[server-log]: authsession match !!!')
                    logger.debug('[server-log]: retarg = %s',retarg)
                    return retarg   #match 
                i += 1
            if has_authsession == 0:
                logger.info('[server-log]: authsession no  match !!!')
                return retarg   #no match
        else:
            return HttpResponse('attach authsession is null !!!')

#-------------------------------------------------
# this function is to get value base of input key
# argid   return value
#  1        nickname
#-------------------------------------------------
def getkeyvalue(authsessioncode,argid): #1:nickname
        all_usersmessage = usersmessagemysqldb.objects.all()
        authsession = authsessioncode
        i = 0
        while i < len(all_usersmessage):
                if authsession in all_usersmessage[i].authsession:   
                     if argid == 1:
                         return all_usersmessage[i].nickname
                i +=1
def listfilename(home_dir,serverurl): #this function find the file under dir
        filelist = []
        logger.info('[server-log]: serverurl = %s',serverurl)
        for root,dirs,files in os.walk(home_dir):
               for file in files:
                   if os.path.splitext(file)[1] == '.PNG':
                       filelist.append(os.path.join(serverurl,file))
        return filelist 


class wxappstruct():
    
    def testfunc(request):
        logger.info('[server-log]: hello world !!!')
        return HttpResponse('hello world')
    def wxsubscribes(request):
        find_openid = 0
        openid = 0
       
        if request.method == 'POST':
           authsession = request.POST['authsession']
           subscribeid = request.POST['subscribeid']
           logger.debug('[server-log]: subscribeid = %s',subscribeid)
           
           _dictret = checkauthsession(authsession)
           has_authsession = _dictret['matchflag']
           openid = _dictret['openid']
           index = _dictret['matchdbid'] 
           if has_authsession == 0:
                return HttpResponse('Authsession no match')
           else:
                #start to get name in mysqldb
                all_usersmessage = usersmessagemysqldb.objects.all()
                i = 0
                while i < len(all_usersmessage):
                        i = index 
                        name = all_usersmessage[i].name
                        logger.debug('[server-log]: openid = %s',openid)
                        break
                
                access_token = cache.get('access_token')
                logger.debug('[server-log]: access token = %s',access_token)
                nowtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) 
                if subscribeid == '1':
                    template_id = 'yknmtxHzvfU4rE84aa9si5LuV0gAW_7KGzEXz7FQgN0'
                    push_data = {
                         "thing1": {
                                   "value": 'Love'
                         },
                         "name2": {
                                   "value": 'chunxiaoxu'
                         },
                         "date4": {
                                   "value": nowtime
                         },
                         "phone_number3": {
                                   "value": '1314'
                         },
                      }
                elif subscribeid == '2':
                    template_id = '8qZXmYaPl9gJsUFQmhtDb73gvkP-lKFivLyroyTpeyI'
                    push_data = {
                        "thing1": {
                                  "value": name
                        },
                        "time3": {
                                  "value": nowtime
                        },
                      }

                if access_token:
                   # 如果存在accesstoken
                   payload = {
                               'touser': openid, #这里为用户的openid
                               'template_id': template_id, #模板id
                               'page': "pages/Preview/Preview",
                               'data': push_data #模板填充的数据
                   }


                   url_sendtemplate = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token='+access_token
                   logger.debug('[server-log]: url_sendtemplate = %s', url_sendtemplate)
                   response = requests.post(url_sendtemplate,json=payload)
                   #print(response)
                   #print(response.json())
                   #直接返回res结果
                   #return JsonResponse(response.json())
                   return HttpResponse('1111111')
                else:
                   '''
                   return JsonResponse({
                         'err': 'access_token missing'
                })   
                   '''

                   return HttpResponse('222')

    def wxcheckSignature(request):
        
        signature = request.GET['signature']
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        echostr = request.GET['echostr']
        token = WEIXIN_TOKEN
        tmp_list = [timestamp,nonce,token]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        sha = hashlib.sha1()
        sha.update(tmp_str.encode())
        tmp_str = sha.hexdigest()
        logger.debug('[server-log]: signature = %s', signature)
        if tmp_str == signature:
             return HttpResponse(echostr)
        else:
             return HttpResponse("weixin index")
#--------------------------------------------------
# onlogin
#-------------------------------------------------

    def onlogin(request):
        has_user = 0
        wx_code = request.GET['code']
        username = request.GET['username']
        logger.info('[server-log]: onlogin func for (res.code)')
        logger.debug('[server-log]: wx_code = %s', wx_code)
        logger.debug('[server-log]: username = %s', username)
        tmpurl = url_code2Session + wx_code + '&grant_type=authorization_code'
        logger.debug('[server-log]: tmpurl = %s', tmpurl)
        res = requests.get(tmpurl)
        _dict = res.json()
        session_key = _dict['session_key'] #get session_key
        openid = _dict['openid']
        #get authsession
        sha = hashlib.sha1()
        sha.update(openid.encode())
        authsession = sha.hexdigest() #define our session for auth
        logger.debug('[server-log]: authsession = %s', authsession)
        #storage username & openid to db
        all_usersmessage = usersmessagemysqldb.objects.all()
        #to find whether db have openid data
        i = 0
        while i < len(all_usersmessage):
                if openid in all_usersmessage[i].openid:    
                    has_user = 1
                    logger.info('[server-log]: db has this username information')
                    break
                i +=1
        if has_user == 0:
                logger.info('[server-log]: db do not this openid,then to storage')
                usermessage = usersmessagemysqldb()
                usermessage.authsession = authsession
                usermessage.openid = openid
                usermessage.nickname = username
                usermessage.save()
        logger.debug('[server-log]: wxserver return the data: %s',str(res.json()))
        #return HttpResponse('key 12')
        return JsonResponse({'authsession':authsession})
#--------------------------------------------------
# user submit same their idmessage
# PEST     7    6    5      4       3      2    1    0
#         保留|保留|会诊师已给出诊断|病历更新|保留|保留|医师已给出诊断|病历更新     
#-------------------------------------------------

    def idmessagehandle(request):
        has_authsession = 0
        name = request.POST['name']
        sex = request.POST['checkbox']
        age = request.POST['age']
        department = request.POST['department']
        telephone = request.POST['telephone']
        authsession = request.POST['authsession']
        
        #check authseesion where is match or not
        if(authsession):
            _dictret = checkauthsession(authsession)
            has_authsession = _dictret['matchflag']
            logger.debug('[server-log]:  dictdata type: %s',type(_dictret))
            logger.debug('[server-log]: return dictdata = %s',_dictret)
            if has_authsession == 0:
                logger.info('[server-log]: authsession no match !!!')
                return HttpResponse('attach authsession is error,no matching with userid(openid)')
            else:
                logger.info('[server-log]: authsession pass !!!')
                index = _dictret['matchdbid'] 
                logger.debug('[server-log]: index = %d',index)
                #do logic demand handle
                all_usersmessage = usersmessagemysqldb.objects.all()
                i = 0
                while i < len(all_usersmessage):
                     i = index
                     #do logic demand handle
                     all_usersmessage[index].name = name
                     all_usersmessage[index].sex = sex
                     all_usersmessage[index].age = age
                     all_usersmessage[index].department = department
                     all_usersmessage[index].telephone = telephone
                     logger.debug('[server-log]: name = %s',all_usersmessage[index].name)
                     logger.debug('[server-log]: status = %d',int(all_usersmessage[index].PEST))
                     all_usersmessage[index].PEST = int(all_usersmessage[index].PEST) | 0x1 
                     all_usersmessage[index].save()
                     logger.info('[server-log]: update the database finish !!!')
                     break
                return HttpResponse('Sever has update the database !')


        return HttpResponse('attach authsession is null !!!')

#--------------------------------------------------
# user upload the PEx and same picture
# storage path :/static/uploads/PEImags/
#-------------------------------------------------
         
    def fileupload(request):
        if request.method == "POST":
            authsession = request.POST['authsession']
            _dictret = checkauthsession(authsession)
            has_authsession = _dictret['matchflag']

            if has_authsession == 0:
                return HttpResponse('Authsession no match')
            else:
                uploadid = request.POST['uploadid']
                logger.debug('[server-log]: upload img id = %s',uploadid )
                if   uploadid == '3':
                     casepicid = request.POST['casepicid']
                     image_file = request.FILES.get('file')
                     nowtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) 
                     filename = nowtime + '_' + casepicid #this is UTC time,hour shoud +8 will be beijing time
                    # print(filename)
                    # print(sys.getdefaultencoding())
                     #storage case imgs to server
                     nickname = getkeyvalue(authsession,1) #1:nickname
                     logger.debug('[server-log]: nickname = %s',nickname)
                     path = PROJECT_ROOT + '/static/uploads/PEImags/' + nickname + '/' #django env
                     logger.debug('[server-log]: upload file path = %s' , path)
                     
                     if not os.path.exists(path):
                          os.makedirs(path)
                     with open(path + filename + '.PNG','wb+') as destination:
                          for chunk in image_file.chunks():
                               destination.write(chunk)

        else:
            return HttpResponse('server cannot handle GET request !!!!')
        logger.info('[server-log]: file upload !!!')
        return HttpResponse('file upload success !!!')
#--------------------------------------------------
# reqid = 1 :doctor check patient PE Info to handle
# PEST     7    6    5      4       3      2    1    0
#         保留|保留|会诊师已给出诊断|病历更新|保留|保留|医师已给出诊断|病历更新     
#-------------------------------------------------
    def querymysqldb(request):
       
        authsession = request.POST['authsession']
        _dictret = checkauthsession(authsession)
        has_authsession = _dictret['matchflag']
      
        if has_authsession == 0:
             return HttpResponse('Authsession no match')
        else:
             logger.info('[server-log]: authsession pass !!!')
             index = _dictret['matchdbid'] 
             reqid = request.POST['reqid']
             logger.info('[server-log]: reqid = %s', reqid)
             if reqid == '1' or reqid == '2':  #doctor get all message from db
                all_usersmessage = usersmessagemysqldb.objects.all()
                #do logic demand handle
                index = 0 
                while index < len(all_usersmessage):
                   logger.debug('[server-log-p6] index = %d',index)
                   status = int(all_usersmessage[index].PEST)      
                   status = status & 0x11
                   logger.debug('[server-log-p1]: status = %s', status)
                   if status != 0:
                     tmp = 0
                     if reqid == '1':
                        tmp = status & 0x1
                        logger.debug('[server-log-p2]: tmp = %d', tmp)
                        if tmp == 1:    
                           logger.info('[server-log-p4]')
                           all_usersmessage[index].PEST = int(all_usersmessage[index].PEST) & 0xfe #set PEST[0]=0,it means the doctor has checked it
                        else:
                           index = index + 1
                           continue
                        logger.debug('[server-log-p5]')
                     elif reqid == '2':
                        tmp = status & 0x10
                        logger.info('[server-log-p3]: tmp = %s', tmp)
                        if tmp == 0x10:    
                           all_usersmessage[index].PEST = int(all_usersmessage[index].PEST) & 0xef #set PEST[0]=0,it means the doctor has checked it
                        else:
                           index = index + 1
                           continue
                     name = all_usersmessage[index].name
                     logger.info('[server-log]: name = %s', name)
                     sex  = all_usersmessage[index].sex
                     age  = all_usersmessage[index].age
                     department =  all_usersmessage[index].department
                     telephone = all_usersmessage[index].telephone
                     #此处为患者的authsession,为了后续的医师诊断使用
                     patient_authsession = all_usersmessage[index].authsession
                     #PE handle
                     PEA =  all_usersmessage[index].PEA
                     PEB =  all_usersmessage[index].PEB
                     PEC =  all_usersmessage[index].PEC
                     all_usersmessage[index].save()

                     _ListPEA = PEA.strip(',').split(',')
                     _ListPEB = PEB.strip(',').split(',')
                     _ListPEC = PEC.strip(',').split(',')
                     logger.debug('[server-log]: PEA_list = %s', _ListPEA)
                     logger.debug('[server-log]: PEB_list = %s', _ListPEB)
                     logger.debug('[server-log]: PEC_list = %s', _ListPEC)
                     ###########################################
                     _retPEAlist = [0 for x in range(0,4)]
                     _retPEBlist = [0 for x in range(0,4)]
                     _retPEClist = [0 for x in range(0,11)]
                     ##########################################
                     _nickname = all_usersmessage[index].nickname
                     nickname = _nickname.encode('UTF-8')
                     logger.debug('[server-debug]: the nickname %s',nickname)
                     _homepath = PROJECT_ROOT + '/static/uploads/PEImages/' + all_usersmessage[index].nickname + '/'
                     _serverurlpath = SERVER_URL + '/static/uploads/PEImages/' + all_usersmessage[index].nickname + '/'
                     homepath = _homepath.encode('UTF-8')
                     serverurlpath = _serverurlpath.encode('UTF-8')
                     PEImglist = listfilename(homepath,serverurlpath)
                     #PEA
                     for i in range(len(_ListPEA)):
                         for j in range(len(PEA_index)):
                             if _ListPEA[i] == PEA_index[j]:
                                _retPEAlist[j] = 1
                     #PEB
                     for i in range(len(_ListPEB)):
                         for j in range(len(PEB_index)):
                             if _ListPEB[i] == PEB_index[j]:
                                _retPEBlist[j] = 1
                     #PEC
                     for i in range(len(_ListPEC)):
                         for j in range(len(PEC_index)):
                             if _ListPEC[i] == PEC_index[j]:
                                _retPEClist[j] = 1
                     logger.debug('[server-debug]: tmp_PEAindex 1 conver = %s',_retPEAlist)
                     logger.debug('[server-debug]: tmp_PEAindex 2 conver = %s',_retPEBlist)
                     logger.debug('[server-debug]: tmp_PEAindex 3 conver = %s',_retPEClist)
                     logger.info('[server-debug]: get the database data !!!')
                     #此次返回的authsession是患者的authsession,为了后续医师填写
                     #诊断结果准备
                     return JsonResponse({'authsession':patient_authsession,'name':name,\
                                             'sex':sex,'age':age,'department':department, \
                                             'telephone':telephone,  \
                                             'PEA':_retPEAlist,  \
                                             'PEB':_retPEBlist,  \
                                             'PEC':_retPEClist,  \
                                             'PEImglist':PEImglist \
                                       })
                   index = index + 1
                logger.info('[server-debug]: this is last handle dbcase !!!')
                #如果查不多患者者信息，则authsession返回null,代表无
                return JsonResponse({'authsession':null})
             if reqid == '3':  #doctor diagnosis result get all message from db
                all_usersmessage = usersmessagemysqldb.objects.all()
                #do logic demand handle
                i = 0 
                while i < len(all_usersmessage):
                    i = index
                    hascheckflag = int(all_usersmessage[index].PEST) & 0x02 #set PEST[1]=1,it means the doctor has checked it
                    if hascheckflag == 0x2:
                       IMP_RA =  all_usersmessage[index].IMP_Doctor_RA
                       IMP_RB =  all_usersmessage[index].IMP_Doctor_RB
                       IMP_RC =  all_usersmessage[index].IMP_Doctor_RC

                       return JsonResponse({ \
                                             'IMP_RA':IMP_RA,  \
                                             'IMP_RB':IMP_RB,  \
                                             'IMP_RC':IMP_RC,  \
                                    })

                    else:
                       return HttpResponse('has not be checked')

                    break
#--------------------------------------------------
# Handle PEx Post Data,Storage to db
# PEST     7    6    5      4       3      2    1    0
#         保留|保留|会诊师已给出诊断|病历更新|保留|保留|医师已给出诊断|病历更新     
#-------------------------------------------------
    def patientcasehandle(request):
        logger.info('[server-log]:enter patient case handle')
        has_authsession = 0
        PEA_Data = request.POST['PEA_Data']
        PEB_Data = request.POST['PEB_Data']
        PEC_Data = request.POST['PEC_Data']
        authsession = request.POST['authsession']
        _ListPEA = PEA_Data.strip(',').split(',')
        _ListPEB = PEB_Data.strip(',').split(',')
        _ListPEC = PEC_Data.strip(',').split(',')
        logger.debug('[server-log]: PEA_Data = %s ', PEA_Data)
        logger.debug('[server-log]: PEB_Data = %s ', PEB_Data)
        logger.debug('[server-log]: PEC_Data = %s ', PEC_Data)
       
        
        _dictret = checkauthsession(authsession)
        has_authsession = _dictret['matchflag']
      
        if has_authsession == 0:
            return HttpResponse('Authsession no match')
        else:
            logger.info('[server-log]: authsession pass !!!')
            index = _dictret['matchdbid'] 
            logger.debug('[server-log]: index = %d',index)

            all_usersmessage = usersmessagemysqldb.objects.all()
            #to find whether db have authsession
            i = 0
            while i < len(all_usersmessage):
                    i = index
                    #do logic demand handle
                    all_usersmessage[i].PEA = PEA_Data
                    all_usersmessage[i].PEB = PEB_Data
                    all_usersmessage[i].PEC = PEC_Data
                    all_usersmessage[i].PEST = int(all_usersmessage[i].PEST) | 0x1 
                    all_usersmessage[i].PEST = int(all_usersmessage[i].PEST) | 0x10 
                    logger.debug('[server-log]: status = %d',int(all_usersmessage[index].PEST))
                    all_usersmessage[i].save()
                    logger.info('[server-log]: update the database finish !!!')
                    return HttpResponse('Sever has update the database !')

#--------------------------------------------------
# reqid = 1 :doctor check patient PE Info to handle
# PEST     7    6    5      4       3      2    1    0
#         保留|保留|会诊师已给出诊断|病历更新|保留|保留|医师已给出诊断|病历更新     
#-------------------------------------------------
    def diagnoseresulthandle(request):
       
        authsession = request.POST['authsession']
        _dictret = checkauthsession(authsession)
        has_authsession = _dictret['matchflag']
        
        IMP_RA = request.POST['IMP_RA']
        IMP_RB = request.POST['IMP_RB']
        IMP_RC = request.POST['IMP_RC']
        IMP_SCHEME = request.POST['IMP_SCHEME']
        checkerdoctorid  = request.POST['checkerdoctorid']
      
        if has_authsession == 0:
             return HttpResponse('Authsession no match')
        else:
             logger.info('[server-log]: authsession pass !!!')
             if checkerdoctorid == 'doctor':
                  index = _dictret['matchdbid'] 
                  logger.debug('[server-log]: index = %d',index)

                  all_usersmessage = usersmessagemysqldb.objects.all()
           
                  i = 0
                  while i < len(all_usersmessage):
                      i = index
                      #do logic demand handle
                      all_usersmessage[i].IMP_Doctor_RA = IMP_RA 
                      all_usersmessage[i].IMP_Doctor_RB = IMP_RB 
                      all_usersmessage[i].IMP_Doctor_RC = IMP_RC 
                      all_usersmessage[i].IMP_SCHEME = IMP_SCHEME
                      all_usersmessage[i].PEST = int(all_usersmessage[i].PEST) | 0x2 
                      logger.debug('[server-log]: status = %d',int(all_usersmessage[index].PEST))
                      all_usersmessage[i].save()
                      return HttpResponse('doctor result')
                  logger.debug('[server-log]: result_1 = %s,result_2 = %s',  \
                IMP_RA,IMP_RB)
             elif checkerdoctorid == 'consultants':
                  index = _dictret['matchdbid'] 
                  logger.debug('[server-log]: index = %d',index)

                  all_usersmessage = usersmessagemysqldb.objects.all()
           
                  i = 0
                  while i < len(all_usersmessage):
                      i = index
                      #do logic demand handle
                      all_usersmessage[i].IMP_Consultant_RA = IMP_RA 
                      all_usersmessage[i].IMP_Consultant_RB = IMP_RB
                      all_usersmessage[i].IMP_Consultant_RC = IMP_RC 
                      all_usersmessage[i].PEST = int(all_usersmessage[i].PEST) | 0x20 
                      logger.debug('[server-log]: status = %d',int(all_usersmessage[index].PEST))
                      all_usersmessage[i].save()
                      return HttpResponse('consultant result')
                  logger.debug('[server-log-1]: result_1 = %s,result_2 = %s',  \
                IMP_RA,IMP_RB)
        return HttpResponse('result')
#--------------------------------------------------
# 患者方案处理
# 依据医生诊断结果自动分析提供方案或者使用医生直接提供的方案
# reqid = 1 :doctor check patient PE Info to handle
# PEST     7    6    5      4       3      2    1    0
#         保留|保留|会诊师已给出诊断|病历更新|保留|保留|医师已给出诊断|病历更新     
# schemeid  0:暂无治疗方案 1:schemeA   2:schemeB   3:schemeC
#-------------------------------------------------
    def patientschemethandle(request):
       
        authsession = request.POST['authsession']
        _dictret = checkauthsession(authsession)
        has_authsession = _dictret['matchflag']
        
        if has_authsession == 0:
             return HttpResponse('Authsession no match')
        else:
             logger.info('[server-log]: authsession pass !!!')
             index = _dictret['matchdbid'] 
             logger.debug('[server-log]: index = %d',index)
             all_usersmessage = usersmessagemysqldb.objects.all()
             i = 0
             while i <= len(all_usersmessage):
                 i = index
                 #do logic demand handle
                 schemeid = all_usersmessage[i].IMP_SCHEME
                 break
             return JsonResponse({\
                                             'schemeid':schemeid,  \
                                       })

#--------------------------------------------------
# Convert DB to xls format
#-------------------------------------------------
    def handlecovertxls(request):
        authsession = request.POST['authsession']
        _dictret = checkauthsession(authsession)
        has_authsession = _dictret['matchflag']
        if has_authsession == 1:
             os.system('python3 /opt/wxminiprogram_server/wxapp/mysqlcovert_toxls.py')
             return HttpResponse('Server has coverted mysqldb to xls !!!')
        else:
             return HttpResponse('Authsession no match')
