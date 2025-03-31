from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import HomePageContent, Document, ContactInfo, FooterSettings, UserProfile, DietProgram, Meal

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Kullanıcı Profili'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_user_type')
    list_filter = ('home_profile__user_type',)
    
    def get_user_type(self, obj):
        return obj.home_profile.get_user_type_display()
    get_user_type.short_description = 'Kullanıcı Tipi'

class DietProgramAdmin(admin.ModelAdmin):
    list_display = ('client', 'employee', 'start_date', 'end_date', 'target_weight', 'daily_calories')
    list_filter = ('employee', 'start_date', 'end_date')
    search_fields = ('client__user__username', 'client__user__first_name', 'client__user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(employee__user=request.user)

class MealAdmin(admin.ModelAdmin):
    list_display = ('program', 'meal_type', 'time', 'calories')
    list_filter = ('meal_type', 'program__employee')
    search_fields = ('program__client__user__username', 'program__client__user__first_name', 'program__client__user__last_name')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(program__employee__user=request.user)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone', 'birth_date', 'height', 'weight')
    list_filter = ('user_type', 'birth_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.home_profile.user_type == 'employee':
            return qs.filter(user_type='client')
        return qs.filter(user=request.user)

@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    fieldsets = (
        ('Genel Bilgiler', {
            'fields': ('title', 'logo', 'homepage_image', 'banner_image', 'content_text')
        }),
        ('Dokümanlar', {
            'fields': ('documents',),
            'classes': ('collapse',)
        }),
    )
    filter_horizontal = ('documents',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date')
    search_fields = ('title', 'description')

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'whatsapp')

@admin.register(FooterSettings)
class FooterSettingsAdmin(admin.ModelAdmin):
    list_display = ('facebook_url', 'instagram_url', 'linkedin_url')
    fieldsets = (
        ('Footer Metni', {
            'fields': ('footer_description',),
            'description': 'Footer bölümünde görünecek açıklama metni'
        }),
        ('Sosyal Medya Linkleri', {
            'fields': ('facebook_url', 'instagram_url', 'linkedin_url'),
            'description': 'Sosyal medya hesaplarınızın linkleri. Boş bırakılan linkler footer\'da görünmeyecektir.'
        }),
    )
    
    def has_add_permission(self, request):
        # Sadece bir tane footer ayarı olabilir
        return not FooterSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'user_type')
    list_filter = ('user_type',)

@admin.register(DietProgram)
class DietProgramAdmin(admin.ModelAdmin):
    list_display = ('client', 'employee', 'start_date', 'end_date')
    list_filter = ('employee', 'start_date', 'end_date')

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('program', 'meal_type', 'time', 'calories')
    list_filter = ('program', 'time')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

