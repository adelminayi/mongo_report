from django import forms


class DateForm(forms.Form):
    from_date = forms.DateTimeField(widget=forms.TextInput(
        attrs={'type': 'date'}), label='از تاریخ')
    from_hour = forms.DateTimeField(widget=forms.TextInput(
        attrs={'type': 'time'}), input_formats=['%H:%M'], label='از ساعت')
    to_date = forms.DateField(widget=forms.TextInput(
        attrs={'type': 'date'}),  label='تا تاریخ')
    to_hour = forms.DateTimeField(widget=forms.TextInput(
        attrs={'type': 'time'}), input_formats=['%H:%M'], label='تا ساعت')
