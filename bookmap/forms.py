from django import forms
from .models import Review, Tag

class ReviewForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':' 후기를 입력해주세요.'}), label='')
    class Meta:
        model = Review
        fields = ['content']

class AddThemaForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title', 'description', 'img', 'private']