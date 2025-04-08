from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch
from rest_framework import status

class SingleAttributeTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/send_notif/'  # The endpoint for testing

    @patch('yourapp.views.notificationapi.send')  # Mock the external API call
    def test_post_notification(self, mock_send):
        data = {
            "received_date": "2025-04-07",
            "received_time": "09:45",
            "issuing_entity": "Juzgado Primero Civil",
            "case_number": "EXP-2025-04567",
            "recipient": "Lic. Mariana López",
            "receptionist": "Amanda González",
            "internal_delivery_time": "10:15",
            "internal_collaborator": ["Carlos Méndez"],
            "final_delivery_datetime": ["2025-04-07T10:30:00"]
        }

        mock_send.return_value = {"status": "success", "message": "Notification sent successfully"}

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        mock_send.assert_called_once()

        self.assertEqual(response.data['status'], 'Notification sent successfully')

    @patch('yourapp.views.notificationapi.send')  
    def test_post_notification_failure(self, mock_send):
        data = {
            "received_date": "2025-04-07",
            "received_time": "09:45",
            "issuing_entity": "Juzgado Primero Civil",
            "case_number": "EXP-2025-04567",
            "recipient": "Lic. Mariana López",
            "receptionist": "Amanda González",
            "internal_delivery_time": "10:15",
            "internal_collaborator": ["Carlos Méndez"],
            "final_delivery_datetime": ["2025-04-07T10:30:00"]
        }

        mock_send.side_effect = Exception("API request failed")

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        self.assertEqual(response.data['status'], 'Failed to send notification')
