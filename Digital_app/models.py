from django.db import models

class EncryptedDocument(models.Model):
    user_email = models.EmailField(max_length=254)
    file_name = models.CharField(max_length=255)
    encrypted_data = models.BinaryField()
    timestamp = models.DateTimeField(auto_now_add=True)
    clearance_required = models.CharField(max_length=50, default='Standard')


    def __str__(self):
        return f"Username: {self.user_email} File:{self.file_name}"