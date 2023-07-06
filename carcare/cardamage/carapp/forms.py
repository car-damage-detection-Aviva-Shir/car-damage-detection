from django import forms

class ImageForm(forms.Form):
        imagefile = forms.ImageField( widget=forms.ClearableFileInput(attrs={'accept': 'image/*','class':'custom-file-input','value': 'Select Image'}))
