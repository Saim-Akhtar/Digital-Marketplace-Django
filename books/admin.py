from django.contrib import admin
from .models import Book,Author,Chapter,Exercise,Solution, UserLibrary
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    pass

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    pass

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    pass

@admin.register(UserLibrary)
class UserLibraryAdmin(admin.ModelAdmin):
    pass
