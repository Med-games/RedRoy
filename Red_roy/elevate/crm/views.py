from django.shortcuts import render,redirect,get_object_or_404
from .models import Event, BlogPost,Reservation,BlogImage,ReservationClient
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.template.loader import render_to_string
import qrcode
import io 
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.http import HttpResponseForbidden,HttpResponse,HttpResponseBadRequest
from .decorators import admin_v8_required
import base64

@admin_v8_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        return JsonResponse({})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)
    
@admin_v8_required
def delete_reservation_Client(request, reservation_id):
    reservation = get_object_or_404(ReservationClient, id=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        return JsonResponse({})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)

@admin_v8_required
def update_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        
        if title and content:
            post.title = title
            post.content = content
            post.save()
            messages.success(request, "The post has been updated.")
            return redirect('posts')
        else:
            messages.error(request, "Please fill in all fields.")
    
    return render(request, 'crm/update_post.html', {'post': post})
@admin_v8_required
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    messages.success(request, "The post has been deleted.")
    return redirect('posts')

@admin_v8_required
def v8_template(request):
    b=request.session.get('b')
    reservations = Reservation.objects.all()
    reservationClient=ReservationClient.objects.all()
    query = request.GET.get('search')
    query1 = request.GET.get('search1')
    if query1:
        reservationClient = reservationClient.filter(name__icontains=query1)
    if query:
        reservations = reservations.filter(user__username__icontains=query)
    if request.method == 'POST':
        if 'event_name' in request.POST:
            event_name = request.POST.get('event_name')
            event_date = request.POST.get('event_date')
            event_time = request.POST.get('event_time')
            available_places = request.POST.get('available_places')
            event_price = request.POST.get('event_price')
            event_description = request.POST.get('event_description')
            event_image = request.FILES.get('event_images')
            event_type = request.POST.get('event_type')  # Retrieve the event type from the form data
            if not event_image:
                    event_image = 'media/1.png'
            Event.objects.create(
                title=event_name,
                date=event_date,
                time=event_time,
                available_places=available_places,
                price=event_price,
                description=event_description,
                image=event_image,
                espace=event_type
            )
            return redirect('v8_template')
            
        if 'blog_title' in request.POST:
            title = request.POST.get('blog_title')
            content = request.POST.get('blog_content')
            images = request.FILES.getlist('blog_images')

            # Create BlogPost instance
            blog_post = BlogPost.objects.create(
                title=title,
                content=content,
                created_at=timezone.now()
            )

            # Check if there are images and create BlogImage instances if present
            if images:
                for image in images:
                    BlogImage.objects.create(blog_post=blog_post, images=image)

            return redirect('v8_template')
    return render(request, 'crm/admin.html', {'events': Event.objects.all(),
                                              'Reservations': reservations,
                                              'b':b,
                                              'blogs': BlogPost.objects.all(),
                                              'reservationClient':reservationClient})


def email(request):
    return render(request,'crm/email_client.html')

def login_admin(request):
    return render(request,'crm/login-admin.html')


def custom_logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')  
        
        try:
            user = User.objects.create_user(username=username, password=password)
            messages.success(request, f'Account created successfully for {username}!')
            return redirect('home')  
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('register')  
    
    return render(request, 'crm/index.html')  

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('crm/index')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'crm/login.html')
def home(request):
    return render(request,'crm/index.html')


def events(request):
    events = Event.objects.all()
    event_type = request.GET.get('event_type', 'all')

    if event_type != 'all':
        events = events.filter(espace=event_type)
    
    if request.method == 'POST':
        event_title = request.POST.get('modal-title')
        places = request.POST.get('places')
        name = request.POST.get('name')
        tel=request.POST.get('tel')
        email = request.POST.get('email')
        total_price = request.POST.get('totalPrice')
        event = get_object_or_404(Event, title=event_title)

        if places and name and email and total_price and event.available_places >= int(places):
            reservation =ReservationClient.objects.create(
                event_title=event_title,
                places=places,
                name=name,
                email=email,
                total_price=(total_price)
            )
            event.available_places -= int(places)
            event.save()
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data( f"Event Title: {event_title}\n"
            f"Events: {event_title}\n"
            f"places:{places}\n"
            f"name: {name}\n"
            f"total price: {total_price}"
            )
            qr.make(fit=True)

            qr_img_io = io.BytesIO()
            qr.make_image().save(qr_img_io, 'PNG')
            qr_img_io.seek(0)
            qr_img_base64 = base64.b64encode(qr_img_io.getvalue()).decode()

            # Create the email 
            subject = 'Reservation Confirmation'
            html_content = render_to_string('crm/email_Client.html', {'reservation': reservation,'qr_img_base64': qr_img_base64})
            text_content = strip_tags(html_content)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [email]

            # Create the email message with HTML content
            email_message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            email_message.attach_alternative(html_content, "text/html")

            # Attach the QR code image to the email
            email_message.attach('reservation_qr.png', qr_img_io.read(), 'image/png')

            # Send the email
            email_message.send()

            return redirect('events')
        else:
            return HttpResponseBadRequest("Missing required fields or places not avaible.")

    return render(request, 'crm/events.html', {'events': events})



@login_required
def reset_b(request):
    request.session['b'] = 0
    return JsonResponse({})


@login_required
def reservation(request):
    b = request.session.get('b', 0)
    if request.method == 'POST':
        # Get reservation details from the form
        places = request.POST.get('places')
        association = request.POST.get('association')
        date = request.POST.get('date')
        time = request.POST.get('time')
        phone = request.POST.get('phone')
        espace = request.POST.get('espace')
        b += 1
        if Reservation.objects.filter(date=date, espace=espace).exists():
            messages.error(request, 'This date and space are already reserved. Please choose another date or space.')
            return redirect('reservation')
        else:
            request.session['b'] = b
            reservation = Reservation.objects.create(
                user=request.user,
                places=places,
                association=association,
                date=date,
                time=time,
                phone=phone,
                espace=espace
            )
            

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f"Places: {places}\nAssociation: {association}\nDate: {date}\nTime: {time}\nPhone: {phone}\nEspace: {espace}")
            qr.make(fit=True)

            qr_img_io = io.BytesIO()
            qr.make_image().save(qr_img_io, 'PNG')
            qr_img_io.seek(0)

            # Create the email 
            subject = 'Reservation Confirmation'
            html_content = render_to_string('crm/email.html', {'reservation': reservation})
            text_content = strip_tags(html_content)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [request.user.email]

            # Create the email message with HTML content
            email_message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            email_message.attach_alternative(html_content, "text/html")

            # Attach the QR code image to the email
            email_message.attach('reservation_qr.png', qr_img_io.read(), 'image/png')

            # Send the email
            email_message.send()

            return redirect('success')  
    else:
        context = {
            'name': request.user.username,
            'email': request.user.email,
            'b':b
        }
        return render(request, 'crm/reservation.html', context)

def success(request):
    return render(request, 'crm/success.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, BlogPost

def posts(request):
    events = Event.objects.all()
    posts = BlogPost.objects.order_by('-created_at')
    
    if request.method == 'POST':
        if 'delete_post' in request.POST:
            post_id = request.POST.get('post_id')
            post = get_object_or_404(BlogPost, pk=post_id)
            post.delete()
            return redirect('posts')  # Redirect to the same page after deletion
    
    return render(request, 'crm/posts.html', {'events': events, 'posts': posts})




@admin_v8_required
def delete_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return JsonResponse({"message": "Event deleted successfully."})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)

@admin_v8_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.title = request.POST.get('event_name')
        event.date = request.POST.get('event_date')
        event.time = request.POST.get('event_time')
        event.available_places = request.POST.get('available_places')
        event.price = request.POST.get('event_price')
        event.description = request.POST.get('event_description')
        if request.FILES.get('event_images'):
            event.image = request.FILES.get('event_images')
        event.save()
        return redirect('v8_template')
    return render(request, 'crm/update_event.html', {'event': event})

def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'crm/post_detail.html', {'post': post})



