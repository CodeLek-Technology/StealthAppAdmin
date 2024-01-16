from django import forms
from django.contrib.auth import get_user_model
from django.forms.widgets import PasswordInput, NumberInput, FileInput


User = get_user_model()

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        try:
            self.fields['phone_no'].label = "Phone Number"
            self.fields['password'].label = "Create Password"
        except:  # noqa: E722
            pass
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'

class AddUserForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['first_name','last_name','username','password', 'phone_no', 'profile_picture']
        model = User
        widgets = {
            'password': PasswordInput(attrs={'type': 'password'}),
            'username': NumberInput(attrs={'type': 'text'}),
            'profile_picture': FileInput(attrs={'type': 'file'}),
            # 'closing_date': DateInput(attrs={'type': 'date'}),
        }