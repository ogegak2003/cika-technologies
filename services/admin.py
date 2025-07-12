from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import format_html
from .models import ServiceCategory, Service, Booking

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon_preview')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
    def icon_preview(self, obj):
        return format_html(f'<i class="bi bi-{obj.icon}"></i> {obj.icon}') if obj.icon else "-"
    icon_preview.short_description = "Icon"

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration_display', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing & Duration', {
            'fields': ('price', 'duration'),
            'description': 'Duration is in minutes'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def duration_display(self, obj):
        return f"{obj.duration} mins"
    duration_display.short_description = "Duration"

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'booking_date', 'status_badge', 'created_at')
    list_filter = ('status', 'service__category', 'booking_date')
    search_fields = ('user__username', 'service__name')
    readonly_fields = ('created_at', 'response_date')
    date_hierarchy = 'booking_date'
    actions = ['mark_confirmed', 'mark_completed', 'mark_cancelled']
    
    def status_badge(self, obj):
        colors = {
            'pending': 'warning',
            'confirmed': 'success',
            'completed': 'primary',
            'cancelled': 'danger'
        }
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            colors[obj.status],
            obj.get_status_display()
        )
    status_badge.short_description = "Status"
    
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f"{updated} bookings marked as confirmed")
    mark_confirmed.short_description = "Mark as confirmed"
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f"{updated} bookings marked as completed")
    mark_completed.short_description = "Mark as completed"
    
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f"{updated} bookings marked as cancelled")
    mark_cancelled.short_description = "Mark as cancelled"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='services_dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        from django.db.models import Count, Q
        context = {
            **self.admin_site.each_context(request),
            'active_services': Service.objects.filter(is_active=True).count(),
            'total_bookings': Booking.objects.count(),
            'pending_bookings': Booking.objects.filter(status='pending').count(),
            'recent_bookings': Booking.objects.select_related('user', 'service')
                              .order_by('-created_at')[:10],
            'popular_services': Service.objects.annotate(
                                  booking_count=Count('bookings')
                              ).order_by('-booking_count')[:5],
        }
        return TemplateResponse(request, "admin/services/dashboard.html", context)