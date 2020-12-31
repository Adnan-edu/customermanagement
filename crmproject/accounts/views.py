from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
#To create multiple form within one form
from django.forms import inlineformset_factory
from .forms import OrderForm
from .filters import OrderFilter

# Create your views here.



def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {
        'orders':orders,
        'customers':customers,
        'total_customers':total_customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending
    }
    return render(request,'accounts/dashboard.html',context)

def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{
        'products':products
    })

def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    #Filter-We are first going to query all the orders.
    
    orders = customer.order_set.all()
    orders_count = orders.count()
    #We are going to throw them into this filter
    #And based on request data is-request.GET we are going to filter this data down
    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer,'orders':orders,'orders_count':orders_count
    ,'myFilter':myFilter}
    return render(request,'accounts/customer.html',context)

def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    customer = Customer.objects.get(id=pk)
    #form = OrderForm(initial={'customer':customer})
    #queryset=Order.objects.none() - If we have already order objects there don't reference them.
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)#Item instances we are going to fill out in this form

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order) #We are posting new post data into the previous instance inorder to avoid creating a new instance again
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)