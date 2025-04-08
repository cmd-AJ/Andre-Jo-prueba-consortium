from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import asyncio 
from notificationapi_python_server_sdk import notificationapi
from spending_control.models import Spending
from liquidations.models import Liquidation
from django.core import serializers

NOTIFICATIONAPI_CLIENT_ID=os.getenv("NOTIFICATIONAPI_CLIENT_ID")
NOTIFICATIONAPI_CLIENT_SECRET=os.getenv("NOTIFICATIONAPI_CLIENT_SECRET")


class EchoDataView(APIView):
    def post(self, request):
        data = request.data
        # Extract specific fields if needed
        received_date = data.get('received_date', 'N/A')
        received_time = data.get('received_time', 'N/A')
        issuing_entity = data.get('issuing_entity', 'N/A')
        case_number = data.get('case_number', 'N/A')
        recipient = data.get('recipient', 'N/A')
        receptionist = data.get('receptionist', 'N/A')
        internal_delivery_time = data.get('internal_delivery_time', 'N/A')
        internal_collaborator = data.get('internal_collaborator', 'N/A')
        final_delivery_datetime = data.get('final_delivery_datetime', 'N/A')




        return Response({
            "received_data": {
                "received_date": received_date,
                "received_time": received_time,
                "issuing_entity": issuing_entity,
                "case_number": case_number,
                "recipient": recipient,
                "receptionist": receptionist,
                "internal_delivery_time": internal_delivery_time,
                "internal_collaborator": internal_collaborator,
                "final_delivery_datetime": final_delivery_datetime,
            }
        }, status=status.HTTP_200_OK)
    
class SingleAttribute(APIView):
    def post(self, request):
        data = request.data
        # Extract specific fields if needed
        received_date = data.get('received_date', 'N/A')
        received_time = data.get('received_time', 'N/A')
        issuing_entity = data.get('issuing_entity', 'N/A')
        case_number = data.get('case_number', 'N/A')
        recipient = data.get('recipient', 'N/A')
        receptionist = data.get('receptionist', 'N/A')
        internal_delivery_time = data.get('internal_delivery_time', 'N/A')
        internal_collaborator = data.get('internal_collaborator', [])
        final_delivery_datetime = data.get('final_delivery_datetime', [])

        combined = ", ".join([f"{collaborator}, {datetime}" for collaborator, datetime in zip(internal_collaborator, final_delivery_datetime)])

        # If the arrays are different lengths, handle that case (e.g., just add the extra items to the result)
        if len(internal_collaborator) > len(final_delivery_datetime):
            combined += ", " + ", ".join(internal_collaborator[len(final_delivery_datetime):])
        elif len(final_delivery_datetime) > len(internal_collaborator):
            combined += ", " + ", ".join(final_delivery_datetime[len(internal_collaborator):])

        async def send_notification():
            try:
                notificationapi.init(
                    NOTIFICATIONAPI_CLIENT_ID, #If using .env, replace this with your clientId env variable
                    NOTIFICATIONAPI_CLIENT_SECRET 
                )
                result = await notificationapi.send({
                    "notificationId": "send_notif",
                    "user": {
                        "id": "ptoribio@consortiumlegal.com",
                        "email": "ptoribio@consortiumlegal.com",
                        "number": "+15005550006"
                    },
                    "mergeTags": {
                        "received_date": received_date,
                        "received_time": received_time,
                        "issuing_entity": issuing_entity,
                        "case_number": case_number,
                        "recipient": recipient,
                        "internal_collaborator": combined,
                        "receptionist": receptionist,
                        "internal_delivery_time": internal_delivery_time

                    }
                })
                return True, result  # success
            except Exception as e:
                return False, str(e)  # error message

        sent, result_or_error = asyncio.run(send_notification())

        if sent:
            return Response({
                "status": "Notification sent successfully",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "Failed to send notification",

            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class ServerAliveView(APIView):
    def get(self, request):
        return Response({"status": "Server is alive!"}, status=status.HTTP_200_OK)
    



class SpendingListView(APIView):
    def get(self, request, format=None):
        # Fetch all spendings
        spendings = Spending.objects.all()

        # Manually format the queryset into a list of dictionaries
        spendings_data = []
        for spending in spendings:
            spendings_data.append({
                'id': spending.id,
                'created_by': spending.created_by.id,  # assuming creator is a ForeignKey
                'created_at': spending.created_at,
                'liquidation_sent': spending.liquidation_sent.url if spending.liquidation_sent else None,
                'account_status': spending.account_status.url if spending.account_status else None,
                'invoice': spending.invoice.url if spending.invoice else None,
                'type': spending.type,
                'status': spending.status,
                'totals_match': spending.totals_match,
                'justification': spending.justification,
            })

        # Return the manually formatted data in the response
        return Response(spendings_data)


class LiquidationListView(APIView):
    def get(self, request, *args, **kwargs):
        # Query all liquidations
        liquidations = Liquidation.objects.all()
        
        # Create a list of dictionaries to return USE FOR JSONARRAY
        liquidation_data = []
        for liquidation in liquidations:
            liquidation_data.append({
                "id": liquidation.id,
                "created": liquidation.created,
                "creator": liquidation.creator.id, 
                "document_type_code": liquidation.document_type_code,
                "invoice_nit": liquidation.invoice_nit,
                "invoice_serie": liquidation.invoice_serie,
                "invoice_number": liquidation.invoice_number,
                "invoice_name": liquidation.invoice_name,
                "invoice_adress": liquidation.invoice_adress,
                "total_value": str(liquidation.total_value),  
                "description": liquidation.description,
                "document_link": liquidation.document_link,
                "state": liquidation.get_state_display(), 
                "is_devolution": liquidation.is_devolution,
                "elimination_reason": liquidation.elimination_reason,
                "document": liquidation.document.url if liquidation.document else None, 
            })
        
        return Response(liquidation_data, status=status.HTTP_200_OK)
