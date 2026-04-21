from django.contrib import admin
# DİKKAT: Buraya 'Reservation' eklendi
from .models import Vehicle, Insurance, Reservation

class InsuranceInline(admin.StackedInline):
    model = Insurance
    can_delete = False
    verbose_name_plural = 'Insurance Details'

class VehicleAdmin(admin.ModelAdmin):
    inlines = [InsuranceInline]
    list_display = ('brand', 'model', 'vehicle_type', 'fuel_type', 'transmission', 'daily_rate', 'status')
    list_filter = ('status', 'vehicle_type', 'fuel_type', 'transmission')
    search_fields = ('brand', 'model')
    list_per_page = 20

admin.site.register(Vehicle, VehicleAdmin)

# --- AŞAĞISI YENİ EKLENDİ (SPRINT 2) ---

class ReservationAdmin(admin.ModelAdmin):
    # Listede görünecek sütunlar
    list_display = ('customer', 'vehicle', 'start_date', 'end_date', 'total_price', 'status')
    
    # Sağ taraftaki filtreleme menüsü
    list_filter = ('status', 'start_date', 'end_date')
    
    # Arama çubuğu (Kullanıcı adı veya Araba markasına göre arama)
    search_fields = ('customer__user__username', 'vehicle__brand', 'vehicle__model')
    
    # Listede direkt durum güncellemesi yapabilmek için (Pratiklik sağlar)
    list_editable = ('status',)

admin.site.register(Reservation, ReservationAdmin)