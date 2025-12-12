from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


# تابع اعتبارسنجی کد ملی
def validate_national_code(value):
    if len(value) != 10 or not value.isdigit():
        raise ValidationError('کد ملی باید ۱۰ رقم باشد')


# Regex دقیق برای تاریخ تولد
birthday_regex = RegexValidator(
    r'^(13[0-9]{2})/(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])$',
    'تاریخ تولد باید با فرمت YYYY/MM/DD باشد و ماه و روز معتبر باشند'
)


class GeneratorForm(forms.Form):
    first_name = forms.CharField(
        label='نام',
        min_length=3,
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'علی', 'class': 'form-control'}),
        error_messages={'required': 'نام خود را به درستی وارد کنید.'}
    )

    last_name = forms.CharField(
        label='نام خانوادگی',
        min_length=3,
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'نادری', 'class': 'form-control'}),
        error_messages={'required': 'نام خانوادگی خود را به درستی وارد کنید.'}
    )

    national_code = forms.CharField(
        label='کد ملی',
        min_length=10,
        max_length=10,
        validators=[validate_national_code],
        widget=forms.TextInput(attrs={'placeholder': '0012345678', 'class': 'form-control', 'inputmode': 'numeric'}),
        error_messages={'required': 'کد ملی خود را به درستی وارد کنید'}
    )

    birthday = forms.CharField(
        label='تاریخ تولد',
        min_length=10,
        max_length=10,
        validators=[birthday_regex],
        widget=forms.TextInput(
            attrs={'placeholder': '1381/05/12', 'class': 'form-control', 'pattern': r'\d{4}/\d{2}/\d{2}'}),
        error_messages={'required': 'تاریخ تولد خود را به درستی وارد کنید'}
    )

    father_name = forms.CharField(
        label='نام پدر',
        min_length=3,
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'محمد', 'class': 'form-control'}),
        error_messages={'required': 'نام پدر خود را به درستی وارد کنید'}
    )

    # فیلد عکس
    image = forms.ImageField(
        label='عکس پرسنلی',
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'لطفا یک عکس انتخاب کنید'}
    )
