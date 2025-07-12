from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Service, ServiceCategory, Booking
from .forms import BookingForm

def home(request):
    categories = ServiceCategory.objects.all().prefetch_related('services')
    featured_services = Service.objects.filter(is_active=True).order_by('-created_at')[:6]
    return render(request, 'services/home.html', {
        'categories': categories,
        'featured_services': featured_services
    })

def service_list(request, category_slug=None):
    category = None
    services = Service.objects.filter(is_active=True)
    
    if category_slug:
        category = get_object_or_404(ServiceCategory, slug=category_slug)
        services = services.filter(category=category)
    
    query = request.GET.get('q')
    if query:
        services = services.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    return render(request, 'services/services.html', {
        'category': category,
        'services': services,
        'query': query or ''
    })

@login_required
def book_service(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            
            if booking.booking_date < timezone.now():
                messages.error(request, "Booking date must be in the future")
            else:
                booking.save()
                messages.success(request, 
                    f"Your booking for {service.name} has been submitted! "
                    f"We'll confirm your appointment soon."
                )
                return redirect('services:my_bookings')
    else:
        default_date = timezone.now().replace(
            hour=9, minute=0, second=0, microsecond=0
        ) + timezone.timedelta(days=1)
        form = BookingForm(initial={'booking_date': default_date})
    
    return render(request, 'services/book.html', {
        'form': form,
        'service': service
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('service').order_by('-booking_date')
    return render(request, 'services/bookings.html', {'bookings': bookings})

@user_passes_test(lambda u: u.is_staff)
def admin_response(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        response_text = request.POST.get('response')
        new_status = request.POST.get('status')
        
        if response_text:
            booking.admin_response = response_text
            booking.status = new_status
            booking.save()
            messages.success(request, "Response submitted successfully!")
            return redirect('admin:services_booking_changelist')
    
    return render(request, 'services/admin/response.html', {
        'booking': booking,
        'status_choices': Booking.STATUS_CHOICES
    })