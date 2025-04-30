from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
    email = forms.EmailField()
    outputFormat = forms.ChoiceField(
        choices=[
            ("txt", "TXT"),
            ("docx", "DOCX"),
            ("pdf", "PDF"),
        ],
        required=False,  # If users don't choose, backend use txt as default.
        initial="txt"
    )
