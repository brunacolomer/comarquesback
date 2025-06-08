from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class TipusVisibilitat(models.TextChoices):
    ME = 'ME', 'Només jo'
    AMICS = 'AMICS', 'Només amistats'
    PUBLIC = 'PUBLIC', 'Públic'
   
class Insignia(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    titol = models.CharField(max_length=75, null=False)
    text = models.CharField(max_length=255, null=False)
    icona = models.URLField(default="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.flaticon.es%2Ficono-gratis%2Ftrofeo_536056&psig=AOvVaw1bTfl895dsISlq8UIpoJmT&ust=1747325495554000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCPDL0u2so40DFQAAAAAdAAAAABAE")
    
    def __str__(self):
        return f"{self.titol} - {self.text}"
    


class Usuari(AbstractUser):
    puntuacio = models.IntegerField(default=0)
    insignies = models.ManyToManyField(Insignia, blank=True, related_name='obte')
    poblacio = models.ForeignKey('Poblacio', on_delete=models.RESTRICT, related_name='pertany')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username'], name='usuari_unic')
        ]

    def __str__(self):
        return self.username


class Amistat(models.Model):
    usuari1 = models.ForeignKey(Usuari, on_delete=models.RESTRICT, related_name='amistats_usuari1')
    usuari2 = models.ForeignKey(Usuari, on_delete=models.RESTRICT, related_name='amistats_usuari2')
    data = models.DateTimeField(auto_now_add=True)
    descripcio = models.TextField(blank=True, null=True)
    foto = models.ImageField( upload_to='amistats/', null=False)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['usuari1', 'usuari2'], name='amistat_unica')
    ]

    def __str__(self):
        return f"{self.usuari1.username} - {self.usuari2.username} ({self.data})"
 

class Repte(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    titol = models.CharField(max_length=75, null=False)
    visiblitat = models.CharField(max_length=10, choices=TipusVisibilitat.choices, default=TipusVisibilitat.PUBLIC)
    usuari = models.ForeignKey(Usuari, on_delete=models.RESTRICT, related_name='repte_usuari')

class Original(Repte):
    permissos = models.TextField(null=False, choices=TipusVisibilitat.choices, default=TipusVisibilitat.PUBLIC)
    
class Copiat(Repte):
    basat = models.ForeignKey(Original, on_delete=models.RESTRICT)
    def __str__(self):
        return f"Repte Copiat: {self.titol}"


class Missatge(models.Model):
    dataHora = models.DateTimeField()
    text = models.TextField()
    receptor = models.ForeignKey(Usuari, on_delete=models.RESTRICT, related_name= 'missatge_receptor')
    emisor = models.ForeignKey (Usuari, on_delete=models.RESTRICT, related_name= 'missatge_emisor')
    
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['emisor', 'receptor', 'dataHora'], name= 'missatge_unic')
        ]

class Comarca(models.Model):
    nom = models.CharField(primary_key=True, max_length=50)
    habitants = models.IntegerField()

class Distancia(models.Model):
    comarca1 = models.ForeignKey(Comarca, on_delete=models.RESTRICT, related_name='distancia_comarca1')
    comarca2 = models.ForeignKey(Comarca, on_delete=models.RESTRICT, related_name='distancia_comarca2')
    distancia = models.FloatField()
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['comarca1', 'comarca2'], name= 'distancia_unic')
        ]

class Poblacio(models.Model):
    nom = models.CharField(primary_key=True, max_length=50)
    comarca = models.ForeignKey(Comarca, on_delete=models.RESTRICT, related_name= 'pertany')

class Descripcio(models.Model):
    original = models.ForeignKey(Original, on_delete=models.RESTRICT,  related_name="descripcio_original")
    comarca = models.ForeignKey(Comarca, on_delete=models.RESTRICT,  related_name="descripcio_comarca")
    descripcio = models.TextField()
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['original', 'comarca'], name= 'descripcio_unic')
        ]  
 

class Assolit(models.Model):
    repte = models.ForeignKey(Repte, on_delete=models.RESTRICT)
    comarca= models.ForeignKey(Comarca, on_delete=models.RESTRICT)
    foto = models.URLField()
    descripcio = models.TextField(blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['repte', 'comarca'], name= 'assolit_unic')
        ]


class Perfil(models.Model):
    usuari = models.OneToOneField(Usuari, on_delete=models.RESTRICT, related_name='creat')
    likes = models.ManyToManyField('self', blank=True)
    repte = models.ForeignKey(Repte, on_delete=models.RESTRICT, related_name='preferit')
    descripcio = models.CharField( max_length=255)
    foto = models.URLField()
    