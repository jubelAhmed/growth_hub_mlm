from django.db import models
import agent.models
from django.contrib.auth.models import User

# Withdraw Type 
BALANCE_WITHDRAW_CHOICES = [
    ("BTC", "Bitcoin"),
    ("PERFECT_MONEY", "Perfect Money"),
    ("SKRILL", 'Skrill'),
    ("NETELLER", 'Neteller'),
    ("PAYPAL", 'PayPal'),
    ("PAYZA", 'Payza'),
]
#  Transection Status
TRANSECTION_STATUS = [
    ("PENDING", "Pending"),
    ("DONE", "Done"),
    ("REJECTED", "Rejected"),
]
# Create your models here.
class AgnetBalance(models.Model):
    agent = models.OneToOneField(User, on_delete=models.CASCADE,related_name="agnetbalance")
    amount = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.agent.username.capitalize() + " - (" + self.agent.email + ")"

class AgentBalanceAdd(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.agent.username + " - (" + self.agent.email + ")"

class AgentBalanceExchange(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE, related_name="receiver" )
    amount = models.FloatField(default=0.0) 
    pin = models.CharField(max_length=250,default=1)
    status = models.CharField(choices=TRANSECTION_STATUS, default="PENDING", max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ' Sender: (' + self.sender.username.capitalize() + ") Receiver: (" + self.receiver.username + ")"

class AgentBalanceWithdraw(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bwagent")
    payment_method = models.CharField(max_length=200, choices=BALANCE_WITHDRAW_CHOICES, default='BTC' )
    amount = models.FloatField(default=0.0)
    pin = models.CharField(max_length=250,default=1)
    accountIdentifier = models.CharField(max_length=250, blank=True, null=True)
    transection_id = models.TextField(blank=True, null=True, default="0")
    status = models.CharField(choices=TRANSECTION_STATUS, default="PENDING", max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.agent.username + " - (" + self.agent.email + ")" + " Amount: (" + str(self.amount) + ")" + " Status: (" + self.status + ")"

class UserBalanceWithdraw(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="ubwuser")
    agent =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="ubwagent")
    amount = models.FloatField(default=0.0)
    withdraw_method = models.CharField(choices=BALANCE_WITHDRAW_CHOICES, default="Bitcoin", max_length=50)
    accountIdentifier = models.CharField(max_length=250, blank=True, null=True)
    pin = models.CharField(max_length=250,default=1)
    status = models.CharField(choices=TRANSECTION_STATUS, default="PENDING", max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  "User: " + self.user.username + " - " + "Agent : " + self.agent.username + " - Amount: (" + str(self.amount) + ")" + " Status: (" + self.status + ")"



class AdminAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="adminaccount")
    btc_address = models.CharField(max_length=250,null=True,blank=True)
    amount = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    