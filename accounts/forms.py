from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email'})
    )



# User Profile form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'location', 'bio', 'phone_no']
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Write about yourself...', 'rows': 4}),
        }

# To remove the name of the image uploaded
def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This will prevent showing the current file name
        self.fields['profile_picture'].initial = None


