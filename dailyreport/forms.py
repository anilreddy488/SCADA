from django import forms
from .models import *
from django.forms import formset_factory




class GeneratingStationForm(forms.ModelForm):
    class Meta:
        model = GeneratingStation
        fields = '__all__'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class CustomTimeField(forms.TimeField):
    widget = TimeInput(format='%H:%M')

class GridFreqForm(forms.ModelForm):
    TimeMaxDemandMorning = CustomTimeField()
    TimeMaxDemandEvening = CustomTimeField()
    class Meta:
        model = GridFreq
        fields = '__all__'


class ExcelUploadForm(forms.Form):
    file = forms.FileField(label='Upload Excel File')

class DemandDataForm(forms.ModelForm):
    class Meta:
        model = DemandData
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Date'].widget = forms.DateInput(attrs={'type': 'date'})  # Use HTML5 date input type
        self.fields['Date'].initial = datetime.date.today()  # Set the default value to today's date




class SchDrwlDataForm(forms.ModelForm):
    class Meta:
        model = SchDrwlData
        fields = '__all__'


