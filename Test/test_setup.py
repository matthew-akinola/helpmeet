from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    def setUp(self):
        self.estate_registration = reverse("estate-registration")
        # self.get_and_delete_user = reverse("get-and-delete-user")
        # self.get_and_delete_estate = reverse("get-and-delete-estate")
        self.register_url = reverse("user-registration")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.email_verification = reverse("email-verification")
        self.logout_url = reverse("logout")
        self.estate_list = reverse("list-estate")
        self.user_list = reverse("list-user")
        self.forgetPassword_url = reverse("forget-password")
        self.admin_list = reverse("admin-list")
        # self.refresh_token= reverse("refresh-token")        
        self.estate_data = {
            "estate_admin":{
                "email": "wreco@gmail.com",
                "password": "Password@01"
            },
            "estate_address": "Plot 34, Galadimawa, Abuja",
            "estate_country": "AF",
            "estate_name": "Suncity"
        }
        self.user_data = {
            "email": "wrecode@gmail.com",
            "house_address": "Lekki toll gate",
            "password": "Password@01",
            "estate_id":"",
            "name": "string",
            "estate_name": "Suncity"
        }
        self.admin_login_data = {
            "email": "wreco@gmail.com",
            "password": "Password@01"
        }
        self.user_login_data = {
            "email": "wrecode@gmail.com",
            "password": "Password@01"
        }
        self.forgetPassword_data = {
            "email": "wreco@gmail.com",
            "password": "Password@011",
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
