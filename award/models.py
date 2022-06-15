from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    # projects = models.ManyToOneField()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

# class Category(models.Model):
#     name =models.CharField(max_length=255)


#     def __str__(self):
#         return self.name 

#     def get_absolute_url(self):
#         return reverse('home')
        # return reverse('article-detail', args=(str(self.id)))

class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    body = models.TextField()
    post_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=255, default='coding')
    image = models.ImageField(default='default.jpg', upload_to='images')
    likes = models.ManyToManyField(User, related_name='blog_posts')
    
    def total_likes(self):
        return self.likes.count()


    def __str__(self):
        return self.title + '|' + str(self.author)

    def get_absolute_url(self):
        return reverse('home')
        # return reverse('article-detail', args=(str(self.id)))

    def save_post(self):
        return self.save()

    def update_caption(self, body):
        return self.body.update()
        

    def delete_post(self):
        return self.delete()