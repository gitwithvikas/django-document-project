from django.shortcuts import render,redirect

# Create your views here.

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from .models import UserProfile
from django.contrib.auth.decorators import login_required
import os
import io
import zipfile
from django.http import HttpResponse
from django.conf import settings


# from rest_framework import viewsets
# from .models import UserProfile
# from .serializers import UserSerializer, UserProfileSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     # queryset = User.objects.all()
#     # serializer_class = UserSerializer

   


# class UserProfileViewSet(viewsets.ModelViewSet):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer


def register(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(name,email,password)
        
        user = User.objects.create_user(username=name,email=email, password=password)
        # user_profile, created = UserProfile.objects.get_or_create(user=user)
        auth_login(request, user)
        return redirect('login')
    return render(request, 'register.html')
 

def login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            return redirect('uploadDoc')
    return render(request, 'login.html')


@login_required
def uploadDoc(request):
      print(request)
      if request.method=='POST':
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        user_profile.profile_photo = request.FILES.get('profile_photo')
        user_profile.aadhar_card = request.FILES.get('aadhar_card')
        user_profile.pan_card = request.FILES.get('pan_card')
        user_profile.voter_id_proof = request.FILES.get('voter_id_proof')
        user_profile.marksheet = request.FILES.get('marksheet')

        user_profile.save()

      user_profile = UserProfile.objects.get(user=request.user)
      print(user_profile)
      return render(request, 'uploadDoc.html', {'user_profile': user_profile})
    # return render(request, 'uploadDoc.html')

@login_required
def download_documents(request):
    user_profile = UserProfile.objects.get(user=request.user)
    print('myuser',user_profile.user_id)
    # Collect all image fields from the UserProfile model
    image_fields = [
        user_profile.profile_photo,
        user_profile.aadhar_card,
        user_profile.pan_card,
        user_profile.voter_id_proof,
        user_profile.marksheet,
    ]

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        for field in image_fields:
            print('myfield' ,field)
            if field:
              
                file_path = os.path.join(settings.MEDIA_ROOT,str(field))
                print('filepath ' , file_path)
                # Add the image to the ZIP archive with the original file name
                zipf.write(file_path, os.path.basename(file_path))
    
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename=user_documents.zip'
    return response