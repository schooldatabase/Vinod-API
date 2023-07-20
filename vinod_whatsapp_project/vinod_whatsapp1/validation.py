from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_call_status(value):
    valid_statuses = ['incoming', 'outgoing', 'answered', 'ended']
    if value not in valid_statuses:
        raise ValidationError("Invalid call status. Valid call statuses: incoming, outgoing, answered, ended.")

def validate_call_encryption(value):
    # Custom validation for call encryption (you can implement your encryption logic here)
    if not value:
        raise ValidationError("Call encryption cannot be empty.")

# Add other validation for other models (e.g., Photo, Video, Audio, Document, etc.).
def validate_file_extension(valid_extensions):
    def validator(value):
        file_extension = value.name.lower().split('.')[-1]
        if file_extension not in valid_extensions:
            raise ValidationError(f"Invalid file extension. Supported extensions are: {', '.join(valid_extensions)}")
    return validator

def validate_file_size(max_size):
    def validator(value):
        # Set the maximum allowed size for the file (in bytes)
        if value.size > max_size:
            raise ValidationError(f"File size should be less than {max_size} bytes.")
    return validator

def validate_image(value):
    validate_file_extension(['.jpg', '.jpeg', '.png'])(value)
    validate_file_size(10 * 1024 * 1024)(value)  # 10 MB

def validate_video(value):
    validate_file_extension(['.mp4', '.mov'])(value)
    validate_file_size(100 * 1024 * 1024)(value)  # 100 MB

def validate_audio(value):
    validate_file_extension(['.mp3'])(value)
    validate_file_size(20 * 1024 * 1024)(value)  # 20 MB

def validate_document(value):
    validate_file_extension(['.pdf', '.txt'])(value)
    validate_file_size(5 * 1024 * 1024)(value)  # 5 MB
    
    
# user validation some code
def validate_language(value):
    supported_languages = ['en', 'fr', 'es']
    if value not in supported_languages:
        raise ValidationError("Invalid language. Please select a supported language.")

def validate_app_theme(value):
    if value not in ['light', 'dark']:
        raise ValidationError("Invalid app theme. Please select 'light' or 'dark'.")

def validate_privacy_enabled(value):
    if not isinstance(value, bool):
        raise ValidationError("Invalid value for privacy_enabled. It should be a boolean.")

def validate_sender_and_receiver(sender_id, receiver_id):
    try:
        sender = User.objects.get(pk=sender_id)
        receiver = User.objects.get(pk=receiver_id)
    except User.DoesNotExist:
        raise ValidationError("Invalid sender or receiver ID. Please provide valid user IDs.")

def validate_message_content_length(value):
    max_length = 1000
    if len(value) > max_length:
        raise ValidationError(f"Message content should not exceed {max_length} characters.")