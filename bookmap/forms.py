from django import forms
from .models import Review, Thema

class ReviewForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':' 후기를 입력해주세요.'}), label='')
    class Meta:
        model = Review
        fields = ['content']

class AddThemaForm(forms.ModelForm):
    class Meta:
        model = Thema
        fields = ['title', 'description', 'img', 'private']