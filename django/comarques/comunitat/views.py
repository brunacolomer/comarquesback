from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegistreSerializer

class RegistreView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegistreSerializer(data=request.data)
        if serializer.is_valid():
            usuari = serializer.save()

            refresh = RefreshToken.for_user(usuari)

            return Response({
                "message": "Usuari registrat correctament",
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
