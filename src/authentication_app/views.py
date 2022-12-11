from rest_framework.views import APIView

from authentication_app.utils.auth_service import AuthenticateUserService
from authentication_app.utils.user_auth_service import UserTokenAuthentication
from authentication_app.utils.auth_decorator import check_authenticated_user
class AuthenticateUser(APIView):
    '''
    API View for user authentication
    '''

    authentication_classes = [UserTokenAuthentication]

    def __init__(self):
        self.authenticate_user_service = AuthenticateUserService()

    def post(self, request):
        return self.authenticate_user_service.post_authenticate_user(request.data)
        
    def get(self, request):
        return self.authenticate_user_service.get_authenticate_user(request.data)

    @check_authenticated_user
    def put(self, request, email):
        return self.authenticate_user_service.put_authenticate_user(request, email)
    
    @check_authenticated_user
    def delete(self, request, email):
        return self.authenticate_user_service.delete_authenticate_user(request, email)
