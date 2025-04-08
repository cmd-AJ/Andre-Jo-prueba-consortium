from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import asyncio 
from notificationapi_python_server_sdk import notificationapi
from spending_control.models import Spending
from liquidations.models import Liquidation
from .models import Notification
from django.contrib.auth.models import User
from datetime import datetime

NOTIFICATIONAPI_CLIENT_ID=os.getenv("NOTIFICATIONAPI_CLIENT_ID")
NOTIFICATIONAPI_CLIENT_SECRET=os.getenv("NOTIFICATIONAPI_CLIENT_SECRET")


class EchoDataView(APIView):
    def post(self, request):

        time = datetime.now().strftime("%H:%M:%S")

        data = request.data
        received_date = data.get('received_date', 'N/A')
        received_time = data.get('received_time', 'N/A')
        issuing_entity = data.get('issuing_entity', 'N/A')
        case_number = data.get('case_number', 'N/A')
        recipient = data.get('recipient', 'N/A')
        receptionist = data.get('receptionist', 'N/A')
        internal_delivery_time = time ##JUNTO CON EL COLLABORATOR
        internal_collaborator = data.get('internal_collaborator', 'N/A')
        final_delivery_datetime = str(datetime.strptime(received_date, "%Y-%m-%d").date()) + ":"+time


        notification = Notification.objects.create(
            received_date=received_date,
            received_time=received_time,
            issuing_entity=issuing_entity,
            case_number=case_number,
            recipient=recipient,
            receptionist=receptionist,
            internal_delivery_time=internal_delivery_time,
            internal_collaborator=internal_collaborator,
            final_delivery_datetime=final_delivery_datetime
        )

        return Response({
            "message": "Notification created successfully",
        }, status=status.HTTP_201_CREATED)


    
class SingleAttribute(APIView):
    def post(self, request):
        data = request.data
        time = datetime.now().strftime("%H:%M:%S")
        received_date = data.get('received_date', 'N/A')
        received_time = data.get('received_time', 'N/A')
        issuing_entity = data.get('issuing_entity', 'N/A')
        case_number = data.get('case_number', 'N/A')
        recipient = data.get('recipient', 'N/A')
        receptionist = data.get('receptionist', 'N/A')
        internal_delivery_time = data.get('internal_delivery_time', "N/A")
        internal_collaborator = data.get('internal_collaborator', "N/A")
        final_delivery_datetime =  str(datetime.strptime(received_date, "%Y-%m-%d").date()) +":" + time


      

        async def send_notification():
            try:
                notificationapi.init(
                    NOTIFICATIONAPI_CLIENT_ID, #If using .env, replace this with your clientId env variable
                    NOTIFICATIONAPI_CLIENT_SECRET 
                )
                result = await notificationapi.send({
                    "notificationId": "send_notif",
                    "user": {
                        "id": "ptoribio@consortiumlegal.com",  #ptoribio@consortiumlegal.com
                        "email": "ptoribio@consortiumlegal.com",
                        "number": "+15005550006"
                    },
                    "mergeTags": {
                        "received_date": received_date,
                        "received_time": received_time,
                        "issuing_entity": issuing_entity,
                        "case_number": case_number,
                        "recipient": recipient,
                        "internal_collaborator":  ','.join(internal_collaborator) + ',' + internal_delivery_time,
                        "receptionist": receptionist,
                        "internal_delivery_time": final_delivery_datetime

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
        spendings = Spending.objects.all()

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



class UserListView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        
        user_data = [{"username": user.username, "first_name": user.first_name, "last_name": user.last_name, "email": user.email} for user in users]
        
        return Response(user_data, status=status.HTTP_200_OK)
    


class NotificationListView(APIView):
    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.all()  # Get all notifications
        data = []

        # Optionally, you can customize this response to return only specific fields
        for notification in notifications:
            data.append({
                'received_date': notification.received_date,
                'received_time': notification.received_time,
                'issuing_entity': notification.issuing_entity,
                'case_number': notification.case_number,
                'recipient': notification.recipient,
                'receptionist': notification.receptionist,
                'internal_delivery_time': notification.internal_delivery_time,
                'internal_collaborator': notification.internal_collaborator,
                'final_delivery_datetime': notification.final_delivery_datetime,
            })

        return Response(data, status=status.HTTP_200_OK)
