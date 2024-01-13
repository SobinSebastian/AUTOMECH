from allauth.account.views import SignupView
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import *
def index(request):
    messages.success(request, 'This is a success message!')
    return render(request,'client/index.html')
def customlogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'ADMIN':
                    u_admin = True
                    return redirect('/admin_home',{'uadmin':u_admin})
                elif user.role == 'MECHANIC':
                    return redirect('mechanic')
                else:
                    messages.success(request, 'Sign in completed successfully!')
                    # try:
                    #     UserInfo.objects.get(user=user)
                    # except UserInfo.DoesNotExist:
                    #     messages.warning(request, 'Please Update Your Details!')
                    return redirect('/')  # Replace 'dashboard' with the URL for your user dashboard
            else:
                user=''
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request,'client/signin.html',{'form':form})

# def register(request):
#     if request.method == 'POST':
#         form = CustomRegistrationForm(request.POST)
#         if form.is_valid():
#             firstname = form.cleaned_data['firstname']
#             lastname = form.cleaned_data['lastname']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             confirmpassword = form.cleaned_data['confirmpassword']
#             username=email 
             
#             if password == confirmpassword:
#                 # Create a new user
#                      if User.objects.filter(email=email).exists():
#                         #messages.error(request, 'User with this email already exists. Please sign in.')
#                         return redirect('login')
#                      else:
#                         user = Client.objects.create_user(username=username,first_name=firstname,last_name=lastname, email=email, password=password)
#                         # views.py or models.py or any other Django module
#                         subject = 'Subject of the email'
#                         message = 'Body of the email'
#                         from_email = settings.DEFAULT_FROM_EMAIL
#                         recipient_list = [email]

#                         send_mail(subject, message, from_email, recipient_list)

#                         return redirect('login')  # Replace 'login' with the URL for your login page
#     else:
#         form = CustomRegistrationForm()
#     return render(request,'client/signup.html',{'form': form})

def signout(request):
    logout(request)
    request.session.flush()
    return redirect('index')

class CustomSignupView(SignupView):
    template_name = 'account/signup.html'
    form_class = CustomSignupForm  # Specify your custom form class
    
    print("#########################################################")
    def form_valid(self, form):
        # Custom logic when the form is valid
        firstname = form.cleaned_data['firstname']
        lastname = form.cleaned_data['lastname']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        confirmpassword = form.cleaned_data['password2']
        email=username
        print(username)
        if password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.error(self.request, 'User with this email already exists. Please sign in.')
                print("######################################################### hello")
                return redirect('account_login')
            else:
                user = Client.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email, password=password)
                # Additional logic for sending email
                subject = 'Subject of the email'
                message = 'Body of the email'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [email]

                send_mail(subject, message, from_email, recipient_list)

                return redirect('account_login')  # Replace with the URL for your login page
        else:
            # Handle the case when passwords don't match
            messages.error(self.request, 'Passwords do not match.')
            return redirect('/')