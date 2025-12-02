import os
import sys
import django

sys.path.insert(0, r'c:\Users\moham\Downloads\ETUSL\admin_dashboard')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.contrib.auth.models import User

try:
    User.objects.create_superuser(
        username='ETUSLWEB001',
        email='mohamedsallu.sl@gmail.com',
        password='P@$$W0RD'
    )
    print("Superuser created successfully!")
except Exception as e:
    print(f"Error: {e}")
