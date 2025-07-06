from rest_framework import serializers
from .models import C2BPayment
from .utils import is_valid_phone_number

class C2BPaymentValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = C2BPayment
        fields = ['sender_phone', 'amount']

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")

        if not is_valid_phone_number(data['sender_phone']):
            raise serializers.ValidationError("Phone number must be valid and start with +254...")

        return data
    
class SimulateC2BSerializer(serializers.Serializer):
    shortcode = serializers.CharField(max_length=10)
    amount = serializers.IntegerField(min_value=1)
    phone_number = serializers.CharField(max_length=15)
    bill_ref = serializers.CharField(max_length=50, required=False, default="Test")
    command = serializers.ChoiceField(
        choices=["CustomerPayBillOnline", "CustomerBuyGoodsOnline"],
        default="CustomerPayBillOnline"
    )

    

