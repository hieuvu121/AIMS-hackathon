# Commented out API URLs to prevent API-related errors and simplify the project
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .api_views import (
#     NewsletterViewSet, 
#     PageContentViewSet, 
#     CaseStudyViewSet, 
#     MethodViewSet, 
#     AboutSectionViewSet
# )

# router = DefaultRouter()
# router.register(r'newsletter', NewsletterViewSet, basename='newsletter')
# router.register(r'pages', PageContentViewSet, basename='pages')
# router.register(r'case-studies', CaseStudyViewSet, basename='case-studies')
# router.register(r'methods', MethodViewSet, basename='methods')
# router.register(r'about-sections', AboutSectionViewSet, basename='about-sections')

# urlpatterns = [
#     path('api/', include(router.urls)),
# ]

# Empty urlpatterns to prevent import errors
urlpatterns = []

