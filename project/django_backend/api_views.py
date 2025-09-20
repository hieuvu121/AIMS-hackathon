# Commented out API views to prevent API-related errors and simplify the project
# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
# from .models import NewsletterSubscriber, PageContent, CaseStudy, Method, AboutSection
# from .serializers import (
#     NewsletterSubscriberSerializer, 
#     PageContentSerializer, 
#     CaseStudySerializer, 
#     MethodSerializer, 
#     AboutSectionSerializer
# )

# class NewsletterViewSet(viewsets.ModelViewSet):
#     queryset = NewsletterSubscriber.objects.filter(is_active=True)
#     serializer_class = NewsletterSubscriberSerializer

#     @action(detail=False, methods=['post'])
#     def subscribe(self, request):
#         email = request.data.get('email')
#         if not email:
#             return Response(
#                 {'error': 'Email is required'}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         subscriber, created = NewsletterSubscriber.objects.get_or_create(
#             email=email,
#             defaults={'is_active': True}
#         )
        
#         if not created and not subscriber.is_active:
#             subscriber.is_active = True
#             subscriber.save()
        
#         serializer = self.get_serializer(subscriber)
#         return Response(
#             {
#                 'message': 'Successfully subscribed to newsletter!',
#                 'subscriber': serializer.data
#             },
#             status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
#         )

# class PageContentViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = PageContent.objects.all()
#     serializer_class = PageContentSerializer
#     lookup_field = 'page'

# class CaseStudyViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = CaseStudy.objects.filter(is_active=True)
#     serializer_class = CaseStudySerializer

# class MethodViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Method.objects.filter(is_active=True)
#     serializer_class = MethodSerializer

# class AboutSectionViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = AboutSection.objects.filter(is_active=True)
#     serializer_class = AboutSectionSerializer

