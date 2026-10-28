from django.shortcuts import render
import datetime
from django.conf import settings
from django.urls import reverse
from django.core.signing import Signer, BadSignature
from django.http import HttpResponse, HttpResponseBadRequest
from .crypto_utils import encrypt_file_pipeline, decrypt_file_pipeline
from .models import EncryptedDocument 

AUTHORIZED_MANAGERS = ['sana_testing@example.com']

def generate_temporary_link(request):
    if request.method == 'GET':
        return render(request, 'upload.html')

    if request.method == 'POST':
        try:
            user_email = request.POST.get('email')
            raw_file = request.FILES.get('files')
            
            if not user_email or user_email not in AUTHORIZED_MANAGERS:
                return render(request, 'upload.html', {
                    "error_message": f"Access Denied: Role assigned to '{user_email}' lacks Manager Clearance."
                })
                
            if not raw_file:
                return render(request, 'upload.html', {
                    "error_message": "No file stream detected."
                })
                
            encrypted_blob = encrypt_file_pipeline(raw_file, settings.SECRET_KEY)
            
            # ✅ FIXED: Now maps perfectly with your actual models.py fields
            doc_record = EncryptedDocument.objects.create(
                user_email=user_email,
                file_name=raw_file.name,
                encrypted_data=encrypted_blob
            )
            
            expiry_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=10)).isoformat()
            signer = Signer()
            token_payload = f"{doc_record.id}--{expiry_time}"
            signed_token = signer.sign(token_payload)
            
            download_path = reverse('api_download_vault_document')
            clean_secure_url = request.build_absolute_uri(f"{download_path}?token={signed_token}")
            
            return render(request, 'upload.html', {
                "secure_download_url": clean_secure_url
            })
            
        except Exception as e:
            return render(request, 'upload.html', {
                "error_message": f"Internal server processing error: {str(e)}"
            })

def api_download_vault_document(request):
    signed_token = request.GET.get('token')
    if not signed_token:
        return HttpResponseBadRequest("Cryptographic lookup token is missing.")
        
    signer = Signer()
    try:
        original_payload = signer.unsign(signed_token)
        doc_id, expiry_time = original_payload.split('--')
        
        if datetime.datetime.utcnow() > datetime.datetime.fromisoformat(expiry_time):
            return HttpResponse("This secure link has expired (10-minute window exceeded).", status=410)
            
        doc_record = EncryptedDocument.objects.get(id=doc_id)
        
        # ✅ FIXED: Using correctly updated models.py fields
        decrypted_binary_data = decrypt_file_pipeline(doc_record.encrypted_data, settings.SECRET_KEY)
        
        response = HttpResponse(decrypted_binary_data, content_type="application/octet-stream")
        response['Content-Disposition'] = f'attachment; filename="{doc_record.file_name}"'
        return response
        
    except (BadSignature, ValueError, EncryptedDocument.DoesNotExist):
        return HttpResponse("Tamper alert: Cryptographic token validation failed.", status=400)