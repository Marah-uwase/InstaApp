from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from .email import send_activation_email
from .tokens import account_activation_token
from .models import Image, Profile,Comments
from .forms import SignupForm,ImageForm,ProfileForm,CommentForm

@login_required(login_url='/')
def home(request):
    images = Image.get_all_images()
    
    return render(request, 'index.html', {'images':images})

def signup(request):
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            to_email = form.cleaned_data.get('email')
            send_activation_email(user, current_site, to_email)
            return HttpResponse('Confirm your email address to complete registration')
    else:
        form = SignupForm()
    return render(request, 'registration/registration_form.html',{'form':form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
        return HttpResponse('Thank you for confirming email. Now login to your account')
    else:
        return HttpResponse('Activation link is invalid')
def profile(request, username):
    profile = User.objects.get(username=username)
    
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    images = Image.get_profile_images(profile.id)
    title = f'@{profile.username} Instagram photos and videos'

    return render(request, 'profile/profile.html', {'title':title, 'profile':profile, 'profile_details':profile_details, 'images':images})

@login_required(login_url='login')
def user_profile(request, username):
    user_pro = get_object_or_404(User, username=username)
    if request.user == user_pro:
        return redirect('profile', username=request.user.username)
    user_posts = user_pro.profile.posts.all()
    
    followers = Follow.objects.filter(followed=user_pro.profile)
    follow_status = None
    for follower in followers:
        if request.user.profile == follower.follower:
            follow_status = True
        else:
            follow_status = False
    context = {
        'user_pro': user_pro,
        'user_posts': user_posts,
        'followers': followers,
        'follow_status': follow_status
    }
    print(followers)
    return render(request, 'profile.html', context)


@login_required(login_url='/accounts/login')
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.profile = request.user
           
            upload.save()
            return redirect('profile', username=request.user)
    else:
        form = ImageForm()
    
    return render(request, 'profile/upload_image.html', {'form':form})
@login_required(login_url='/accounts/login')
def _profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('edit_profile')
    else:
        form = ProfileForm()

    return render(request, 'profile/edit_profile.html', {'form':form})    
@login_required(login_url='/accounts/login')
def single_image(request, image_id):
    image = Image.get_image_id(image_id)
    comments = Comments.get_comments_by_images(image_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.user = request.user
            comment.save()
            return redirect('single_image', image_id=image_id)
    else:
        form = CommentForm()
        
    return render(request, 'image.html', {'image':image, 'form':form, 'comments':comments})  

@login_required(login_url='login')
def search_profiles(request):
    if 'search_user' in request.GET and request.GET['search_user']:
        name = request.GET.get("search_user")
        result = Profile.search_profile(name)
        print(result)
        message = f'name'
        return render(request, 'search.html',{'results': result,'message': message})
    else:
        message = "There's no profile name with that username "
    return render(request, 'search.html', {'message': message})

@login_required(login_url='login')
def unfollow(request, unfollowing):
    if request.method == 'GET':
        user_prof = Profile.objects.get(pk=unfollowing)
        unfollowed = Follow.objects.filter(follower=request.user.profile, followed=user_prof)
        unfollowed.delete()
        return redirect('profile',  username=request.user)


@login_required(login_url='login')
def follow(request, following):
    if request.method == 'GET':
        user_profs = Profile.objects.get(pk=following)
        follower = Follow(follower=request.user.profile, followed=user_profs)
        follower.save()
        return redirect('profile',  username=request.user)

def like_post(request,post_id):
    image = Post.objects.get(id=post_id)
    user = request.user
    image.likes.add(user)
    image.save()
    print(user)
    return redirect('comment',post_id)

       
