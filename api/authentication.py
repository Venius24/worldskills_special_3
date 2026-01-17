#from rest_framework.authentication import BasicAuthentication as DRFBasicAuth
#from rest_framework.exceptions import AuthenticationFailed
#import base64
#
#class BasicAuthentication(DRFBasicAuth):
#    def authenticate_credentials(self, userid, password, request=None):
#        # Жестко заданные учетные данные
#        if userid == 'staff' and password == 'BCLyon2024':
#            return (None, None)
#        raise AuthenticationFailed('Неверные учетные данные')