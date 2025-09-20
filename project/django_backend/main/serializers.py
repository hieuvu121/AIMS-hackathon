# Commented out serializers to prevent API-related errors and simplify the project
# from rest_framework import serializers
# from .models import NewsletterSubscriber, PageContent, CaseStudy, Method, AboutSection

# class NewsletterSubscriberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NewsletterSubscriber
#         fields = ['email', 'subscribed_at']
#         read_only_fields = ['subscribed_at']

# class PageContentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PageContent
#         fields = ['page', 'title', 'subtitle', 'content', 'updated_at']
#         read_only_fields = ['updated_at']

# class CaseStudySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CaseStudy
#         fields = ['id', 'title', 'icon', 'description', 'details', 'order', 'is_active', 'created_at']
#         read_only_fields = ['created_at']

# class MethodSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Method
#         fields = ['id', 'title', 'icon', 'description', 'details', 'order', 'is_active', 'created_at']
#         read_only_fields = ['created_at']

# class AboutSectionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AboutSection
#         fields = ['id', 'title', 'icon', 'description', 'details', 'order', 'is_active', 'created_at']
#         read_only_fields = ['created_at']

