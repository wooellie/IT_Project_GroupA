# properties/forms.py
from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        # 允许中介填写的字段
        fields = ['title', 'description', 'price', 'zip_code', 'image']
        
        # 为表单添加 Bootstrap 样式，适配 iPhone UI
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the property'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weekly price in £'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. G12 8QQ'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        