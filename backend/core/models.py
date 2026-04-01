from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    sender = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("draft", "Draft"), ("sent", "Sent"), ("viewed", "Viewed"), ("signed", "Signed"), ("declined", "Declined"), ("expired", "Expired")], default="draft")
    signers = models.IntegerField(default=0)
    sent_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    file_url = models.URLField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class SignRequest(models.Model):
    document_title = models.CharField(max_length=255)
    signer_name = models.CharField(max_length=255, blank=True, default="")
    signer_email = models.EmailField(blank=True, default="")
    status = models.CharField(max_length=50, choices=[("pending", "Pending"), ("signed", "Signed"), ("declined", "Declined")], default="pending")
    sent_date = models.DateField(null=True, blank=True)
    signed_date = models.DateField(null=True, blank=True)
    ip_address = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.document_title

class Template(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, default="")
    pages = models.IntegerField(default=0)
    fields_count = models.IntegerField(default=0)
    usage_count = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
