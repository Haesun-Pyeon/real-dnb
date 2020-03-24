from django import forms
from .models import Review, Thema

class ReviewForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'후기를 입력해주세요'}), label='')

    class Meta:
        model = Review
        fields = ['content']

class AddThemaForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'제목을 입력하세요'}), label='')
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'내용을 입력하세요'}), label='')
    img = forms.ImageField(widget=forms.FileInput(attrs={'placeholder': ''}), label='∙ 업로드할 사진 선택', allow_empty_file=True, required=False)
    private = forms.NullBooleanField(widget=forms.CheckboxInput(attrs={'placeholder':''}), label='∙ 비공개 테마로 작성하시겠습니까?', required=False)
    class Meta:
        model = Thema
        fields = ['title', 'description', 'img', 'private']