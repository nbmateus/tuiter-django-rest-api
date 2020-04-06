from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def tuiterAPIRootView(request):
    return Response({
        'accounts_app':{
            'registration':reverse('rest_register',request=request, format=None),
            'login': reverse('rest_login',request=request, format=None),
            'logout':reverse('rest_logout',request=request, format=None),
            'password_reset':reverse('rest_password_reset',request=request, format=None),
            'password_change':reverse('rest_password_change',request=request, format=None),
            'user_details':reverse('rest_user_details',request=request, format=None),

        },
        'postings_app':{
            

        }
        
    })
        
    