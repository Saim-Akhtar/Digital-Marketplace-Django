from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Order,OrderItem, Payment
from books.models import Book

import random
import string
import stripe
stripe.api_key=settings.STRIPE_SECRET_KEY
# Create your views here.

def create_ref_code():
    return ''.join(random.choices(string.ascii_uppercase+ string.digits, k=15))

@login_required
def add_to_cart(request,book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    order_item, created = OrderItem.objects.get_or_create(book=book)
    order, created = Order.objects.get_or_create(user=request.user, is_ordered=False)
    order.items.add(order_item)
    order.save()
    messages.info(request,'Successfully added to cart')
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@login_required
def remove_from_cart(request,book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    order_item = get_object_or_404(OrderItem,book=book)
    order = get_object_or_404(Order, user=request.user, is_ordered=False)
    order.items.remove(order_item)
    order.save()
    messages.info(request,'Successfully removed from cart')

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@login_required
def order_view(request):
    try:
        order = get_object_or_404(Order,user=request.user,is_ordered=False)
    except:
        order={}
    context = {
                "order":order
            }
    return render(request,'shopping_cart/order_summary.html',context)

@login_required
def checkout(request):
    try:
        order = get_object_or_404(Order,user=request.user,is_ordered=False)
        pass
    except:
        return redirect(reverse('cart:order-summary'))
    if request.method == 'POST':
        try:
            order.ref_code = create_ref_code()
            token = request.POST.get('stripeToken')

            charge = stripe.Charge.create(
            amount=int(order.get_total() * 100),
            currency="usd",
            source=token,
            description=f"{request.user.username} charged for book",
            )

            payment = Payment()
            payment.order = order
            payment.total_amount = order.get_total()
            payment.stripe_charge_id = charge.id
            payment.save()

            # adding books to the user book library list
            books = [item.book for item in order.items.all()]
            for book in books:
                request.user.userlibrary.books.add(book)
            
            order.is_ordered = True
            order.save()
            messages.success(request, "Your order was successful!")
            return redirect(reverse("accounts/profile"))

        except stripe.error.CardError as e:
            messages.error(request, "There was a card error.")
            return redirect(reverse("cart:checkout"))
        except stripe.error.RateLimitError as e:
            messages.error(request, "There was a rate limit error on Stripe.")
            return redirect(reverse("cart:checkout"))
        except stripe.error.InvalidRequestError as e:
            messages.error(request, "Invalid parameters for Stripe request.")
            return redirect(reverse("cart:checkout"))
        except stripe.error.AuthenticationError as e:
            messages.error(request, "Invalid Stripe API keys.")
            return redirect(reverse("cart:checkout"))
        except stripe.error.APIConnectionError as e:
            messages.error(
                request, "There was a network error. Please try again.")
            return redirect(reverse("cart:checkout"))
        except stripe.error.StripeError as e:
            messages.error(request, "There was an error. Please try again.")
            return redirect(reverse("cart:checkout"))
        except Exception as e:
            messages.error(
                request, "There was a serious error. We are working to resolve the issue.")
            return redirect(reverse("cart:checkout"))        

    context = {
        "order":order
    }

    return render(request,'shopping_cart/checkout.html',context)