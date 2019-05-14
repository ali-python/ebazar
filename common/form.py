from django import forms
from common.models import UserProfile, Feedback

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

class FeedBackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'
