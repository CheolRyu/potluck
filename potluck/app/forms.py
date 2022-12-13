from django import forms
from .models import Event, Profile, Guest, Item

SELECT_CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No'),
]
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",  "placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control",  "placeholder": "Password"}))


class SignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",  "placeholder": "Username"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control",  "placeholder": "Email"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",  "placeholder": "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",  "placeholder": "Last Name"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control",  "placeholder": "Password"}))


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['owner', 'name', 'start', 'time', 'address', 'description', 'city', 'state', 'zip_code', 'apt']
        widgets = {
            'start': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'time': forms.TimeInput(format=('%H:%M'), attrs={'class':'form-control', 'placeholder':'Select a time', 'type':'time'}),
            'name': forms.TextInput(attrs={'placeholder': 'Event Name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Street', 'class': 'form-control'}),
            'apt': forms.TextInput(attrs={'placeholder': 'Apt', 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
            'state': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code', 'class': 'form-control'}),

        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'quantity', 'price', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Item Name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Quantity', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}, choices=SELECT_CHOICES),
        }
class ItemUpdate(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}, choices=SELECT_CHOICES),
        }


class FriendForm(forms.Form):
    CHOICES = Profile.objects
    new_friend_email = forms.EmailField(label='friend\'s email')
