from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import *
def index(request):
    messages.success(request, 'This is a success message!')
    return render(request,'client/index.html')
def login(request):
    return render(request,'client/signin.html')
def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirmpassword = form.cleaned_data['confirmpassword']
            role="CLIENT"
            username=email 
             
            if password == confirmpassword:
                # Create a new user
                     if User.objects.filter(email=email).exists():
                        #messages.error(request, 'User with this email already exists. Please sign in.')
                        return redirect('login')
                     else:
                        user = User.objects.create_user(username=username,first_name=firstname,last_name=lastname, email=email, password=password,role=role)
                # You can also perform additional actions like sending confirmation emails, etc.
                        return redirect('login')  # Replace 'login' with the URL for your login page
    else:
        form = CustomRegistrationForm()
    return render(request,'client/signup.html',{'form': form})