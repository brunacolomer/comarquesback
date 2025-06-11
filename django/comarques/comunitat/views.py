from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Poblacio, Amistat, Usuari, Repte, Original, Descripcio, Assolit, Copiat, Comarca
from .serializers import RegistreSerializer, PoblacioSerializer, AmistatSerializer, UsuariRankingSerializer, OriginalRepteSerializer, DescripcioSerializer, AssolitSerializer, CopiaRepteSerializer

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
    
class CrearRepteOriginalView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=OriginalRepteSerializer,
        responses={201: 'Repte original creat correctament', 400: 'Error en la creació del repte'},
        operation_description="Crea un nou repte original"
    )
    def post(self, request):
        serializer = OriginalRepteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            repte = serializer.save()
            return Response({
                "message": "Repte original creat correctament",
                "repte_id": repte.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views.py
class CrearRepteCopiatView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=CopiaRepteSerializer,
        responses={201: 'Repte copiat correctament', 400: 'Error de validació'},
        operation_description="Copia un repte original i el crea per l’usuari actual"
    )
    def post(self, request):
        serializer = CopiaRepteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            repte = serializer.save()
            return Response({
                "message": "Repte copiat correctament",
                "repte_id": repte.id,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetallRepteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: 'Detall del repte', 404: 'Repte no trobat'})
    def get(self, request, repte_id):
        try:
            repte = Repte.objects.get(id=repte_id)
        except Repte.DoesNotExist:
            return Response({"detail": "Repte no trobat"}, status=status.HTTP_404_NOT_FOUND)

        # Comprovem si és un repte original i si és de l'usuari
        try:
            original = Original.objects.get(id=repte.id, usuari=request.user)
            es_teu = True
            es_original = True
        except Original.DoesNotExist:
            es_teu = False
            es_original = False

        # Carreguem assolits
        assolits = Assolit.objects.filter(repte=repte).select_related('comarca')

        # Carreguem descripcions segons si és original o copiat
        descripcions = []
        if es_original:
            descripcions = Descripcio.objects.filter(original=repte).select_related('comarca')
        else:
            try:
                original = Copiat.objects.get(id=repte.id).basat
                descripcions = Descripcio.objects.filter(original=original).select_related('comarca')
            except Copiat.DoesNotExist:
                descripcions = []

        assolits_dict = {a.comarca.nom: a for a in assolits}
        descripcions_dict = {d.comarca.nom: d for d in descripcions}

        totes_les_comarques = Comarca.objects.all()
        comarca_data = []

        for comarca in totes_les_comarques:
            comarca_dict = {
                "nom": comarca.nom,
                "descripcio_repte": None,
                "assolit": False,
                "foto": None,
                "data": None,
                "descripcio_assolit": None
            }

            a = assolits_dict.get(comarca.nom)
            if a:
                comarca_dict["assolit"] = True
                comarca_dict["foto"] = request.build_absolute_uri(a.foto.url) if a.foto else None
                comarca_dict["data"] = a.data.strftime("%d-%m-%Y")
                comarca_dict["descripcio_assolit"] = a.descripcio

            d = descripcions_dict.get(comarca.nom)
            if d:
                comarca_dict["descripcio_repte"] = d.descripcio

            comarca_data.append(comarca_dict)

        return Response({
            "id": repte.id,
            "titol": repte.titol,
            "es_original": es_teu,
            "comarques": comarca_data
        }, status=status.HTTP_200_OK)
    
class AfegirDescripcioComarcaView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=DescripcioSerializer,
        responses={
            200: 'Descripció guardada correctament',
            400: 'Error de validació o repte no vàlid'
        },
        operation_description="Afegeix o modifica una descripció per una comarca dins d’un repte original"
    )
    def post(self, request, repte_id):
        original = Original.objects.get(id=repte_id)
        serializer = DescripcioSerializer(data=request.data, context={'request': request, 'original': original})
        if serializer.is_valid():
            descripcio = serializer.save()
            return Response({
                "message": "Descripció guardada correctament",
                "repte_id": descripcio.original.id,
                "comarca": descripcio.comarca.nom,
                "descripcio": descripcio.descripcio
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AssolitView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        request_body=AssolitSerializer,
        responses={200: 'Assolit guardat correctament', 400: 'Error de validació'},
        operation_description="Afegeix o modifica un assoliment per una comarca dins d’un repte"
    )

    def post(self, request, repte_id):
        repte = Repte.objects.get(id=repte_id)
        serializer = AssolitSerializer(data=request.data, context={'request': request, 'repte': repte})
        if serializer.is_valid():
            assolit = serializer.save()
            return Response({
                "message": "Assolit guardat correctament",
                "repte_id": assolit.repte.id,
                "comarca": assolit.comarca.nom,
                "descripcio": assolit.descripcio,
                "foto": request.build_absolute_uri(assolit.foto.url),
                "data": assolit.data.strftime('%d-%m-%y')
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)