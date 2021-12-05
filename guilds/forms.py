from django import forms
from .models import GuildArticle


class GuildArticleForm(forms.ModelForm):

    class Meta:
        model = GuildArticle
        fields = '__all__'
        # exclude = ('title',)





