from django import forms
from .models import IncomingData


# Создание формы для возврата данных с index.html после отправки

class GetDataForm(forms.ModelForm):
    
      class Meta:
        model = IncomingData
        exclude = [""]


# Поле выпадающего списка систем координат

Choices1 =(("1", "CK-42"),("2", "WGS84"))
class DropDownList(forms.Form):
    SK = forms.ChoiceField(choices = Choices1)