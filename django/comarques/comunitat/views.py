from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Poblacio, Amistat, Usuari
from .serializers import RegistreSerializer, PoblacioSerializer, AmistatSerializer, UsuariRankingSerializer

class RegistreView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=RegistreSerializer, responses={201: 'Usuari registrat correctament', 400: 'Error en el registre'})
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

class LlistaPoblacionsView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: 'Llista de poblacions'})
    def get(self, request):
        poblacions = Poblacio.objects.all()
        serializer = PoblacioSerializer(poblacions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CrearAmistatView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        request_body=AmistatSerializer,
        manual_parameters=[],
        responses={201: 'Amistat creada correctament', 400: 'Error en la creació de l\'amistat'},
        operation_description="Crea una nova amistat amb foto",
        consumes=['multipart/form-data']
    )
    def post(self, request):
        serializer = AmistatSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            amistat = serializer.save()
            return Response({
                "message": "Amistat creada correctament",
                "amistat_id": amistat.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AmistatsPerComarcaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuari = request.user
        amistats = Amistat.objects.filter(usuari1=usuari) | Amistat.objects.filter(usuari2=usuari)
        # Veure si l'usuari té amistats
        print(f"Usuari: {usuari.username}, Amistats trobades: {amistats.count()}")
        comarca_dict = {}
        for amistat in amistats:
            amic = amistat.usuari2 if amistat.usuari1 == usuari else amistat.usuari1
            comarca = amic.poblacio.comarca.nom
            if comarca not in comarca_dict:
                comarca_dict[comarca] = {
                    'num_amics': 0,
                    'amics': []
                }
            comarca_dict[comarca]['num_amics'] += 1
            comarca_dict[comarca]['amics'].append({
                'username': amic.username,
                'foto': request.build_absolute_uri(amistat.foto.url),
                'descripcio': amistat.descripcio or "",
                'data': amistat.data.strftime('%d-%m-%y %H:%M:%S')
            })

        return Response(comarca_dict, status=status.HTTP_200_OK)
    

class UsuariRankingView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: 'Llista de comarques amb el nombre d\'amics'})
    def get(self, request):
        usuari = request.user

        amics_1 = Usuari.objects.filter(
            id__in=Amistat.objects.filter(usuari1=usuari).values_list('usuari2_id', flat=True)
        )

        # Amics per usuari2
        amics_2 = Usuari.objects.filter(
            id__in=Amistat.objects.filter(usuari2=usuari).values_list('usuari1_id', flat=True)
        )

        # Unió d'amics + unió amb tu mateix
        ranking_qs = amics_1.union(amics_2, Usuari.objects.filter(id=usuari.id))

        # Ordenem per puntuació descendent
        ranking_ordenat = ranking_qs.order_by('-puntuacio')

        serializer = UsuariRankingSerializer(ranking_ordenat, many=True)
        return Response(serializer.data)  # Inclou l'usuari en la llista d'amics