from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import sys

from django.forms import TextInput, Textarea, NumberInput, EmailInput, DateInput, CheckboxInput, NullBooleanSelect, \
    SelectDateWidget, FileInput, ClearableFileInput, SelectMultiple

import accounting
from accounting.models import Profile, field_types, DynamicField




class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_type in field_types:
            specific_fileds = (getattr(accounting.models, field_type)).objects.filter(profile=self.instance)
            for specific_filed in specific_fileds:
                rebuild_class = getattr(forms, field_type.replace('Desired', ''))
                field_name = str(specific_filed.field_name).replace("DynamicField object", '').replace('(', '').replace(
                    ")", '').strip()
                self.fields[field_name] = rebuild_class(required=True)
                self.initial[field_name] = specific_filed.field

    def get_dynamic_fields(self):
        for field_name in self.fields:
            yield self[field_name]

    def save(self, commit=True):
        super().save()
        print(self.changed_data)
        for key in self.changed_data:
            dynamic_field = DynamicField.objects.filter(field_name=key).first()
            if dynamic_field:
                field_type = dynamic_field.field_type
                (getattr(accounting.models, field_type)).objects.filter(profile=self.instance, field_name=key).update(
                    field=self.cleaned_data[key])

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user',)
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control'
            }),
            'email': EmailInput(attrs={
                'class': 'form-control'
            }),
            'phone': TextInput(attrs={
                'class': 'form-control'
            }),
            'national': TextInput(attrs={
                'class': 'form-control'
            }),
            'gender': TextInput(attrs={
                'class': 'form-control'
            }),
            'address': Textarea(attrs={
                'class': 'form-control'
            }),
            'bio': Textarea(attrs={
                'class': 'form-control'
            }),
            'height': NumberInput(attrs={
                'class': 'form-control'
            }),
            'weight': NumberInput(attrs={
                'class': 'form-control'
            }),
            'born': SelectDateWidget(attrs={
                'class': 'form-control'
            }),
            'phone_verified': NullBooleanSelect(attrs={
                'class': 'form-control'
            }),
            'image': FileInput(attrs={
                'class': 'form-control'
            }),
            'using_sites': SelectMultiple(attrs={
                'class': 'form-control'
            }),


        }


class EnteranceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        fields_name = kwargs.pop('fields_name', None)
        fields_type = kwargs.pop('fields_type', None)
        # fields_template = kwargs.pop('fields_template', None)
        super().__init__(*args, **kwargs)
        if fields_name:
            for i in range(len(fields_name)):
                name = fields_name[i]
                type = fields_type[i]
                # template=fields_template[i]
                rebuild_class = getattr(forms, type)
                self.fields[name] = rebuild_class(required=True)
                # self.initial[field_name] = specific_filed.field
