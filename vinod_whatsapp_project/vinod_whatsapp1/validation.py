from django.core.exceptions import ValidationError

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