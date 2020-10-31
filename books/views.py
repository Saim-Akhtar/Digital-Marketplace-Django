from django.http import Http404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,reverse
from .models import Book, Chapter, Exercise
from shopping_cart.models import Order, OrderItem


OWNED = 'owned'
IN_CART = 'in_cart'
NOT_IN_CART = 'not_in_cart'

def verify_book_relation(user,book):
    if book in user.userlibrary.book_list():
        return OWNED
    try:
        user_order = get_object_or_404(Order,user=user,is_ordered=False)
        order_item = get_object_or_404(OrderItem,book=book)
        if order_item in user_order.items.all():
            return IN_CART
    except:
        return NOT_IN_CART

# Create your views here.

def book_list(request):
    queryset = Book.objects.all()
    context = {
        "books": queryset
    }
    return render(request,"books/book_list.html",context)

@login_required
def book_details(request,slug):
    book = get_object_or_404(Book, slug=slug)
    if book:
        book_status = ''
        if request.user.is_authenticated:
            book_status = verify_book_relation(request.user,book)
            print(book_status)
        context = {
        "book":book,
        "book_status":book_status
        }
        return render(request,'books/book_detail.html',context)
    raise Http404
  
@login_required
def chapter_detail(request,book_slug,chapter_number):
    chapter = Chapter.objects.filter(Q(book__slug=book_slug) & Q(chapter_number=chapter_number))
    if chapter.exists():
        book_status = ''
        if request.user.is_authenticated:
            book_status = verify_book_relation(request.user,chapter[0].book)
        context = {
            'chapter':chapter[0],
            "book_status":book_status
        }
        return render(request,'books/chapter_detail.html',context)

    raise Http404

@login_required
def exercise_detail(request,book_slug,chapter_number,exercise_number):
    exercise = Exercise.objects.filter( \
        Q(chapter__book__slug=book_slug) & \
        Q(chapter__chapter_number=chapter_number) &\
        Q(exercise_number=exercise_number))
    
    if exercise.exists():
        book_status = ''
        if request.user.is_authenticated:
            book_status = verify_book_relation(request.user,exercise[0].chapter.book)
        context = {
            'exercise':exercise[0],
            'book_status':book_status
        }
        return render(request,'books/exercise_detail.html',context)
    
    raise Http404