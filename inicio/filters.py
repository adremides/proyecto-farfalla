from cabina.models import Cliente, Sesion, Firma
from django_filters import DateFilter, FilterSet
from bootstrap_datepicker_plus import DatePickerInput

class SesionFilter(FilterSet):

    fecha = DateFilter(
        widget=DatePickerInput(format='%d/%m/%Y')
    )

    class Meta:
        model = Sesion
        fields = ['fecha', ]

class ClienteSesionFilter(FilterSet):
    class Meta:
        model = Sesion
        fields = ['cliente', ]