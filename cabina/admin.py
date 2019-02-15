import sys
from django import forms
from django.contrib import admin, messages
from django.db.models import Q, Sum, Avg, Min, F, ExpressionWrapper, BooleanField
import nested_admin
from .models import Cliente, Sesion, Firma, Responsable, Pack

from django.forms.models import BaseInlineFormSet

class PackAdmin(admin.ModelAdmin):
    autocomplete_fields = ('cliente',)
    fields = ['cliente',
              'cant_sesiones',
              'tipo',
              'responsable',
              'pagada',
              'proxima',
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + (# 'cliente',
                                           'cant_sesiones',
                                           'tipo',
                                           'responsable',
                                           'pagada')
        return self.readonly_fields

class SesionProximaFilter(admin.SimpleListFilter):
    title = 'próxima sesión de pack'

    parameter_name = 'proxima'

    def lookups(self, request, model_admin):
        return (
            ('si', 'Próxima'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'si':
            qs_preparado = queryset.annotate(es_proxima=ExpressionWrapper(F('actual')-F('pack__proxima'),
                                                                          output_field=BooleanField()))
            return qs_preparado.filter(es_proxima=True)

class SesionEsPackFilter(admin.SimpleListFilter):
    title = 'si es pack o no'

    parameter_name = 'es_pack'

    def lookups(self, request, model_admin):
        return (
            ('si', 'Es pack'),
            ('no', 'No es pack'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'si':
            return queryset.exclude(pack=None)
        if self.value() == 'no':
            return queryset.filter(pack=None)

class FirmadaListFilter(admin.SimpleListFilter):
    title = 'sesión firmada'

    parameter_name = 'firmada'

    def lookups(self, request, model_admin):
        return (
            ('si', 'Con firma'),
            ('no', 'Sin firma'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'si':
            return queryset.exclude(firma__firma__exact='') # acá un firma__firma__is_null=True no funciona
        if self.value() == 'no':
            return queryset.filter(firma__firma__exact='') # acá un firma__firma__is_null=True no funciona

# Esto fue creado basandome en el ejemplo de DecadeBornListFilter
# en https://docs.djangoproject.com/en/2.1/ref/contrib/admin/
class ClienteSesionFormSet(BaseInlineFormSet):
    def get_queryset(self):
     qs = super(ClienteSesionFormSet, self).get_queryset()
     # qs.filter(prueba=False) # ¿Cómo hago para que aparezcan sólo las que no están firmadas?
     return qs[:10]

#class ResponsableAdmin(nested_admin.NestedModelAdmin):
#    model = Responsable

class FirmaInline(nested_admin.NestedStackedInline):
    model = Firma
    verbose_name_plural = 'Firma'
    extra = 1
    max_num = 1
    fk_name = 'sesion'
    classes = ['collapse']

# Esto se usaba cuando se cargaban las sesiones dentro del cliente, ahora las sesiones se cargan por separado
# class SesionInline(nested_admin.NestedTabularInline):
#     model = Sesion
#     # fields = ('fecha', 'duracion', 'responsable', 'esta_firmada') # Con esto y
#     # readonly_fields = ('esta_firmada',) # esto hago que aparezca pero no lo puedo usar como field
#
#     fields = ('fecha', 'duracion', 'responsable', ) # Con esto y
#
#     verbose_name = 'Sesión'
#     verbose_name_plural = 'Sesiones'
#     extra = 0
#     fk_name = 'cliente'
#     inlines = [FirmaInline]
#     # ordering = ("-id",)
#     formset = ClienteSesionFormSet
#     # show_change_link = False

class SesionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SesionForm, self).__init__(*args, **kwargs)
        if self.instance.pk is not None:
            self.fields['fecha'].required = True

    class Meta:
        model = Sesion
        fields = ('cliente',
              'fecha',
              'duracion',
              'responsable',
              'pagada',)

class SesionAdmin(nested_admin.NestedModelAdmin):
    form = SesionForm
    model = Sesion
    fields = ['cliente',
              'fecha',
              'duracion',
              'responsable',
              'pagada',
    ]

    autocomplete_fields = ('cliente', )

    inlines = [FirmaInline]
    list_display = ('cliente', 'fecha', 'duracion', 'responsable', 'pagada', 'esta_firmada', 'es_pack' )
    readonly_fields = ('esta_firmada', 'es_pack')
    ordering = ('cliente__nombre_y_apellido',)
    search_fields = ('cliente__nombre_y_apellido', )

    date_hierarchy = 'fecha'

    list_filter = (
        'fecha',
        'pagada',
        (SesionEsPackFilter),
        (FirmadaListFilter),
        (SesionProximaFilter),
    )
    # Esto serviría para que no se muestre un campo diferenciando si es Create o Update,
    # NO sirve para modificar algo del campo (por ejemplo los atributos).
    # def get_fields(self, request, obj=None):
    #     fields = super(SesionAdmin, self).get_fields(request, obj)
    #     if obj is not None: # Acá esto indica si se viene de un Create o un Update
    #         # fields = [f for f in fields if f != 'fecha']
    #         # for f in fields:
    #         #     if f == 'fecha':
    #         #         f.blank = False
    #         pass
    #     return fields

    def save_model(self, request, obj, form, change):
        # messages.add_message(request, messages.INFO, 'PRUEBA MENSAJE EN MODELADMIN')
        super(SesionAdmin, self).save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        # Al editar una Sesión, si tiene un Pack relacionado ADVERTIR
        # También advierte si una sesión con Pack fue seleccionada para eliminar
        selected = request.POST.getlist(admin.helpers.ACTION_CHECKBOX_NAME)
        if obj is not None: # obj guarda el registro, si es None es un Create, sino un Update
            if obj.pack != None: # pack es el ForeignKey, si tiene algo fue creado de un Pack
                if selected:
                    mensaje = '¡ATENCIÓN! Una o más sesiones seleccionadas fueron generadas como parte de un PACK, NO LAS ELIMINE excepto que sea extremadamente necesario.'
                else:
                    mensaje = '¡ATENCIÓN! Esta sesión fue generada como parte de un PACK, NO LA ELIMINE excepto que sea extremadamente necesario.'
                all_warning_messages_content = [msg.message for msg in list(messages.get_messages(request)) if
                                              msg.level_tag == 'warning']
                if mensaje not in all_warning_messages_content:
                    messages.add_message(request, messages.WARNING, mensaje)
                # self.message_user(request, 'Pack contiene un valor')
                return True # Poner esto en False si queremos que no aparezca el botón eliminar
        return super(SesionAdmin, self).has_delete_permission(request, obj)


class ClienteAdmin(nested_admin.NestedModelAdmin):

    readonly_fields = ('fecha_incorporacion',)
    fields = ['fecha_incorporacion',
              'nombre_y_apellido',
              'telefono',
              'consintio',
    ]

    # inlines = [SesionInline]
    list_display = ('nombre_y_apellido', 'telefono', 'consintio')
    ordering = ('nombre_y_apellido',)
    search_fields = ('nombre_y_apellido',)



# Confirguración del sitio
admin.AdminSite.site_header = 'Farfalla'
admin.AdminSite.site_title = 'Farfalla - Centro de estética, peluquería y solarium'

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Responsable)
admin.site.register(Sesion, SesionAdmin)
admin.site.register(Pack, PackAdmin)