from rest_framework import serializers

from .models import Usuari, Poblacio, Amistat, Original, Descripcio, Comarca, Assolit, Copiat

class RegistreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuari
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'poblacio')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        usuari = Usuari(**validated_data)
        usuari.set_password(password)
        usuari.save()
        return usuari
    
class PoblacioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poblacio
        fields = ['nom']

class AmistatSerializer(serializers.ModelSerializer):
    usuari2_username = serializers.CharField(write_only=True)
    foto = serializers.ImageField()
    class Meta:
        model = Amistat
        fields = ['foto', 'descripcio', 'usuari2_username']

    def create(self, validated_data):
        usuari1 = self.context['request'].user
        usuari2_username = validated_data.pop('usuari2_username')
        try:
            usuari2 = Usuari.objects.get(username=usuari2_username)
        except Usuari.DoesNotExist:
            raise serializers.ValidationError("Usuari destinatari no trobat.")
        if usuari1 == usuari2:
            raise serializers.ValidationError("No pots afegir-te a tu mateix com a amic.")
        if Amistat.objects.filter(usuari1=usuari1, usuari2=usuari2).exists() or Amistat.objects.filter(usuari1=usuari2, usuari2=usuari1).exists():
            raise serializers.ValidationError("Ja existeix una amistat entre aquests usuaris.")
        amistat = Amistat.objects.create(usuari1=usuari1, usuari2=usuari2, **validated_data)
        return amistat
    
class AmicPerComarcaSerializer(serializers.Serializer):
    comarca = serializers.CharField()
    num_amics = serializers.IntegerField()
    amics = serializers.ListField(
        child=serializers.DictField()
    )

class UsuariRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuari
        fields = ['username', 'puntuacio']

class OriginalRepteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Original
        fields = ['titol', 'visiblitat', 'permissos']
    def create(self, validated_data):
        usuari = self.context['request'].user
        return Original.objects.create(usuari=usuari,**validated_data)

class CopiaRepteSerializer(serializers.ModelSerializer):
    basat = serializers.PrimaryKeyRelatedField(queryset=Original.objects.all(), write_only=True)
    class Meta:
        model = Copiat
        fields = ['visiblitat', 'basat']
    def create(self, validated_data):
        usuari = self.context['request'].user
        basat = validated_data.pop('basat')
        return Copiat.objects.create(usuari=usuari, basat=basat, titol=basat.titol, visiblitat=validated_data['visiblitat'])


class DescripcioSerializer(serializers.ModelSerializer):
    comarca = serializers.SlugRelatedField(slug_field='nom', queryset=Comarca.objects.all())
    class Meta:
        model = Descripcio
        fields = ['comarca', 'descripcio']
    
    def create(self, validated_data):
        original = self.context['original']
        comarca = validated_data['comarca']
        text = validated_data['descripcio']
        descripcio, created = Descripcio.objects.update_or_create(
            original=original,
            comarca=comarca,
            defaults={'descripcio': text}
        )
        return descripcio
    
class AssolitSerializer(serializers.ModelSerializer):
    comarca = serializers.SlugRelatedField(slug_field='nom', queryset=Comarca.objects.all())
    foto = serializers.ImageField()
    class Meta:
        model = Assolit
        fields = ['comarca', 'descripcio', 'data', 'foto']
    
    def create(self, validated_data):
        repte = self.context['repte']
        assolit, _ = Assolit.objects.update_or_create(
            repte=repte,
            comarca=validated_data['comarca'],
            defaults={
                'foto': validated_data['foto'],
                'descripcio': validated_data.get('descripcio')
            }
        )
        return assolit


