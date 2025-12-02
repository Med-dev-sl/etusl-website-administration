import os
import sys
import django
from pathlib import Path

# Add the admin_dashboard directory to the path
admin_dashboard_path = Path(r'c:\Users\moham\Downloads\ETUSL\admin_dashboard')
sys.path.insert(0, str(admin_dashboard_path))

os.chdir(admin_dashboard_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_dashboard.settings')

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
