from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Archivo
from .serializers import ArchivoSerializer

class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = Archivo.objects.all()
    serializer_class = ArchivoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def perform_create(self, serializer):
        """Guarda el archivo con información del usuario"""
        archivo = self.request.FILES['archivo']
        serializer.save(
            usuario=self.request.user,
            nombre_original=archivo.name,
            tamano=archivo.size
        )
    
    @action(detail=False, methods=['get'])
    def mis_archivos(self, request):
        """Lista los archivos del usuario actual"""
        archivos = self.queryset.filter(usuario=request.user)
        serializer = self.get_serializer(archivos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def upload_multiple(self, request):
        """Sube múltiples archivos a la vez"""
        archivos = request.FILES.getlist('archivos')
        tipo = request.data.get('tipo', 'otro')
        
        if not archivos:
            return Response(
                {'error': 'No se enviaron archivos'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        resultados = []
        errores = []
        
        for archivo in archivos:
            data = {
                'archivo': archivo,
                'tipo': tipo
            }
            serializer = self.get_serializer(data=data)
            
            if serializer.is_valid():
                self.perform_create(serializer)
                resultados.append(serializer.data)
            else:
                errores.append({
                    'archivo': archivo.name,
                    'errores': serializer.errors
                })
        
        return Response({
            'exitosos': len(resultados),
            'fallidos': len(errores),
            'archivos': resultados,
            'errores': errores
        }, status=status.HTTP_201_CREATED if resultados else status.HTTP_400_BAD_REQUEST)