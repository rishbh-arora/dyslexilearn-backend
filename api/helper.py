from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def validate_image_url(logo_url):
    url_validator = URLValidator()
    try:
        url_validator(logo_url)
    except ValidationError:
        raise ValidationError({"logo_url": "Invalid URL format."})

    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

    if not any(logo_url.lower().endswith(ext) for ext in allowed_extensions):
        raise ValidationError({"logo_url": "Logo URL must be an image link (jpg, jpeg, png, gif, webp)."})
    
def validate_csv_row(row):
    required_fields = ['question', 'max_marks']
    for field in required_fields:
        if not row.get(field):
            raise ValidationError(f"Missing required field: {field}")
    
    try:
        if row.get('duration'):
            float(row['duration'])
        float(row['max_marks'])
    except ValueError:
        raise ValidationError("Duration and max_marks must be numeric values")