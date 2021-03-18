from django import forms
from common.models import Announcement

class editforms2(forms.ModelForm):
    class Meta:
        model=Announcement
        fields= [
            'title',
            'description',
            'account_id',
            ]

            