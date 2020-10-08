from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

class Profile(models.Model):
    # Relacion con el modelo User de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Atributos adicionales para el usuario
    documento_identidad = models.CharField(max_length=8)
    fecha_nacimiento = models.DateField()
    estado = models.CharField(max_length=3)
    ## Opciones de genero
    MASCULINO = 'MA'
    FEMENINO = 'FE'
    NO_BINARIO = 'NB'
    GENERO_CHOICES = [
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino'),
        (NO_BINARIO, 'No Binario')
    ]
    genero = models.CharField(max_length=2, choices=GENERO_CHOICES)

    #Para que aparezcan los nombres/etiquetas
    def __str__(self):
        return self.user.get_username()


#Cliente y Colaborador deberán estar integrados con el modelo Profile

class Cliente(models.Model):
    # Relacion con el modelo Perfil
    user_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    # Atributos especificos del Cliente
    preferencias = models.ManyToManyField(to='Categoria')

    #Para que aparezcan los nombres/etiquetas
    def __str__(self):
        return f'Cliente: {self.user_profile.user.get_username()}'

class Colaborador(models.Model):
    # Relacion con el modelo Perfil
    user_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    # Atributos especificos del Colaborador
    reputacion = models.FloatField()
    cobertura_entrega = models.ManyToManyField(to='Localizacion')

    #Para que aparezcan los nombres/etiquetas
    def __str__(self):
        return f'Colaborador: {self.user_profile.user.get_username()}'

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------



# Create your models here.
class Proveedor(models.Model):
    ruc = models.CharField(max_length=11)
    razon_social = models.CharField(max_length=20)
    telefono = models.CharField(max_length=9)

    #Para que aparezcan los nombres/etiquetas de los atributos
    def __str__(self):
        return self.razon_social


class Categoria(models.Model):
    codigo = models.CharField(max_length=4)
    nombre = models.CharField(max_length=50)

    #Para que aparezcan los nombres/etiquetas de las categorias
    def __str__(self):
        return f'{self.codigo}: {self.nombre}'


class Localizacion(models.Model):
    distrito = models.CharField(max_length=20)
    provincia = models.CharField(max_length=20)
    departamento = models.CharField(max_length=20)

    #Para que aparezcan los nombres/etiquetas de las localizaciones
    def __str__(self):
        return f'{self.distrito}, {self.provincia}, {self.departamento}'


class Producto(models.Model):
    # Relaciones
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, null=True)

    # Atributos
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField()
    precio = models.FloatField()
    estado = models.CharField(max_length=3)
    descuento = models.FloatField(default=0)

    #Para que aparezcan los nombres/etiquetas de los productos
    def __str__(self):
        return self.nombre

    # Métodos
    def precio_final(self):
        return self.precio * (1 - self.descuento)

    def sku(self):
        codigo_categoria = self.categoria.codigo.zfill(4)
        codigo_producto = str(self.id).zfill(6)

        return f'{codigo_categoria}-{codigo_producto}'
