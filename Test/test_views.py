from Test.test_setup import TestSetUp
from Authentication.models import User, Estate
import pdb, json

class TestViews(TestSetUp):
    
    def test_user_cannot_register_with_no_data(self):
            res = self.client.post(self.register_url)
            self.assertEqual(res.status_code, 400)


    def test_user_can_register(self):
        response = self.client.post(
            self.estate_registration, 
            self.estate_data,
            format='json'
            )
        get_estate_details = self.client.get(self.estate_list, format='json')
        result = list(get_estate_details)
        result_one =  json.loads(result[0])
        # pdb.set_trace()
        self.user_data[
            'estate_id'] =result_one[0]['public_id']
        res = self.client.post(
            self.register_url, self.user_data, format="json"
        )
        # pdb.set_trace()
        self.assertEqual(res.status_code, 201)


    def test_User_cannot_login(self):
        self.client.post(self.register_url, self.user_data, format="json")
        invalid_user_detail ={
            "email":"akin@gmail.com",
            "password":"werner@004"
        }
        res = self.client.post(
            self.login_url, 
            invalid_user_detail, 
            format="json"
            )
        # pdb.set_trace()
        self.assertEqual(res.status_code, 401)

    def test_VerifiedUser_login(self):
        response = self.client.post(
            self.estate_registration, 
            self.estate_data,
            format='json'
            )
        get_estate_details = self.client.get(self.estate_list, format='json')
        result = list(get_estate_details)
        result_one =  json.loads(result[0])
        # pdb.set_trace()
        self.user_data.update(
            estate_id=result_one[0]['public_id']
            )
        res = self.client.post(
            self.register_url, self.user_data, format="json"
        )
        # pdb.set_trace()
        response = User.objects.get(email=self.user_data["email"])
        response.is_verify = True
        response.is_user = True
        response.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        # pdb.set_trace()
        self.assertEqual(res.status_code, 200)

        

    def test_get_all_user(self):
        response = self.client.post(
            self.estate_registration, self.estate_data, format='json'
            )
        get_estate_details = self.client.get(self.estate_list, format='json')
        result = list(get_estate_details)
        result_one =  json.loads(result[0])
        self.user_data.update(
            estate_id=result_one[0]['public_id']
            )
        self.client.post(self.register_url, self.user_data)
        response = self.client.get(self.user_list)
        result = list(response)
        result_one =  json.loads(result[0])
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 204)
        self.assertEqual(result_one[0]["house_address"], "Lekki toll gate")



    def test_get_all_user_error(self):  
        response = self.client.post(
            self.estate_registration, 
            self.estate_data, 
            format='json'
            )
        get_estate_details = self.client.get(self.estate_list, format='json')
        result = list(get_estate_details)
        result_one =  json.loads(result[0])
        self.user_data.update(
            estate_id='d9erkokfof'
            )
        self.client.post(self.register_url, self.user_data)
        response = self.client.get(self.user_list)
            # pdb.set_trace()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            response.data['error'], 
            "No available user"
            )
        self.assertNotEqual(
            response.data, 
            "successful"
        )
        self.assertNotEqual(response.status_code, 200)

            
    
    def test_get_all_estate(self):
            self.client.post(
                self.estate_registration, 
                self.estate_data, 
                format='json'
                )
            response = User.objects.get(
                email=self.estate_data['estate_admin']["email"]
                )
            response.is_verify = True
            response.is_user = True
            response.save()
            estate_list = self.client.get(self.estate_list)
            result = list(estate_list)
            result_one =  json.loads(result[0])
            self.assertEqual(estate_list.status_code, 200)
            self.assertNotEqual(result_one[0]["estate_name"], "Chevron")
            self.assertEqual(
                result_one[0]["estate_address"], 
                "Plot 34, Galadimawa, Abuja"
                )
            self.assertNotEqual(estate_list.status_code, 204)



    # def test_verifyEmail_endpoint(self):
    #     self.email_verification_url = reverse("verify-email")
    #     self.client.post(self.register_url, self.user_data)
    #     # pdb.set_trace()
    #     token = self.client.get(self.email_verification_url)
    #     self.assertEqual(token.status_code, 400)
    #     self.assertEqual(
    #         token.data, 
    #         "No token Input or Token already expired"
    #         )
        
        

    def test_admin_logout_endpoint(self):
        self.client.post(self.estate_registration, self.estate_data, format="json")
        response = User.objects.get(email=self.estate_data['estate_admin']["email"])
        response.is_verify = True
        response.save()
        login = self.client.post(
            self.login_url, 
            self.admin_login_data, format="json"
            )
        auth_token= json.loads(login.content).get("refresh")
        refresh_token = {
            "refresh_token": f"{auth_token}"
        }
        logout_user = self.client.post(self.logout_url, refresh_token)
        self.assertEqual(logout_user.status_code, 204)



    def test_forgetPassword_endpoint(self):
        res = self.client.post(self.estate_registration, self.estate_data, format="json")
        # pdb.set_trace()
        response = User.objects.get(email=self.estate_data['estate_admin']["email"])
        response.is_verify = True
        response.save()
        password_reset = self.client.put(
            (self.forgetPassword_url),
            self.forgetPassword_data,
        )
        self.assertEqual(password_reset.status_code, 200)
        self.assertNotEqual(
            password_reset.data, "password reset is successful"
        )

    def test_get_and_delete_user_endpoint(self):
        self.getAndDeleteUser_url = "/api/v1/user/get/"
        response = self.client.post(
            self.estate_registration, self.estate_data, format='json'
            )
        get_estate_details = self.client.get(self.estate_list, format='json')
        result = list(get_estate_details)
        result_one =  json.loads(result[0])
        self.user_data.update(
            estate_id=result_one[0]['public_id']
            )
        self.client.post(self.register_url, self.user_data)
        response = User.objects.get(email=self.user_data["email"])
        response.is_verify = True
        response.save()
        # you need to login to get token before you can delete a user
        login = self.client.post(
            self.login_url, self.user_data, format="json"
            )
        auth_token= login.data['refresh']
        header= {'Authorization':'Token '+ auth_token}
        get_user = self.client.get(
            (self.getAndDeleteUser_url + str(self.user_data['email'])), 
            headers=header,
            format='json'
        )
        delete_user = self.client.delete(
            (self.getAndDeleteUser_url + str(self.user_data['email'])), 
            headers=header,
            format = 'json'
        )
        self.assertEqual(get_user.status_code, 200)
        self.assertEqual(delete_user.status_code, 204)
        self.assertNotEqual(get_user.data["name"], "wreco")



    def test_get_and_delete_estate_endpoint(self):
        self.getAndDeleteAgent_url = "/api/v1/estate/get/"
        self.client.post(
            self.estate_registration, self.estate_data, format="json"
            )
        estate_admin = User.objects.get(
            email=self.estate_data['estate_admin']["email"]
            )
        # pdb.set_trace()
        estate_admin.is_verify = True
        estate_admin.save()
        login = self.client.post(
            self.login_url, 
            self.admin_login_data, 
            format="json"
            )
        auth_token= json.loads(login.content).get("refresh")
        header= {'Authorization':'Token '+ auth_token}
        get_estate = self.client.get(
            (self.getAndDeleteAgent_url + str(estate_admin.email)),
            headers=header
        )
        delete_user = self.client.delete(
            (self.getAndDeleteAgent_url + str(estate_admin.email)),
            headers=header
        )
        self.assertEqual(get_estate.status_code, 200)
        self.assertEqual(delete_user.status_code, 204)
        self.assertNotEqual(delete_user.status_code, 200)
        self.assertEqual(get_estate.data["estate_name"], "Suncity")
        self.assertEqual(
            get_estate.data["member"]['email'], "wreco@gmail.com"
            )

