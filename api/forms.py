from django import forms
from .models import item, hoyRX

class GenerarPedidosForm(forms.ModelForm):
    class Meta:
        model = item
        fields = '__all__'


class registroUsuarioForm(forms.ModelForm):
    class Meta:
        model = hoyRX
        fields = '__all__'