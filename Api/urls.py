from django.urls import path,include
from Api.views import *

urlpatterns = [
### LOGIN ###
path('ManagerSignup',ManagerSignup.as_view()),
path('UserSignup',UserSignup.as_view()),
path('Getloan',Getloan.as_view()),
path('login',login.as_view()),
path('Loan',Loan.as_view()),
path('LoanActive',LoanActive.as_view()),
 path('',index),
]
