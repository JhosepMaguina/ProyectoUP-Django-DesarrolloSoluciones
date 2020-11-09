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
    def get_precio_final(self):
        return self.precio * (1 - self.descuento)

    def sku(self):
        codigo_categoria = self.categoria.codigo.zfill(4)
        codigo_producto = str(self.id).zfill(6)

        return f'{codigo_categoria}-{codigo_producto}'

#Para que el producto tenga imagen.
class ProductoImage(models.Model):
    product = models.ForeignKey('Producto', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="products", null=True, blank=True)



class Pedido(models.Model):
    # Relaciones
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE) #Cuando se elimine un cliente se borrarán todos sus pedidos (on_delete=models.CASCADE).
    repartidor = models.ForeignKey('Colaborador', on_delete=models.SET_NULL, null=True) #Si se elimina el colaborador no se eliminará el pedido, sino se pondrá como nulo (on_delete=models.SET_NULL, null=True).
    ubicacion = models.ForeignKey('Localizacion', on_delete=models.SET_NULL, null=True) #Si se elimina una localización, los pedidos tendrán el valor nulo (on_delete=models.SET_NULL, null=True).

    # Atributos
    fecha_creacion = models.DateTimeField(auto_now=True) #Cuando se cree una instancia de pedido automáticamente colocará la hora que fue creada (auto_now=True).
    fecha_entrega = models.DateTimeField(blank=True, null=True) #Cuando el atributo no tenga valor estará vacío (blank=True, null=True).
    estado = models.CharField(max_length=3)
    direccion_entrega = models.CharField(max_length=100, blank=True, null=True) #El atributo puede estar vacio sin que haya algún problema (blank=True, null=True). Porque en un inicio no se le pedirá al usuario su dirección.
    tarifa = models.FloatField(blank=True, null=True) #Un número con decimales (FloatField) que puede estar vacío (blank=True, null=True).

    #Para que aparezcan los nombres/etiquetas de las categorias.
    def __str__(self):
        return f'{self.cliente} - {self.fecha_creacion} - {self.estado}'

    #Método personalizado
    #Para obtener todos los detalles de pedido relacionados a un pedido en específico.
    #Utiliza el método de "detalle de pedido" para cada línea (for detalle) en los detalles de pedido (in detalles) se sumará el subtotal (detalle.get_subtotal()) para obtener el total (total +=).
    #Por último se le suma la tarifa (total += self.tarifa) para que finalmente devuelva el total (return total).
    def get_total(self):
        detalles = self.detallepedido_set.all()
        total = 0
        for detalle in detalles:
            total += detalle.get_subtotal()
        total += self.tarifa
        return total


class DetallePedido(models.Model):
    # Relaciones
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE) #Si se elimina el producto, se elimina el detablle de pedido (on_delete=models.CASCADE).
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE) #Si se elimina el pedido se eliminan sus detalles de pedido (on_delete=models.CASCADE).

    # Atributos
    cantidad = models.IntegerField(blank=True, null=True) #Para determinar la cantidad que el cliente está pidiendo de este producto.

    #Para que aparezcan los nombres/etiquetas de las categorias
    def __str__(self):
        return f'{self.pedido.id} - {self.cantidad} x {self.producto.nombre}'

    #Método personalizado
    #El get_subtotal devuelve el método get_precio_final de Producto (considerando todo tipo de descuentos) multiplicado por la cantidad.
    def get_subtotal(self):
        return self.producto.get_precio_final() * self.cantidad
