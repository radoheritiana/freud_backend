from rest_framework import generics
from authentication.serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt



class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        #print(request.content_type)

        if 'multipart/form-data' in request.content_type:
            data = request.data
        else:
            data = request.data.dict() if isinstance(request.data, QueryDict) else request.data

        serializer = self.get_serializer(instance, data=data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPIView(generics.GenericAPIView):
    
    serializer_class = RegisterSerializer
    authentication_classes = []
    
    
    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return response.Response({"status": True, "user": serializer.data}, status=status.HTTP_201_CREATED)
        
        return response.Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class LoginAPIView(generics.GenericAPIView):
    
    serializer_class = LoginSerializer
    authentication_classes = []
    
    @csrf_exempt
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        
        user = authenticate(username=email, password=password)
        if user:
            serializer = self.serializer_class(user)
            return response.Response({'status': True, 'user': serializer.data}, status=status.HTTP_200_OK)
        
        return response.Response({'status': False, 'message': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


