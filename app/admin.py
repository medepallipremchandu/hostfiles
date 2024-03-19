# blog/admin.py

from django.contrib import admin
from app.models import File, UploadedPDF, UploadedImage

class FileAdmin(admin.ModelAdmin):
    pass

class UploadedPDFAdmin(admin.ModelAdmin):
    pass

class UploadedImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(File, FileAdmin)
admin.site.register(UploadedImage, UploadedImageAdmin)
admin.site.register(UploadedPDF, UploadedPDFAdmin)