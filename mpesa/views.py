from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import C2BPaymentValidationSerializer,SimulateC2BSerializer
from .api import simulate_c2b_payment
from .models import C2BPayment
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class C2BPaymentValidationView(APIView):
    def post(self, request):
        serializer = C2BPaymentValidationSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "ResultCode": 0,
                "ResultDesc": "Accepted"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "ResultCode": 1,
                "ResultDesc": "Rejected",
                "Errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

class SimulateC2BPaymentView(APIView):
    def post(self, request):
        serializer = SimulateC2BSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            result = simulate_c2b_payment(
                shortcode=data["shortcode"],
                amount=data["amount"],
                phone_number=data["phone_number"],
                bill_ref=data.get("bill_ref", "Test"),
                command=data.get("command", "CustomerPayBillOnline")
            )
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(csrf_exempt, name='dispatch') 
class ConfirmationView(APIView):
    def post(self,request):
        data = request.data

        try:
            transaction_id = data.get("TransID")

            if C2BPayment.objects.filter(transaction_id=transaction_id).exists():
                return Response({"ResultCode": 0, "ResultDesc": "Duplicate transaction"}, status=200)
            
            full_name = " ".join(filter(None, [
    data.get("FirstName", ""),
    data.get("MiddleName", ""),
    data.get("LastName", "")
]))


            transaction_time = datetime.strptime(data.get("TransTime"), "%Y%m%d%H%M%S")

            payment = C2BPayment.objects.create(
                transaction_type = data.get("TransactionType"),
                transaction_id = transaction_id,
                amount = int(float(data.get("TransAmount"))),
                sender_phone = data.get("MSISDN"),
                sender_name = full_name,
                reference_number = data.get("BillRefNumber"),
                organization_short_code = data.get("BusinessShortCode"),
                transaction_time = transaction_time,
                raw_data = data
            )

            return Response({
                "ResultCode": 0,
                "ResultDesc": "Confirmation Received Successfully"
            }, status=status.HTTP_200_OK)


        except Exception as e:
            return Response({
                "ResultCode": 1,
                "ResultDesc": f"Processing Error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
