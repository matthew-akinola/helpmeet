import os
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from decouple import config
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from django.conf import settings
from django.contrib.sites.models import Site
from drf_spectacular.utils import extend_schema


from .serializers import *

# from .views import CustomSocialLoginView

from_email = config("EMAIL_HOST_USER", "")
api_key = config("MJ_API_KEY", "")
api_secret = config("MJ_API_SECRET", "")


class CustomRegisterView(RegisterView):
    """
    Register New users
    """
    serializer_class = CustomRegisterSerializer



class CustomSocialLoginView(SocialLoginView):
    """
    Google Login- Changing the Serializer class to a Custom made one
    """

    serializer_class = CustomSocialLoginSerializer


site = Site.objects.get(id=getattr(settings, "SITE_ID", 1))


@extend_schema(
    description=f"# Visit this [`link`](https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=https://{site.domain}/accounts/google/login/callback/&prompt=consent&response_type=code&client_id=878674025478-e8s4rf34md8h4n7qobb6mog43nfhfb7r.apps.googleusercontent.com&scope=openid%20email%20profile&access_type=offline) for users to see the google account select modal."
    + """
    After Users select account for login, they will be redirected to a new url.

    extract the `code` query parameter passed in the redirected url and send to this endpoint to get access and refresh tokens

    Example data:

    {

        code : "4%2F0AWafdDkbD_aCTargumCuVFpZSEpImEuZouFACTO1hxoDwqCV1zazen7ev5FmH2w"

    }
    """
)
# if you want to use Authorization Code Grant, use this
class GoogleLogin(CustomSocialLoginView):
    # Local Development link
    # https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://127.0.0.1:8000/accounts/google/login/callback/&prompt=consent&response_type=code&client_id=878674025478-e8s4rf34md8h4n7qobb6mog43nfhfb7r.apps.googleusercontent.com&scope=openid%20email%20profile&access_type=offline

    # CALLBACK_URL_YOU_SET_ON_GOOGLE
    default_call_back_url = "http://127.0.0.1:8000/accounts/google/login/callback/"

    adapter_class = GoogleOAuth2Adapter
    callback_url = os.environ.get("CALLBACK_URL", default_call_back_url)

    client_class = OAuth2Client


class CustomSocialLoginView(SocialLoginView):
    """
    Google Login- Changing the Serializer class to a Custom made one
    """

    serializer_class = CustomSocialLoginSerializer


"""_summary_

    Returns:
        _type_: _description_
class EstateRegistration(APIView):
    "
    A estate registration class.
    An endpoint to create both estate and estate-admin .
    Returns: 
        HTTP_201_CREATED- a success response and created data
    ""
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EstateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = EstateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        admin_registration = serializer.validated_data.pop("estate_admin")
        user = User.objects.create_user(**admin_registration)
        if not user:
            return Response(
                "User registration failed",
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        user.is_admin = True
        user.save()
        estate = serializer.save()
        update_estate = get_object_or_404(
            Estate, estate_name=estate.estate_name
        )
        update_estate.member = user
        update_estate.save()
        Room.objects.get_or_create(user=update_estate)
        return Response(
            {"success": "Account created, check your email and verify"},
            status=status.HTTP_201_CREATED,
        )


class ListEstateAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    
    An endpoint to list available Estate(s)
    Filters the database for available estate
    Response:
        HTTP_200_OK - a success response
    Raise:
        HTTP_404_NOT_FOUND - if no estate found in the database
    

    serializer_class = EstatesSerializer
    queryset = Estate.objects.select_related("member")
    lookup_field = "estate_name"
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if self.get_queryset():
            return Response(
                self.serializer_class(self.get_queryset(), many=True).data,
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "No available Estate"},
            status=status.HTTP_204_NO_CONTENT
        )


class ListEstateAdminAPIView(
    generics.GenericAPIView,
    mixins.ListModelMixin
):

    
    An endpoint to list available Estate-admin
    Filters the database base on the user permission class
    Response:
        HTTP_200_OK - a success response
    Raise:
        HTTP_404_NOT_FOUND - if no estate-admin found in the database
    
    serializer_class = EstateAdminSerializer
    queryset = User.objects.filter(is_user=False)
    lookup_field = "email"
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if self.get_queryset():
            return Response(
                self.serializer_class(self.get_queryset(), many=True).data,
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "No available Estate Admin"},
            status=status.HTTP_204_NO_CONTENT,
        )


class UserAPIView(generics.GenericAPIView, mixins.ListModelMixin):

    
    An endpoint to list available User(s)
    Filters the database base on the user permission class
    Response:
        HTTP_200_OK - a success response and user data
    Raise:
        HTTP_404_NOT_FOUND - if no user found in the database


    serializer_class = ListUserSerializer
    queryset = User.objects.filter(is_user=True)
    lookup_field = "email"
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if self.get_queryset():
            return Response(
                self.serializer_class(self.get_queryset(), many=True).data,
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "No available user"},
            status=status.HTTP_204_NO_CONTENT
        )


class UserRegistration(APIView):
    
    A user registration class
    permits a user to register only if the user's estate exist
    Returns: 
        HTTP_201_CREATED- a success response, serializer data
    Raises: 
        HTTP_404_NOT_FOUND- an error message if estate does not exist
    
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        estate_public_id = serializer.validated_data.pop("estate_id")
        validated_data = serializer.validated_data
        # Verify if the estate details exist in the database
        estate = Estate.objects.filter(
            estate_name=validated_data["estate_name"],
            public_id=estate_public_id,
        )
        if not estate.exists():
            return Response(
                "Estate with given information does not exist",
                status=status.HTTP_404_NOT_FOUND,
            )
        user = User.objects.create_user(**validated_data)
        user.is_user = True
        user.save()
        estate.update(member=user)
        return Response(
            {"Success": "Check your email for verification"},
            status=status.HTTP_201_CREATED,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def User_Email_Verification_Token(request, email):
    
     A Refresh Token class for email verifcation
    A JWT refresh token is created for email verification
    and the token is sent to user's email using MAILJET
    Args:
        email- a user email is provided
    Returns: HTTP_201_created, mailjet data

    Raises: (i) HTTP_404_NOT_FOUND if email doesn't exist
            (ii) HTTP_422_UNPROCESSABLE_ENTITY- if mailjet 
            couldn't send the email
    

    get_token = get_object_or_404(User, email=email)
    if get_token.is_verify is True:
        return Response(
            "User's Email already verified",
            status=status.HTTP_208_ALREADY_REPORTED,
        )
    email_verification_token = RefreshToken.for_user(get_token).access_token
    # current_site = get_current_site(request).domain
    absurl = f"https://help-meet.herokuapp.com/api/v1/user/email-verification?token={email_verification_token}"
    email_body = (
        f"Hi  {get_token.name} Use link below to verify your email"
        "\n" + absurl
    )
    data = {
        "email_body": email_body,
        "to_email": get_token.email,
        "subject": "Verify your email",
    }
    mailjet = Client(auth=(api_key, api_secret), version="v3.1")
    data = {
        "Messages": [
            {
                "From": {
                    "Email": "akinolatolulope24@gmail.com",
                    "Name": "freehouse",
                },
                "To": [
                    {
                        "Email": f"{get_token.email}",
                        "Name": f"{get_token.name}",
                    }
                ],
                "Subject": "Email Verification",
                "TextPart": "Click on the below link to verify your Email!",
                "HTMLPart": email_body,
            }
        ]
    }
    mail_jet_result = mailjet.send.create(data=data)
    if mail_jet_result:
        # print(mail_jet_result.json()["Messages"]["Status"])
        return Response(
            mail_jet_result.json(),
            status=status.HTTP_201_CREATED
        )
    return Response(
        "Email sending failed",
        status=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


class VerifyUserEmail(APIView):

    # Verify user email endpoint

    permission_classes = [AllowAny]

    def get(self, request):
        token = request.GET.get("token")
        print(token)
        access_token_str = str(token)
        try:
            # access token verification
            access_token_obj = AccessToken(access_token_str)
        except Exception as e:
            return Response(
                "No token Input or Token already expired",
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_id = access_token_obj["user_id"]
        print(access_token_obj)
        print(user_id)
        user = get_object_or_404(User, pk=int(user_id))
        if not user.is_verify:
            user.is_verify = True
            user.save()
        return Response(
            {"email": "Email verification is successful"},
            status=status.HTTP_200_OK,
        )

class GET_AND_DELETE_ESTATE(APIView):

    
    #? An endpoint to GET or delete an estate's record.
    Returns a user object.
    Args:
        Email- returns a user data that was provided during registration
    Response:
        HTTP_200_OK, a serailizer data if user exists
        HTTP_204_NO_CONTENT, a success response if estate delete is successful
    Raise:
        HTTP_404- returns not found if a user/estate with 
        the email doesn't exist
    
    permission_classes = [IsAuthenticated]

    def get(self, request, email):
        user = get_object_or_404(User, email=email)
        get_estate = get_object_or_404(Estate, member=user)
        estate_details = EstatesSerializer(get_estate)
        return Response(
            estate_details.data, status=status.HTTP_200_OK
        )

    def delete(self, request, email):
        user = get_object_or_404(User, email=email)
        get_estate = get_object_or_404(Estate, member=user)
        user.delete()
        get_estate.delete()
        return Response(
            "Estate is successfully deleted",
            status=status.HTTP_204_NO_CONTENT
        )


# class GET_AND_DELETE_USER(APIView):

#     
#     An endpoint to GET or DELETE a specific user data
#     Returns an AGENT object
#     Args:
#         Email- supplied as a path paramter argument for user verification
#     Response:
#         HTTP_200_OK, a serailizer data if user exists
#         HTTP_204_NO_CONTENT- a success response if user delete is successful
#     Raise:
#         HTTP_404- an erorr response if user with email doesn't exist
#     

#     authentication_classes = [TokenAuthentication]
#     permisssion_classes = [IsAuthenticated]

#     def get(self, request, email):
#         get_user = get_object_or_404(User, email=email)
#         serializer = ReturnUserInfoSerializer(get_user)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def delete(self, request, email):
#         agent = get_object_or_404(User, email=email)
#         agent.delete()
#         return Response(
#             "Agent deleted successfully", status=status.HTTP_204_NO_CONTENT
#         )

"""
