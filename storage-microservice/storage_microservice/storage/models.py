from django.db import models
import uuid
import os

def image_upload_path(instance, filename):
    """Generate unique path for uploaded images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('images', filename)

class Image(models.Model):
    """Model for storing image metadata"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to=image_upload_path)
    original_filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    size = models.PositiveIntegerField()  # Size in bytes
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.original_filename
