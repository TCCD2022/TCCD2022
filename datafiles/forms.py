
from django import forms
from users.models import CustomUser
from datafiles.models import Method

class DataModelForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file: ',
        help_text='max. 42 megabytes'
    )

    exclude = ("userid",)

# class RunMethodForm(forms.ModelForm):

#     class Meta:
#         model = Method
#         fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.fields['language'].queryset = Language.objects.none()

        # if 'language' in self.data:
        #     self.fields['language'].queryset = Method.objects.all()

        # elif self.instance.pk:
        #     self.fields['language'].queryset = Language.objects.all().filter(pk=self.instance.language.pk)
