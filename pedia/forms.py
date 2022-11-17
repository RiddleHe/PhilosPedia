from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'description']
        labels = {'title': 'Title', 'description': 'Description'}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'description']
        labels = {'title': 'Title', 'description': 'Content'}