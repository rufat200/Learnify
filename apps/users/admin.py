from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User

admin.site.unregister(Group)
@receiver(post_save, sender=User)
def assign_group_based_on_role(sender, instance, created, **kwargs):
    if created:
        group_name = instance.role.capitalize() + "s"  # 'Students' или 'Teachers'
        group, _ = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group)


@admin.register(User)
class AdminSiteUser(admin.ModelAdmin):
    list_display = ["id", "email", "full_name", "role", "is_staff", "is_active"]
    list_display_links = ["id", "email", "full_name"]
    list_filter = ["is_staff", "is_superuser", "is_active", "role"]
    search_fields = ["full_name", "email"]
    fieldsets = [
        ("User's data", {"fields": ["email", "role", "password", "full_name"]}),
        ("Permissions", {"fields": ["is_staff", "is_superuser", "is_active"]}),
    ]
    readonly_fields = ["date_joined", "last_login", "role"]
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2", "role", "is_staff", "is_active",),
        }),
    )
    
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'user_count']

    def user_count(self, obj):
        return obj.user_set.count()
    user_count.short_description = 'Users'
