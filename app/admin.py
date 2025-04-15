from django.contrib import admin

from app.models import Customer, Crop, Contact

# Register your models here.
admin.site.register(Customer)

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('id', 'userid', 'category', 'condition', 'imgname', 'regday')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('userid', 'username', 'email', 'subject', 'message', 'date')
