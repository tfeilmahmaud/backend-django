from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from django.http import HttpResponse
import jwt , datetime
from rest_framework import status



def options_login(request):
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = 'http://localhost:3000'  # Remplacez ceci par l'URL de votre frontend
    response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
def aPage(request):

    return JsonResponse({"UserName":"",
                         "email":"email"})

@api_view(['POST'])
def registerView(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def LoginView(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email=email).first()

    if not user:
        raise AuthenticationFailed('User not found!')
    
    if not user.check_password(password):
        raise AuthenticationFailed('Incorrect password')

    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')

    return Response({'jwt': token}, status=status.HTTP_200_OK)



@api_view(['GET'])
def UserView(request):
    token = request.COOKIES.get('jwt')
    algorithm = ["HS256"]

    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=algorithm)
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')  

    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)
    return Response(serializer.data) 
    
@api_view(['POST'])
def LogoutView(request):
    response=Response()
    response.delete_cookie('jwt')
    response.data={
        'message':'success'
    }
    return response
    


