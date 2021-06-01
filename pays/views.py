from django.shortcuts import render
import razorpay
from.models import Coffee
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home(request):
    if request.method=="POST":
        name=request.POST.get("name")
        amount=int(request.POST.get("amount")) * 100
        client=razorpay.Client(auth=("rzp_test_IOPsUtuaNxhdlC", "aOnJWUMKjNjIHNumhPp8YscN"))   # First one is the public key. 2nd is secret or private key. Get it from razorpay dashboard
        payment=client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1'})
        print(payment)
        coffee=Coffee(name=name, amount=amount, payment_id=payment['id'])
        coffee.save()
        return render(request,'index.html', {'payment': payment})   # We are rendering index,html again because we want a "Pay with Razorpay" button on this page only
    return render(request,'index.html')

@csrf_exempt
def success(request):
    if request.method == "POST":
        a=request.POST
        print(a)
        order_id=a['razorpay_order_id']
        user=Coffee.objects.filter(payment_id=order_id).first()
        user.paid=True
        user.save()
        

    return render(request,'success.html')
