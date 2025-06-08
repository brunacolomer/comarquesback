from rest_framework import serializers

from .models import Usuari, Poblacio, Amistat

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
        
