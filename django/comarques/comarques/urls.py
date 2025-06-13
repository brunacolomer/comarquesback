"""
URL configuration for comarques project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenVerifyView

from comunitat.views import RegistreView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from comunitat.views import RegistreView, LlistaPoblacionsView, CrearAmistatView, AmistatsPerComarcaView, UsuariRankingView, CrearRepteOriginalView, DetallRepteView, AfegirDescripcioComarcaView, AssolitView, CrearRepteCopiatView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenObtainPairView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #path('api/token/blacklist/', TokenObtainPairView.as_view(), name='token_blacklist'),
    path('api/registre/', RegistreView.as_view(), name='registre'),
    path('api/poblacions/', LlistaPoblacionsView.as_view(), name='llista_poblacions'),
    path('api/amistats/crear/', CrearAmistatView.as_view(), name='crear_amistat'),
    path('api/amistats/comarques/', AmistatsPerComarcaView.as_view(), name='amistats_per_comarca'),
    path('api/amistats/ranking/', UsuariRankingView.as_view(), name='ranking_amics'),
    path('api/repte/original/', CrearRepteOriginalView.as_view(), name='crear_repte_original'),
    path('api/repte/copiat/', CrearRepteCopiatView.as_view(), name='crear_repte_copiat'),
    path('api/repte/<int:repte_id>/descripcio', AfegirDescripcioComarcaView.as_view(), name='crear o modificar descripcio'),
    path('api/repte/<int:repte_id>/', DetallRepteView.as_view(), name='detall_repte'),
    path('api/repte/<int:repte_id>/assolit', AssolitView.as_view(), name='assolit_repte')   
]

schema_view = get_schema_view(
    openapi.Info(
        title="Documentació de l'API",
        default_version='v1',
        description="Endpoints disponibles",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('schema/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
