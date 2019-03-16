from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.db import IntegrityError

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from .serializers import ProfileSerializer, ProfileFileSerializer, ProfileWriteSerializer
from .models import Profile

class ProfileViewSet(viewsets.ViewSet):
    
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def list(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, context={"request": request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        profile = self.get_object(pk)
        serializer = ProfileWriteSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['put'], url_path='image')
    def upload_image(self, request, pk=None):
        profile = self.get_object(pk)
        serializer = ProfileFileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

