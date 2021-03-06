from django.urls import path
from .views import (
    book_list,
    book_details,
    chapter_detail,
    exercise_detail
)

app_name='books'

urlpatterns = [
    path('',book_list,name='book_list'),
    path('<slug:slug>/',book_details,name='book_detail'),
    path('<book_slug>/<int:chapter_number>',chapter_detail,name='chapter_detail'),
    path('<book_slug>/<int:chapter_number>/<int:exercise_number>',exercise_detail,name='exercise_detail')
]