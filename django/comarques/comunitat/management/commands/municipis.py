# comunitat/management/commands/loadmunicipis.py

import csv
import requests
import pandas as pd

from django.core.management.base import BaseCommand
from comunitat.models import Comarca, Poblacio
import re
from unidecode import unidecode

def normalitza_nom(nom):
  
    if not isinstance(nom, str):
        return ""
    nom = nom.strip().lower()
    nom = unidecode(nom)
    nom = re.sub(r"^(el|la|els|les|l[’'])\s*", "", nom)
    return nom


class Command(BaseCommand):
    help = "Importa municipis i comarques reals de Catalunya des de la Viquipèdia"

    URL = "https://ca.wikipedia.org/wiki/Llista_de_municipis_de_Catalunya"

    def handle(self, *args, **kwargs):
        self.stdout.write("Descarregant taules des de la Viquipèdia...")

        # Llegeix totes les taules amb classe 'wikitable'
        tables = pd.read_html(self.URL, attrs={"class": "wikitable"})

        self.stdout.write(f"Trobades {len(tables)} taules. Processant...")

        municipis_afegits = 0
        comarques_cache = {}
        comarques = {normalitza_nom(c.nom): c for c in Comarca.objects.all()}
        print(comarques)
        for table in tables:
            # Noms de columnes pot variar, assegurem que les dues claus existeixen
            if "Municipi" in table.columns and "Comarca" in table.columns:
                for _, row in table.iterrows():
                    nom_municipi = row["Municipi"].strip()
                    nom_comarca = row["Comarca"].strip()
                    nom_municipi = nom_municipi.title()
                    if nom_comarca == "Baixa Cerdanya":
                        nom_comarca = "Cerdanya"
                    comarca = comarques.get(unidecode(nom_comarca.lower()))
                   
                    print(comarca, nom_comarca)
                    poblacio = Poblacio.objects.get_or_create(
                        nom=nom_municipi,
                        comarca=comarca
                    )
                    municipis_afegits += 1
                   
        self.stdout.write(self.style.SUCCESS(f"Import complet: {municipis_afegits} municipis afegits."))
