import time
from django.http import JsonResponse

from authentication_app.models import AppUser
from authentication_app.utils.email_service import EmailService
from authentication_app.utils.password_validator import generate_password_hash, check_password
from authentication_app.utils.serializers import SignInRequestSerializer, SignInResponseSerializer, UserSerializer
from authentication_app.utils.serializer_objects import SignInRequest, SignInResponse
from authentication_app.utils.token_setup import generate_token
from django.contrib.auth.models import AnonymousUser


# TODOS
    # 1.Implement email validator

class AuthenticateUserService:
    ''' AuthenticationUserService class to implement user authentication [post, get, put, delete] services '''

    def get_token_time(self):
        time_to_expire = 60 * 1 * 60 * 5
        current_time_in_seconds = time.time()
        token_expiration_time = current_time_in_seconds + time_to_expire
        return token_expiration_time

    def post_authenticate_user(self, request_data):
        '''
        check for authentication post service and add user to database
        ------------
        parameters
        ------------
        request_data: str (client request body)
        returns: JsonResponse
        '''
        try:
            email = request_data["email"]
            user = AppUser.objects.get(email=email)
            return JsonResponse({"message": f"AppUser with email {email} already exist"})               
        except AppUser.DoesNotExist:
            hashed_password = generate_password_hash(request_data["password"])
            request_data["password"] = hashed_password.decode('UTF-8')
            serializer = UserSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                # email_service = EmailService(email=serializer.data["email"], message="SignUp successful")
                # email_service.send_mail()
                return JsonResponse({"message": "User added successfully"})
            return JsonResponse({"message": "Invaid form data"})

    def get_authenticate_user(self, request_data: SignInRequest):
        '''
        check for authentication get service and retrieve user from database
        ------------
        parameters
        ------------
        request_data: str (client request body)
        returns: JsonResponse
        '''

        expiration_time = self.get_token_time()
        signin_request = SignInRequest(email=request_data["email"], password=request_data["password"])
        serializer = SignInRequestSerializer(signin_request)
        email = serializer.data["email"]
        password = serializer.data["password"]

        if email and password:
            try:
                user = AppUser.objects.get(email=email)
                valid_password = check_password(password, user.password.encode('UTF-8'))
                if valid_password:
                    # email_service = EmailService(
                    #     email=serializer.data["email"], 
                    #     message=f"AppUser {serializer.data['first_name']} {serializer.data['last_name']} logged in"
                    #     )
                    # email_service.send_mail()
                    token = generate_token(
                        {"email": user.email, "exp": expiration_time}
                    )
                    
                    if token:
                        signin_response = SignInResponse(
                            message="User signin successfully",
                            token= token
                        )
                        serializer = SignInResponseSerializer(signin_response)
                        return JsonResponse(serializer.data)
                    return JsonResponse({"message": "Server error generating token"})
                return JsonResponse({"message": "Invalid password"})
            except AppUser.DoesNotExist:
                return JsonResponse({"message": f"AppUser with email {email} does not exist"} )
        return JsonResponse({"message": "Email or Password not provided"})

    def put_authenticate_user(sef, request, email):
        '''
        check for authentication put service and update existing user info in the database
        ------------
        parameters 
        ------------
        request: request (client request object)
        email: str (user email)
        returns: JsonResponse
        '''
        try:
            user = AppUser.objects.get(email=email)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return JsonResponse(serializer.data)
        except AppUser.DoesNotExist:
            return JsonResponse({"message": f"user with email {email} does not exist"} )
    
    def delete_authenticate_user(self, request, email):
        '''
        check for authentication delete service and delete user from database
        ------------
        parameters
        ------------
        request: request (client request object)
        email: str (user email)
        returns: JsonResponse
        '''
        try:
            user = AppUser.objects.get(email=email)
            user.delete()
            return JsonResponse({"data": {"message": f"user {email} deleted sucessfully"}})
        except AppUser.DoesNotExist:
            return JsonResponse({"message": f"user with email {email} does not exist"} )
