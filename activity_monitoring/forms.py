"""
forms.py

Django forms for activity monitoring
"""

from django import forms

from activity_monitoring.models import AllowedDomain


class AllowedDomainForm(forms.ModelForm):
    """
    AllowedDomainForm
    """

    class Meta:
        model = AllowedDomain
        fields = ["company_id", "domain_name", "is_active"]
        widgets = {
            "company_id": forms.Select(attrs={"class": "oh-select oh-select-2"}),
            "domain_name": forms.TextInput(attrs={"class": "oh-input"}),
            "is_active": forms.CheckboxInput(attrs={"class": "oh-switch__checkbox"}),
        }

