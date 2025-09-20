from django.db import models
from django.utils import timezone

# Commented out models to prevent API-related errors and simplify the project
# class NewsletterSubscriber(models.Model):
#     email = models.EmailField(unique=True)
#     subscribed_at = models.DateTimeField(default=timezone.now)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.email

#     class Meta:
#         ordering = ['-subscribed_at']

# class PageContent(models.Model):
#     PAGE_CHOICES = [
#         ('home', 'Home'),
#         ('case_study', 'Case Study'),
#         ('methods', 'Methods'),
#         ('about_us', 'About Us'),
#     ]
    
#     page = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
#     title = models.CharField(max_length=200)
#     subtitle = models.TextField(blank=True)
#     content = models.JSONField(default=dict, blank=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.get_page_display()} - {self.title}"

# class CaseStudy(models.Model):
#     title = models.CharField(max_length=200)
#     icon = models.CharField(max_length=10, default='📊')
#     description = models.TextField()
#     details = models.TextField()
#     order = models.PositiveIntegerField(default=0)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title

#     class Meta:
#         ordering = ['order', 'created_at']

# class Method(models.Model):
#     title = models.CharField(max_length=200)
#     icon = models.CharField(max_length=10, default='📋')
#     description = models.TextField()
#     details = models.TextField()
#     order = models.PositiveIntegerField(default=0)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title

#     class Meta:
#         ordering = ['order', 'created_at']

# class AboutSection(models.Model):
#     title = models.CharField(max_length=200)
#     icon = models.CharField(max_length=10, default='🎯')
#     description = models.TextField()
#     details = models.TextField()
#     order = models.PositiveIntegerField(default=0)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title

#     class Meta:
#         ordering = ['order', 'created_at']