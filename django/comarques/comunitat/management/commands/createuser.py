from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from comunitat.models import Poblacio

class Command(BaseCommand):
    help = "Crea un superusuari amb una població associada."

    def handle(self, *args, **kwargs):
        Usuari = get_user_model()

        self.stdout.write("🔐 Creació de superusuari personalitzat")

        username = input("Nom d'usuari: ").strip()
        email = input("Correu electrònic: ").strip()
        password = input("Contrasenya: ").strip()
        poblacio_nom = input("Nom de la població: ").strip()

        # Verificació de població
        try:
            poblacio = Poblacio.objects.get(nom__iexact=poblacio_nom)
        except Poblacio.DoesNotExist:
            self.stderr.write(f"❌ La població '{poblacio_nom}' no existeix.")
            return

        # Verificació de superusuari existent
        if Usuari.objects.filter(username=username).exists():
            self.stdout.write(f"⚠️  Ja existeix un usuari amb el nom '{username}'.")
            return

        # Creació
        Usuari.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            poblacio=poblacio
        )
        self.stdout.write(f"✅ Superusuari '{username}' creat amb població '{poblacio.nom}'.")
