from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignupForm, ProfileForm, ImageForm, CommentForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from .models import Image, Profile
from django.core.mail import EmailMessage
from .email import send_welcome_email


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            user.is_active = False
            user.save()
            profile = Profile(user=user)
            profile.save()
            send_welcome_email(name, email)
            current_site = get_current_site(request)
            
            return HttpResponse('Please confirm your email to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/registration_form.html', {'form': form})


@login_required(login_url="/accounts/login/")
def hello(request):
    images = Image.objects.all()
    co_form = CommentForm()
    return render(request, 'instagram/index.html', {"images": images, "co_form": co_form})


@login_required
def edit_profile(request):
    images = Image.objects.all()
    profile = Profile.objects.filter(user=request.user)
    current_user = request.user
    photos = Image.objects.filter(user=current_user)
    prof_form = ProfileForm()
    if request.method == 'POST':
        prof_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if prof_form.is_valid:
            prof_form.save()
        else:
            prof_form = ProfileForm()
            return render(request, 'instagram/edit-profile.html', {"image_form": image_form, "photos": photos, "profile": profile, "images": images})
    return render(request, 'instagram/edit-profile.html', {"prof_form": prof_form, "photos": photos, "profile": profile, "images": images})


@login_required(login_url="/accounts/login/")
def view_profile(request):
    current_user = request.user
    profile = Profile.objects.filter(user=request.user)
    images = Image.objects.filter(user=request.user)
    return render(request, 'instagram/profile.html', {'images': images, 'profile': profile, })

@login_required(login_url="/accounts/login/")
def upload_image(request):
    current_user = request.user
    if request.method == 'POST':
        image_form = ImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.save(commit=False)
            image.user = current_user
            image.save()
        return render(request, 'instagram/upload-image.html', {"image_form": image_form})

    else:
        image_form = ImageForm()
    return render(request, 'instagram/upload-image.html', {"image_form": image_form})


@login_required
def new_comment(request, id):
    upload_comment = Image.objects.get(id=id)
    if request.method == 'POST':
        co_form = CommentForm(request.POST)
        if co_form.is_valid():
            comment = co_form.save(commit=False)
            comment.user = request.user
            comment.image = upload_comment
            comment.save()
        return redirect('/')

# @login_required
# def other_profiles(request,id):
#     other_profile = Profile.objects.get(user_id=id)
#     user_images=Image.objects.filter(user_id=id)

#     return render(request,'instagram/other-profile.html',{"other_profile":other_profile,"user_images":user_images})


@login_required
def search_user(request):

    if 'user' in request.GET and request.GET["user"]:
        search_term = request.GET.get("user")
        searched_users = User.objects.filter(username=search_term)
        message = f"{search_term}"

        return render(request, 'instagram/search.html', {"message": message, "users": searched_users})

    else:
        message = "You haven't searched for any user"
        return render(request, 'instagram/search.html', {"message": message, "users": searched_users})


@login_required
def single_image(request, project_id):
    image = Image.objects.get(id=project_id)
    return render(request, 'instagram/single-image.html', {"image": image})


def home(request):
    date = dt.date.today()

    return render(request, 'registration/homepage.html', {"date": date, })


@login_required(login_url='/home')
def index(request):
    date = dt.date.today()
    photos = Image.objects.all()
    # print(photos)
    profiles = Profile.objects.all()
    # print(profiles)
    form = CommentForm()

    return render(request, 'instagram/index.html', {"date": date, "photos": photos, "profiles": profiles, "form": form})


@login_required(login_url='/accounts/login/')
def comment(request, image_id):
    #Getting comment form data
    if request.method == 'POST':
        image = get_object_or_404(Image, pk=image_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.image = image
            comment.save()
    return redirect('index')
