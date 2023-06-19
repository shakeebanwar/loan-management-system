from django.db import models
import uuid

# Create your models here.


user_role =(
    ("user", "user"),
    ("manager", "manager"),
      
) 

loan_status =(
    ("pending", "pending"),
    ("approved", "approved"),
    ("rejected", "rejected"),
  
)

loan_pay_status =(
    ("paid", "paid"),
    ("unpaid", "unpaid")
  
)


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    class Meta:
        abstract = True


class Account(BaseModel):

    fname=models.CharField(max_length=255)
    lname=models.CharField(max_length=255)
    address=models.TextField()
    email=models.EmailField(max_length=255)
    password=models.TextField()
    contact = models.CharField(max_length=20)
    role = models.CharField(choices = user_role,max_length=10,default="user")

    def __str__(self):
        return self.email
    

class loan_amount(BaseModel):

    status = models.CharField(choices = loan_status,max_length=10,default="pending")
    loan_due_date = models.DateTimeField(blank=True, null=True)
    amount=models.FloatField()
    pay_status = models.CharField(choices = loan_pay_status,max_length=10,default="pending")
    manager_comment = models.TextField(default="")
    account_id=models.ForeignKey(Account , on_delete=models.CASCADE,blank=True,null=True)
