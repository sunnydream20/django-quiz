from django.contrib import admin
from .models import Package, Module, Quiz, Question, UserQuiz, UserPackage
from django.utils.html import format_html

# Custom admin for UserPackage
class UserPackageAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'purchase_date', 'display_purchase_image')
    list_filter = ('user', 'package', 'purchase_date')  # Allows filtering by these fields
    search_fields = ('user__username', 'package__name')  # Enables search by user and package name

    def display_purchase_image(self, obj):
        if obj.purchase_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.purchase_image.url)
        return "No Image"
    display_purchase_image.short_description = 'Purchase Image'

# Register other models
admin.site.register(Package)
admin.site.register(Module)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(UserQuiz)

# Register UserPackage with the custom admin interface
admin.site.register(UserPackage, UserPackageAdmin)
