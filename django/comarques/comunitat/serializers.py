from rest_framework import serializers

from .models import Usuari

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