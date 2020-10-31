from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserLibrary(models.Model):
    books = models.ManyToManyField('Book',blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def book_list(self):
        return self.books.all()

    class Meta:
        verbose_name = 'User Library'
        verbose_name_plural = 'User Library'

@receiver(post_save,sender=User)
def post_user_signup_receiver(sender,instance,created,**kwargs):
    if created:
        UserLibrary.objects.get_or_create(user=instance)

class Author(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    slug = models.SlugField(unique=True,null=False,max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=50)
    publication_date = models.DateTimeField()
    isbn = models.CharField(max_length=16)
    slug = models.SlugField(unique=True)
    cover = models.ImageField()
    price = models.FloatField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:book_detail',kwargs={
            "slug":self.slug
        })

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter_number = models.IntegerField()
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('books:chapter_detail',kwargs={
            "book_slug":self.book.slug,
            "chapter_number":self.chapter_number
        })

class Exercise(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    exercise_number = models.IntegerField()
    page_number = models.IntegerField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:exercise_detail',kwargs={
            "book_slug":self.chapter.book.slug,
            "chapter_number":self.chapter.chapter_number,
            "exercise_number":self.exercise_number
        })

class Solution(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    solution_number = models.IntegerField()
    image = models.ImageField()

    def __str__(self):
        return f"{self.exercise.title}-{self.pk}"