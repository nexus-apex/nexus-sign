from django.contrib import admin
from .models import Document, SignRequest, Template

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "sender", "status", "signers", "sent_date", "created_at"]
    list_filter = ["status"]
    search_fields = ["title", "sender"]

@admin.register(SignRequest)
class SignRequestAdmin(admin.ModelAdmin):
    list_display = ["document_title", "signer_name", "signer_email", "status", "sent_date", "created_at"]
    list_filter = ["status"]
    search_fields = ["document_title", "signer_name", "signer_email"]

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "pages", "fields_count", "usage_count", "created_at"]
    search_fields = ["name", "category"]
