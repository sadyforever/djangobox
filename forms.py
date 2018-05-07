from django import forms

# class BookForm(forms.Form):
#     title = forms.CharField(label="书名", required=True, max_length=50)
#     pub_date = forms.DateField(label='出版日期', required=True)
from booktest.models import BookInfo


class BookForm(forms.ModelForm):
    class Meta:
        model = BookInfo
        fields = ('btitle', 'bpub_date')