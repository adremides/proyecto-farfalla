from django.db import models
from django.utils import timezone
from jsignature.fields import JSignatureField

class Responsable(models.Model):
    nombre = models.CharField(max_length=75)

    def __str__(self):
        return str(self.nombre)

class Cliente(models.Model):
    fecha_incorporacion = models.DateTimeField('Fecha de incorporación', default=timezone.now)
    nombre_y_apellido = models.CharField(max_length=75)
    telefono = models.CharField('Teléfono',max_length=50, blank=True, null=True)
    consintio = models.BooleanField('Consintió', default=False)

    def __str__(self):
        return str(self.nombre_y_apellido)

class Sesion(models.Model):
    cliente = models.ForeignKey('cabina.Cliente', on_delete=models.PROTECT)
    fecha = models.DateField('Fecha de la sesión', default=timezone.now, null=True, blank=True)
    duracion = models.IntegerField("Duración",
                                choices=(
                                            (5, '5 minutos'),
                                            (10, '10 minutos'),
                                        )
                                )
    responsable = models.ForeignKey('cabina.Responsable',
                                    on_delete=models.PROTECT)
    pagada = models.BooleanField("Pagada", default=False)
    actual = models.IntegerField('Sesión pack', null=True, blank=True)
    pack = models.ForeignKey('cabina.Pack', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        estoy_creando = not self.pk
        super(Sesion, self).save(*args, **kwargs)
        if not estoy_creando:
            print('la diferencia entre self.actual(%s) y self.pack.proxima (%s) es %s' %(self.actual,
                                                                                         self.pack.proxima,
                                                                                         self.actual - self.pack.proxima))
            if self.actual - self.pack.proxima == 0: # Esto detecta si es la próxima sesion disponible
                # Si es, la próxima será la siguiente del pack, a menos de que esta sea la última
                registro_pack = Pack.objects.filter(pk=self.pack.pk).update(proxima=self.actual + 1)


    def es_pack(self):
        if self.pack != None:
            return str(self.actual) + ' de ' + str(self.pack.cant_sesiones)
        else:
            return "No es pack"
    es_pack.short_description = 'Pack'

    def esta_firmada(self):
        firmas = self.firma_set.all() # Siempre va a haber una sola firma por sesión
        if firmas: # Esto comprueba que exista al menos 1 registro
            firmada = bool(firmas[0].firma) # Si el campo firma (string) está vacío esto es False, sino True
        else:
            firmada = False # si no hay un registro de firma, lógicamente no está firmada
        return firmada
    esta_firmada.boolean = True
    esta_firmada.short_description = 'Firmada'

    def __str__(self):
        if self.fecha:
            sesion_display = self.fecha.strftime('%d/%m/%Y') + ' - '
        else:
            sesion_display = 'Sesión sin fecha de '
        sesion_display += self.cliente.nombre_y_apellido + ' (' + self.es_pack() + ')'
        return sesion_display

    class Meta:
        verbose_name = 'Sesión'
        verbose_name_plural = 'Sesiones'

class Firma(models.Model):
    sesion = models.ForeignKey('cabina.Sesion', on_delete=models.CASCADE)
    firma = JSignatureField(blank=True, null=True)

    def __str__(self):
        return ''

class Pack(models.Model):
    cliente = models.ForeignKey('cabina.Cliente', on_delete=models.PROTECT)
    cant_sesiones = models.IntegerField("Cantidad de sesiones",
                                choices=(
                                            (1, '1 sesión'),
                                            (2, '2 sesiones'),
                                            (4, '4 sesiones'),
                                            (10, '10 sesiones'),
                                        )
                                )
    tipo = models.IntegerField("Tipo",
                                choices=(
                                            (5, 'Suave'),
                                            (10, 'Fuerte'),
                                        )
                                )
    pagada = models.BooleanField("Pagada", default=False)
    responsable = models.ForeignKey('cabina.Responsable', on_delete=models.PROTECT)
    proxima = models.PositiveIntegerField('Próxima sesión disponible', default=1)

    def save(self, *args, **kwargs):
        estoy_creando = not self.pk

        super(Pack, self).save(*args, **kwargs)
        if estoy_creando:
            for actual in range(1, self.cant_sesiones+1):
                p = Sesion.objects.create(cliente=self.cliente,
                                          fecha=None,
                                          duracion=self.tipo,
                                          responsable=self.responsable,
                                          pack=self,
                                          pagada=self.pagada,
                                          actual=actual)
                p.save()
        else:
            registros_sesiones = Sesion.objects.filter(pack=self.pk).update(cliente=self.cliente)

    def __str__(self):
        # get_field_display() muestra el str del choice que lleva el campo cant_sesiones del modelo Pack
        return self.get_cant_sesiones_display() + ' de ' + str(self.cliente)