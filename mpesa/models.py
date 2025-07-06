from django.db import models

# Create your models here.
class C2BPayment(models.Model):
    transaction_type = models.CharField(max_length=10)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.PositiveIntegerField()
    sender_phone = models.CharField(max_length=15)
    sender_name = models.CharField(max_length=100)
    reference_number = models.CharField(max_length=100, blank=True, null=True)

    organization_short_code = models.CharField(max_length=10) 
    transaction_time = models.DateTimeField()
    raw_data = models.JSONField(blank=True, null=True)  

    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_phone} - {self.amount} - {self.transaction_id}"
    

