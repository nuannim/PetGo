from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import json
import os
import uuid

# Use the Image model to persist metadata
from .models import Image
from django.core.files.base import ContentFile



@api_view(['GET'])
def download_image_by_filename(request, filename):
    """API endpoint for downloading an image by path (/images/filename.ext)"""
    # ตัด /images/ ออก ถ้ามี
    if filename.startswith('images/'):
        filename = filename[len('images/'):]
    elif filename.startswith('/images/'):
        filename = filename[len('/images/'):]
    file_path = os.path.join(settings.MEDIA_ROOT, 'images', filename)
    if not os.path.exists(file_path):
        return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

@api_view(['POST'])
def upload_image(request):
    """API endpoint for uploading images (no database)"""
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']

    # --- previous behavior: save file directly to media dir (commented out) ---
    # images_dir = os.path.join(settings.MEDIA_ROOT, 'images')
    # os.makedirs(images_dir, exist_ok=True)
    # file_path = os.path.join(images_dir, file.name)
    # with open(file_path, 'wb+') as destination:
    #     for chunk in file.chunks():
    #         destination.write(chunk)
    # return Response({
    #     'filename': file.name,
    #     'url': request.build_absolute_uri(f'/media/images/{file.name}')
    # }, status=status.HTTP_201_CREATED)

    # New behavior: persist metadata in the Image model and use Image.file.save
    try:
        img = Image(
            title=request.data.get('title', ''),
            original_filename=file.name,
            content_type=getattr(file, 'content_type', ''),
            size=getattr(file, 'size', 0)
        )
        # Save file content to the Image.file field (upload_to will generate a unique filename)
        img.file.save(file.name, ContentFile(file.read()), save=False)
        img.save()

        return Response({
            'id': str(img.id),
            'filename': img.file.name,
            'url': request.build_absolute_uri(img.file.url),
            'original_filename': img.original_filename,
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_image(request, filename):
    """API endpoint for retrieving image information (no database)"""
    # New behavior: try to treat filename as UUID id and lookup Image metadata
    try:
        # If it's a valid UUID, lookup by id
        uuid_obj = uuid.UUID(filename)
        img = get_object_or_404(Image, pk=uuid_obj)
        return Response({
            'id': str(img.id),
            'filename': img.file.name,
            'size': img.size,
            'url': request.build_absolute_uri(img.file.url),
            'original_filename': img.original_filename,
            'uploaded_at': img.uploaded_at,
        })
    except Exception:
        # --- previous filesystem-based logic (commented out) ---
        # if filename.startswith('images/'):
        #     filename = filename[len('images/') :]
        # elif filename.startswith('/images/'):
        #     filename = filename[len('/images/') :]
        # file_path = os.path.join(settings.MEDIA_ROOT, 'images', filename)
        # if not os.path.exists(file_path):
        #     return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        # size = os.path.getsize(file_path)
        # return Response({
        #     'filename': filename,
        #     'size': size,
        #     'url': request.build_absolute_uri(f'/media/images/{filename}')
        # })
        return Response({'error': 'Invalid id or image not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def download_image(request, filename):
    """API endpoint for downloading an image (no database)"""
    # New behavior: if filename is UUID, download via Image.file.path
    try:
        uuid_obj = uuid.UUID(filename)
        img = get_object_or_404(Image, pk=uuid_obj)
        file_path = img.file.path
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{img.original_filename}"'
            return response
    except Exception:
        # --- previous filesystem-based logic (commented out) ---
        # if filename.startswith('images/'):
        #     filename = filename[len('images/'):]
        # elif filename.startswith('/images/'):
        #     filename = filename[len('/images/'):]
        # file_path = os.path.join(settings.MEDIA_ROOT, 'images', filename)
        # if not os.path.exists(file_path):
        #     return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        # with open(file_path, 'rb') as f:
        #     response = HttpResponse(f.read(), content_type='application/octet-stream')
        #     response['Content-Disposition'] = f'attachment; filename="{filename}"'
        #     return response
        return Response({'error': 'Invalid id or image not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_image(request, filename):
    """API endpoint for deleting an image (no database)"""
    # New behavior: delete by Image id
    try:
        uuid_obj = uuid.UUID(filename)
        img = get_object_or_404(Image, pk=uuid_obj)
        # delete the file and the DB record
        img.file.delete(save=False)
        img.delete()
        return Response({'message': 'Image deleted successfully'}, status=status.HTTP_200_OK)
    except Exception:
        # --- previous filesystem-based logic (commented out) ---
        # if filename.startswith('images/'):
        #     filename = filename[len('images/') :]
        # elif filename.startswith('/images/'):
        #     filename = filename[len('/images/') :]
        # file_path = os.path.join(settings.MEDIA_ROOT, 'images', filename)
        # if not os.path.exists(file_path):
        #     return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        # os.remove(file_path)
        # return Response({'message': 'Image deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid id or image not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_images(request):
    """API endpoint for listing all images in media/images/ (no database)"""
    # New behavior: list Image DB records
    images = Image.objects.all().order_by('-uploaded_at')
    data = []
    for img in images:
        data.append({
            'id': str(img.id),
            'filename': img.file.name,
            'url': request.build_absolute_uri(img.file.url),
            'original_filename': img.original_filename,
            'size': img.size,
            'uploaded_at': img.uploaded_at,
        })
    return Response(data)
