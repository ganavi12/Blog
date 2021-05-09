from django import forms

class CommentForm(forms.Form):
    forms.CharField(max_length=100,label="Your Comment") 