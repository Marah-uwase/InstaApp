from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField



# Create your models here.
class Image(models.Model):
    image=models.ImageField(upload_to = 'images/')
    name = models.CharField(max_length =30)
    caption = models.TextField(max_length =30)
    post_date = models.DateTimeField(auto_now=True)
    likes = models.BooleanField(default=False)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    def save_image(self):
        self.save()  
    @classmethod
    def update_caption(cls, update):
        pass
    
    @classmethod
    def get_image_id(cls, id):
        image = Image.objects.get(pk=id)
        return image
    
    @classmethod
    def get_profile_images(cls, profile):
        images = Image.objects.filter(profile__pk = profile)
        return images
    
    @classmethod
    def get_all_images(cls):
        images = Image.objects.all()
        return images

class Profile(models.Model):
    
    prof_pic = models.ImageField(upload_to = 'profile_pictures/')
    bio = HTMLField()
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)

    def save_profile(self):
        self.save()
    
    @classmethod
    def search_profile(cls, name):
        profile = Profile.objects.filter(user__username__icontains = name)
        return profile
    
    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user = id).first()
        return profile    

class Comments(models.Model):
    comment = HTMLField()
    posted_on = models.DateTimeField(auto_now=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save_comment(self):
        self.save()
    
    @classmethod
    def get_comments_by_images(cls, id):
        comments = Comments.objects.filter(image__pk = id)
        return comments  

class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} Follow'
