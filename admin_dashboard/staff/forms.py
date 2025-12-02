from django import forms
from .models import Leadership


class LeadershipForm(forms.ModelForm):
    class Meta:
        model = Leadership
        fields = ['full_name', 'position', 'photo', 'biography', 'email', 'phone']
