from django.contrib import admin
# from .models import NewsletterSubscriber, PageContent, CaseStudy, Method, AboutSection

# Commented out admin registrations to prevent API-related errors
# @admin.register(NewsletterSubscriber)
# class NewsletterSubscriberAdmin(admin.ModelAdmin):
#     list_display = ['email', 'subscribed_at', 'is_active']
#     list_filter = ['is_active', 'subscribed_at']
#     search_fields = ['email']
#     readonly_fields = ['subscribed_at']

# @admin.register(PageContent)
# class PageContentAdmin(admin.ModelAdmin):
#     list_display = ['page', 'title', 'updated_at']
#     list_filter = ['page', 'updated_at']

# @admin.register(CaseStudy)
# class CaseStudyAdmin(admin.ModelAdmin):
#     list_display = ['title', 'order', 'is_active', 'created_at']
#     list_filter = ['is_active', 'created_at']
#     ordering = ['order', 'created_at']

# @admin.register(Method)
# class MethodAdmin(admin.ModelAdmin):
#     list_display = ['title', 'order', 'is_active', 'created_at']
#     list_filter = ['is_active', 'created_at']
#     ordering = ['order', 'created_at']

# @admin.register(AboutSection)
# class AboutSectionAdmin(admin.ModelAdmin):
#     list_display = ['title', 'order', 'is_active', 'created_at']
#     list_filter = ['is_active', 'created_at']
#     ordering = ['order', 'created_at']