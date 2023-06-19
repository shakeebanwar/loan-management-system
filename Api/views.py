from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
import Api.usable as uc
from django.http import HttpResponse
from passlib.hash import django_pbkdf2_sha256 as handler
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from datetime import datetime,timedelta
import jwt
from decouple import config
# Create your views here.


def index(request):

    return HttpResponse("<h1>Django Assessment</h1>")


class ManagerSignup(APIView):
    def post (self,request):
        requireFields = ['fname','lname','address','email','password','contact']
        validator = uc.keyValidation(True,True,request.data,requireFields)

        if validator:
            return Response(validator,status = 200)

        else:
            try:
                fname = request.data.get('fname')
                lname = request.data.get('lname')
                address = request.data.get('address')
                email = request.data.get('email')
                password = request.data.get('password')
                contact = request.data.get('contact')


                if uc.checkemailforamt(email):
                    if not uc.passwordLengthValidator(password):
                        return Response({"status":False, "message":"Password should not be than 8 or greater than 20"})

                    checkemail=Account.objects.filter(email=email).first()
                    if checkemail:
                        return Response({"status":False, "message":"Email already exists"})

                    checkcontact=Account.objects.filter(contact=contact).first()
                    if checkcontact:
                        return Response({"status":False, "message":"phone no already existsplease try different number"})

                    data = Account(fname=fname,lname=lname,password= handler.hash(password),email = email,
                    address=address,contact=contact,role="manager")


                    data.save()

                    return Response({"status":True,"message":"Account Created Successfully"})

                else:
                    return Response({"status":False,"message":"Email Format Is Incorrect"})

            except Exception as e:

                return Response({'Message':"Internal Server Error"})



class UserSignup(APIView):
    def post (self,request):
        requireFields = ['fname','lname','address','email','password','contact']
        validator = uc.keyValidation(True,True,request.data,requireFields)

        if validator:
            return Response(validator,status = 200)

        else:
            try:
                fname = request.data.get('fname')
                lname = request.data.get('lname')
                address = request.data.get('address')
                email = request.data.get('email')
                password = request.data.get('password')
                contact = request.data.get('contact')


                if uc.checkemailforamt(email):
                    if not uc.passwordLengthValidator(password):
                        return Response({"status":False, "message":"Password should not be than 8 or greater than 20"})

                    checkemail=Account.objects.filter(email=email).first()
                    if checkemail:
                        return Response({"status":False, "message":"Email already exists"})

                    checkcontact=Account.objects.filter(contact=contact).first()
                    if checkcontact:
                        return Response({"status":False, "message":"phone no already existsplease try different number"})

                    data = Account(fname=fname,lname=lname,password= handler.hash(password),email = email,
                    address=address,contact=contact,role="user")


                    data.save()

                    return Response({"status":True,"message":"Account Created Successfully"})

                else:
                    return Response({"status":False,"message":"Email Format Is Incorrect"})

            except Exception as e:

                return Response({'Message':"Internal Server Error"})


class login(APIView):
     def post(self,request):
         requireFields = ['email','password']
         validator = uc.keyValidation(True,True,request.data,requireFields)

         print("Done",validator)
         if validator:
            return Response(validator,status = 200)

         else:
            # try:

               email = request.data.get('email')
               password = request.data.get('password')
               fetchAccount = Account.objects.filter(email=email).first()
               if fetchAccount:
                  if handler.verify(password,fetchAccount.password):
                    if fetchAccount.role == 'manager':
                        access_token_payload = {
                           'fname':str(fetchAccount.fname),
                           "role": fetchAccount.role,
                           'exp': datetime.utcnow() + timedelta(days=22),
                           # 'iat': datetime.datetime.utcnow(),
                           }


                        access_token = jwt.encode(access_token_payload,config('managerkey'),algorithm = 'HS256')
                        data = {'fname':fetchAccount.fname,'lname':fetchAccount.lname,'email':fetchAccount.email,'address':fetchAccount.address,'role':fetchAccount.role}

                        
                        #

                        return Response({"status":True,"message":"Login Successlly","token":access_token,"manager":data})

                    if fetchAccount.role  == 'user':
                        access_token_payload = {
                           'id':str(fetchAccount.uuid),
                           'fname':fetchAccount.fname,
                           "role": fetchAccount.role,
                           'exp': datetime.utcnow() + timedelta(days=22),
                           # 'iat': datetime.datetime.utcnow(),

                           }


                        access_token = jwt.encode(access_token_payload,config('userkey'),algorithm = 'HS256')
                        data = {'fname':fetchAccount.fname,'lname':fetchAccount.lname,'email':fetchAccount.email,'address':fetchAccount.address,'role':fetchAccount.role}

                        


                        return Response({"status":True,"message":"Login Successlly","token":access_token,"user":data})
                    else:
                        return Response({"status":False,"message":"Unable to login"})
                  else:
                     return Response({"status":False,"message":"Invalid Creadientialsl"})
               else:
                  return Response({"status":False,"message":"Unable to login"})

            # except Exception as e:

            #    return Response({'Message':"Internal Server Error"})




class Getloan(APIView):
   def get(self, request):
      try:
         my_token = uc.usertokenauth(request.META['HTTP_AUTHORIZATION'][7:])
         if my_token:
            data = loan_amount.objects.filter(account_id =  my_token['id']).values('status','amount')
            return Response ({"status":True,"data":data })
         else:
            return Response ({"status":False,"message":"Unauthorized"})

      except Exception as e:

         return Response({'Message':"Internal Server Error"})


from datetime import datetime, timedelta

class Loan(APIView):
    def post(self, request):
        requireFields = ['amount']
        validator = uc.keyValidation(True, True, request.data, requireFields)

        if validator:
            return Response(validator, status=200)

        else:
            my_token = uc.usertokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                amount = request.data.get('amount')

                # Check if user has already made a request within the last 24 hours
                today = datetime.now().date()
                start_of_day = datetime.combine(today, datetime.min.time())
                end_of_day = datetime.combine(today, datetime.max.time())

                previous_request = loan_amount.objects.filter(account_id=my_token['id'], created_at__range=(start_of_day, end_of_day)).first()

                if previous_request:
                    return Response({"status": False, "message": "You have already made a request today"})

                checkAccount = Account.objects.filter(uuid=my_token['id']).first()

                if checkAccount:
                    last_amount = loan_amount.objects.filter(account_id=checkAccount).order_by('-uuid').first()
                    if last_amount and amount - last_amount.amount < 500:
                        return Response({"status": False, "message": "Loan amount must have a minimum gap of 500 from the previous loan"})

                data = loan_amount(amount=amount, account_id=checkAccount)
                data.save()

                return Response({"status": True, "message": "Loan amount added successfully"})
            else:
                return Response({"status": False, "message": "Unauthorized"})



class LoanActive (APIView):

   def put (self,request):
      try:
        my_token = uc.managertokenauth(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            uuid = request.data.get('uuid')
            status = request.data.get('status')
            manager_comment = request.data.get('manager_comment')

            if status == "approved":
                print("approved")
                checkaccount = loan_amount.objects.filter(uuid = uuid).first()

                if checkaccount:
                    checkaccount.status = 'approved'
                    checkaccount.manager_comment = manager_comment
                    checkaccount.save()
                    return Response({"status":True,"message":"Loan Request Approved Successfully"})

            if status == "rejected":
                print("rejected")
                checkaccount = loan_amount.objects.filter(uuid = uuid).first()

                if checkaccount:
                    checkaccount.status = 'rejected'
                    checkaccount.manager_comment = manager_comment
                    checkaccount.save()
                    return Response({"status":True,"message":"Loan Request Rejected Successfully"})

                else:
                    return Response({"status":False,"message":"Data not found"})
            else:
                return Response({"status":False,"message":"Data not found"})

        else:
                return Response({"status": False, "message": "Unauthorized"})
      except Exception as e:

         return Response({'Message':"Internal Server Error"})


