from django import forms
from django.utils.safestring import mark_safe
from .models import Documents, Peticionarios, RtasFinales



class MiFormulario(forms.ModelForm):

    class Meta:
        model = Documents
        fields = ['archivo']

class RtasForm(forms.ModelForm):

    class Meta:
        model = RtasFinales
        fields = ['rta']


class PeticionarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PeticionarioForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = mark_safe('<span class="form-label-bold">' + self.fields[field_name].label + '</span>')

    class Meta:
        model= Peticionarios
        fields = ['fecha_llegada','fecha_radicado', 'fecha_entrega','nombre', 'radicado', 'correo','direccion','latitud','longitud','ciudad','localidad','barrio','tipo_dp','tema_dp','asunto','peticion','enviada', 'enviada_aerocivil','enviada_revision','radicado_salida','fecha_salida']
        widgets = {
            'fecha_llegada': forms.DateInput(format=('%Y-%m-%d'),   
                                        attrs={'type':'date', 'class':'form-date-input-center form-date-input-width', 
                                        'placeholder':'aaaa-mm-dd','label':'Fecha de llegada Applus+:'}),

            'fecha_radicado': forms.DateInput(format=('%Y-%m-%d'),  
                                        attrs={'type':'date','class': 'form-date-input-center form-date-input-width', 
                                        'placeholder':'aaaa-mm-dd', 'label':'Fecha del radicado de llegada:'}),

            'fecha_entrega': forms.DateInput(format=('%Y-%m-%d'),  
                                        attrs={'type':'date','class': 'form-date-input-center form-date-input-width', 
                                        'placeholder':'aaaa-mm-dd', 'label':'Fecha de entrega al cliente:'}),

            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del peticionario...'}),

            'radicado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Radicado de llegada...'}),

            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico...'}),

            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección...'}),

            'latitud': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Latitud...'}),

            'longitud': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Longitud...'}),

            'ciudad': forms.Select(attrs={'class': 'form-control'}),

            'localidad': forms.Select(attrs={'class': 'form-control'}),
            
            'barrio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Barrio...'}),

            'tipo_dp': forms.Select(attrs={'class': 'form-control'}),

            'tema_dp': forms.Select(attrs={'class': 'form-control'}),

            'asunto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Asunto...'}),

            'peticion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Petición...'}),

            'enviada': forms.CheckboxInput(attrs={'class': 'form-label-padding'}),

            'enviada_aerocivil': forms.CheckboxInput(attrs={'class': 'form-label-padding'}),

            'enviada_revision': forms.CheckboxInput(attrs={'class': 'form-label-padding'}),

            'radicado_salida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Radicado de salida...'}),

            'fecha_salida': forms.DateInput(format=('%Y-%m-%d'),  
                                        attrs={'type':'date', 'class':'form-date-input-center form-date-input-width', 
                                        'placeholder':'aaaa-mm-dd', 'label':'Fecha del radicado de salida:'}),
            
        }
        
