from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше ім\'я (залиште порожнім, якщо ви авторизовані)'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш коментар',
                'rows': 4
            })
        }
        labels = {
            'author': 'Ім\'я (тільки для анонімних користувачів)',
            'text': 'Коментар'
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Якщо користувач авторизований, поле author не обов'язкове
        if self.user and self.user.is_authenticated:
            self.fields['author'].required = False
            self.fields['author'].widget.attrs['placeholder'] = 'Залиште порожнім, буде використано ваше ім\'я користувача'

