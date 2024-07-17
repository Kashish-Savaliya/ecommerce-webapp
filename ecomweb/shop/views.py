from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import stripe
import json
from django.views.decorators.csrf import csrf_exempt
# from PayTm import Checksum
# Create your views here.

def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    print("Search function called")
    if request.method == 'POST':
        query = request.POST.get('search', '')
        allProds = []
        catprods = Product.objects.values('category','id')
        cats = {item['category'] for item in catprods}
        for cat in cats:
            prodtemp = Product.objects.filter(category=cat)  # filters the products acc. to category
            prod = [item for item in prodtemp if searchMatch(query, item)]
            n = len(prod)
            no_of_slides = n // 4 + ceil((n / 4) - (n // 4))
            if len(prod) !=0:
                allProds.append([prod, range(1, no_of_slides), no_of_slides])
        params = {'allProds': allProds,'msg':''}
        if len(allProds) == 0 or len(query) < 4:
            print('Please make sure to enter relevant search query')
            params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def index(request):
    # products = Product.objects.all()
    # params = {'product': products, 'no_of_slides': no_of_slides, 'range': range(1, no_of_slides)}
    print('Inside index')
    allProds = []
    catprods = Product.objects.values('category', 'id')           #The values() method returns a queryset of dictionaries, where each dictionary represents a row from the database table,
                                                                    # containing only the specified fields ('category' and 'id' in this case).
                                                                    # Example -<QuerySet>[
                                                                    # {'category': 'Category A', 'id': 1},
                                                                    # {'category': 'Category B', 'id': 2},
                                                                    # {'category': 'Category A', 'id': 3}
                                                                    #]
    cats = {item['category'] for item in catprods}        # iterates over each dictionary in catprods and collects unique category values into a set. Ex-Collecting unique category values into a set:
                                                            # 'Category A'
                                                            # 'Category B'
    for cat in cats:
        prod = Product.objects.filter(category=cat)             #filters the products acc. to category
        n = len(prod)
        no_of_slides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, no_of_slides), no_of_slides])
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", '')
        email = request.POST.get("email", '')
        phone = request.POST.get("phone", '')
        desc = request.POST.get("desc", '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
        return render(request, 'shop/contact.html', {'thank': thank})
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == 'POST':
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({'status':'success' ,'updates': updates, 'items_json':order[0].items_json}, default=str)
                    # print(order[0].items_json)
                return HttpResponse(response)
            else:
                # print('hello')
                return HttpResponse("{'status':'noitem'}")
        except Exception as e:
            print(e)
            return HttpResponse("{'status':'error'}")
    return render(request, 'shop/tracker.html')


def productView(request, myId):
    # fetch the product using id in list format
    product = Product.objects.filter(id=myId)
    # print(product)
    return render(request, 'shop/prodView.html', {'product': product[0]})

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get("items_json", '')
        name = request.POST.get("name", '')
        email = request.POST.get("email", '')
        amount = request.POST.get("amount", '')
        phone = request.POST.get("phone", '')
        city = request.POST.get("city", '')
        state = request.POST.get("state", '')
        zip_code = request.POST.get("zip_code", '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        order = Order(items_json=items_json, name=name, email=email, phone=phone, city=city, state=state, zip_code=zip_code, address=address, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
    return render(request, 'shop/checkout.html')


stripe.api_key = settings.STRIPE_SECRET_KEY


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    id = Order.order_id
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        try:
            charge = stripe.Charge.create(
                amount=int(product.price * 100),  # Stripe charges are in cents
                currency='inr',
                description=product.product_name,
                source=token,
            )
            order = Order.objects.create(
                product=product,
                stripe_payment_intent_id=charge.id,
                has_paid=True
            )
            return redirect('paymentstatus.html', order_id=order.id)
        except stripe.error.StripeError:
            # Handle the error
            return redirect('paymentstatus.html')

    return render(request, 'product_detail.html',
                  {'product': product, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY, 'id':id})

