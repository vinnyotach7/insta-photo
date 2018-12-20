from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30)
    profile_bio = models.TextField(max_length=50)
    profile_photo = models.ImageField(upload_to='profile/')

    def __str__(self):
        return self.profile_bio

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()
    
    def __str__(self):
        return self.first_name
    
    def save_profile(self):
        self.save()

    @classmethod
    def get_profiles(cls):
        profiles = cls.objects.all()
        return profiles

    @classmethod
    def search_by_username(cls, search_term):
        profiles = cls.objects.filter(title__icontains=search_term)
        return profiles


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Image(models.Model):
    user = models.ForeignKey(User, null=True)
    image_image = models.ImageField(upload_to='images/')
    image_name = models.CharField(max_length=50, null=True)
    image_caption = models.CharField(max_length=50, default="")
    profile = models.ForeignKey(Profile, null=True)
    time_created = models.DateTimeField(auto_now=True, auto_now_add=False)
    time_updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_uploaded = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)

    def save_image(self):
        '''
        method to save image
        '''
        self.save()

    def delete_image(self):
        '''
        method to delete image
        '''
        self.delete()
    
    @classmethod
    def get_images(cls):
        images = cls.objects.all()
        return images

class Comment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='user')
    comment = models.CharField(max_length=80, null=True)
    date_posted = models.DateTimeField(auto_now=True)
    image = models.ForeignKey(Image, related_name='comments', null=True)

    def __str__(self):
        return self.comment
    
    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

    @classmethod
    def get_comments_by_images(cls, id):
        comments = Comments.objects.filter(image__pk = id)
        return comments
