from django.contrib import admin
from .models import CarMake, CarModel
# from .models import related models

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1
# Register your models here.

class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name','description')


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'dealer_id', 'type', 'year')
    list_filter = ('car_make', 'type')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'dealership':
            dealer_ids = fetch_dealer_ids()
            kwargs['queryset'] = dealer_ids
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# CarModelInline class



# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
