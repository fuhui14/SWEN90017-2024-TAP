# transcription/forms.py

from django import forms

class UploadFileForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'})
    )
    # Do not specify 'multiple' here; the frontend <input multiple> already handles multi-file upload
    file = forms.FileField(label='File')  

    outputFormat = forms.ChoiceField(
        choices=[
            ('docx', 'docx'),
            ('pdf',  'pdf'),
            ('txt',  'txt'),
        ],
        initial='txt',
        label='Output Format'
    )
    language = forms.ChoiceField(
        choices=[
            ('english', 'English'),
            ('spanish', 'Spanish'),
            ('french',  'French'),
        ],
        initial='english',
        label='Language'
    )
