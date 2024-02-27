from django.db import models

# Create your models here.

class Blog(models.Model):
    # a blog the user is reading about
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        # return a string representation of the model
        return self.text
    

# class blog_post