from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



#################### index####################################### 
def index(request):
    return render(request, 'app/index.html', {'title':'HOME'})

  
########### register here ##################################### 
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            ######################### mail system #################################### 
            htmly = get_template('app/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ################################################################## 
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {'form': form, 'title':'register here'})
  
################ login forms################################################### 
def Login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'app/login.html', {'form':form, 'title':'log in'})

def logout_view(request):
    logout(request)
    # Custom logic, if any
    return redirect('index')

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'app/password_reset.html'
    email_template_name = 'app/password_reset_email.html'
    subject_template_name = 'app/password_reset_subject.txt'
    success_message = "We emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you dont receive an email, " \
                      "please make sure you were entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('index')


from .models import File
from .forms import FileForm
from django.http import HttpResponseNotFound
from django.urls import reverse
import uuid

@login_required
def add_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            # Generate a unique public_url using UUID
            file.public_url = str(uuid.uuid4())
            file.save()
            # Redirect to the blog detail view with the correct public_url
            return redirect('index1')  # Change this to the appropriate URL name for your blog list view
    else:
        form = FileForm()
    return render(request, 'app/add_file.html', {'form': form, 'title': 'ADD FILE'})

@login_required
def index1(request):
    user_files = File.objects.filter(user=request.user)
    return render(request, 'app/index1.html', {'user_files': user_files, 'title': 'ALL FILES'})
def file_detail(request, public_url):
    try:
        file = File.objects.get(public_url=public_url)
        return render(request, 'app/file_detail.html', {'file': file, 'title': 'FILE'})
    except File.DoesNotExist:
        return HttpResponseNotFound('<h1>File not found</h1>')
@login_required
def get_absolute_url(self):
        return reverse('file_detail', args=[str(self.public_url)])


from .forms import ContactForm
from django.core.mail import EmailMessage
@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = f"Message from {name}"
            body = f"Sender's email: {email}\n\nMessage:\n{message}"
            
            # Create and send the email
            email_message = EmailMessage(
                subject=subject,
                body=body,
                from_email=email,  # Sender's email address from the form
                to=['2000031715cse@gmail.com'],  # Replace with your recipient's email address
                reply_to=[email],  # Set the reply-to address to sender's email
            )
            email_message.send()
            
            return redirect('success')  # Display a success page
    else:
        form = ContactForm()
    return render(request, 'app/contact.html', {'form': form, 'title': 'CONTACT US'})

def success(request):
    return render(request, 'app/success.html',{'title': 'SUCCESS'})
@login_required
def edit_file(request, file_id):
    # Retrieve the file object from the database
    file = get_object_or_404(File, pk=file_id)
    
    # Check if the form is submitted
    if request.method == 'POST':
        # Populate the form with POST data and the file object
        form = FileForm(request.POST, instance=file)
        if form.is_valid():
            # Save the form if it's valid
            form.save()
            # Redirect to a different page after successful form submission
            return redirect('index1')  # Redirect to all blogs page
    else:
        # If the request is not POST, create a form instance with the file object
        form = FileForm(instance=file)
    
    # Render the template with the form and file object in the context
    return render(request, 'app/edit_file.html', {'form': form, 'file': file, 'title': 'EDIT FILE', 'form_title': 'Edit File', 'button_label': 'Update File'})
@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    if request.method == 'POST':
        file.delete()
        # Redirect to a suitable page after deleting
        return redirect('index1')
    # return render(request, 'accounts/delete_blog.html', {'blog': blog})

from .forms import UploadPDFForm
from .models import UploadedPDF

@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_pdf = form.save(commit=False)
            uploaded_pdf.user = request.user
            uploaded_pdf.save()
            uploaded_pdf.public_url = uploaded_pdf.pdf_file.url
            uploaded_pdf.save()
            return redirect('pdf_list')
    else:
        form = UploadPDFForm()
    return render(request, 'app/upload_pdf.html', {'form': form, 'title': 'ADD PDFS'})
@login_required
def pdf_list(request):
    pdfs = UploadedPDF.objects.filter(user=request.user)
    return render(request, 'app/pdf_list.html', {'pdfs': pdfs,'title': 'ALL PDFS'})


from .models import UploadedPDF
from .forms import UploadPDFForm  # Corrected import statement

@login_required
def delete_pdf(request, pdf_id):
    pdf = get_object_or_404(UploadedPDF, pk=pdf_id)
    if request.method == 'POST':
        pdf.delete()
        return redirect('pdf_list')  # Redirect to the page where PDFs are listed
    return render(request, 'delete_pdf_confirm.html', {'pdf': pdf})

@login_required
def edit_pdf(request, pdf_id):
    pdf = get_object_or_404(UploadedPDF, pk=pdf_id)
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES, instance=pdf)  # Updated form name
        if form.is_valid():
            form.save()
            return redirect('pdf_list')  # Redirect to the page where PDFs are listed
    else:
        form = UploadPDFForm(instance=pdf)  # Updated form name
    return render(request, 'app/edit_pdf.html', {'form': form})


def about(request):
    return render(request, 'app/about_us.html', {'title':'ABOUT US'})

def services(request):
    return render(request, 'app/services.html', {'title':'SERVICES'})

def privacypolicy(request):
    return render(request, 'app/privacyandpolicy.html', {'title':'PRIVACY & POLICY'})

def terms(request):
    return render(request, 'app/terms.html', {'title':'TERMS'})

from .forms import UploadImageForm  # Corrected import statement
from .models import UploadedImage  # Corrected import statement

from django.conf import settings
from django.core.files.storage import default_storage
from django.urls import reverse

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save(commit=False)
            uploaded_image.user = request.user
            uploaded_image.save()
            uploaded_image.public_url = settings.MEDIA_URL + str(uploaded_image.image_file)
            uploaded_image.save()
            return redirect('image_list')
    else:
        form = UploadImageForm()
    return render(request, 'app/upload_image.html', {'form': form, 'title': 'ADD IMAGES'})
@login_required
def image_list(request):
    images = UploadedImage.objects.filter(user=request.user)
    return render(request, 'app/image_list.html', {'images': images, 'title': 'ALL IMAGES'})

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(UploadedImage, pk=image_id)
    if request.method == 'POST':
        image.delete()
        return redirect('image_list')
    return render(request, 'delete_image_confirm.html', {'image': image})

@login_required
def edit_image(request, image_id):
    image = get_object_or_404(UploadedImage, pk=image_id)
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = UploadImageForm(instance=image)
    return render(request, 'app/edit_image.html', {'form': form})