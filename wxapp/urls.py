from django.urls import path
from wxapp.wxappstruct import wxappstruct
urlpatterns =[

      ################## [testfunc] ####################
      path('helloworld',wxappstruct.testfunc),
      path('wxsubscribes',wxappstruct.wxsubscribes),
      path('onlogin',wxappstruct.onlogin),
      path('usermesgsubmit',wxappstruct.idmessagehandle),
      path('fileupload',wxappstruct.fileupload),
      path('querymysqldb',wxappstruct.querymysqldb),
      path('patientcasemesgsubmit',wxappstruct.patientcasehandle),
      path('diagnoseresultsubmit',wxappstruct.diagnoseresulthandle),
      path('handlemysqltoxls',wxappstruct.handlecovertxls),
      path('wxsignature',wxappstruct.wxcheckSignature),
      path('patientscheme',wxappstruct.patientschemethandle),

]
 
