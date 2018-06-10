from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms
from django.core.validators import RegexValidator

class CustomUserCreationForm(UserCreationForm):
        email=forms.EmailField(label='電郵',widget=forms.EmailInput(attrs={'v-model':'username'}),required=True)
        password1=forms.CharField(label='Password',widget=forms.PasswordInput,required=True)
        password2=forms.CharField(label='Password Confirm',widget=forms.PasswordInput,required=True)

        class Meta:
            model = CustomUser
            fields  = ("email",)
        def clean_password2(self):
            print('go in')
            password1=self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
            if not password2:
                raise forms.ValidationError("You must confirm your password")
            if password1 != password2:
                raise forms.ValidationError("Your passwords do not match")
            return password2
        def save(self, commit=True):
            user=super(UserCreationForm,self).save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            print(commit)
            if commit:
                user.save()
            return user
class CustomUserChangeForm(UserChangeForm):
    def __inint__(self,*args,**kargs):
        super(CustomUserChangeForm,self).__init__(*args,**kargs)

    class Meta:
        model = CustomUser
        fields = ("email", "password")
class LoginForm(forms.Form):
    username = forms.CharField(label='電郵/電話',widget=forms.TextInput(attrs={'v-model':'username'}),required=True)
    password = forms.CharField(label='密碼',widget=forms.PasswordInput(attrs={'v-model':'password'}),required=True)
