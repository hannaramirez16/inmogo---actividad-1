from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <- AGREGAR
from django.http import HttpResponse  # <- AGREGAR
from django.utils import timezone
from backend.utils.pdf_generator import PDFGenerator  # <- AGREGAR
from .models import Contrato, RenovacionContrato
from .serializers import ContratoSerializer, ContratoListSerializer, RenovacionContratoSerializer

class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    permission_classes = [IsAuthenticated]  # <- AGREGAR (opcional, para proteger el endpoint)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ContratoListSerializer
        return ContratoSerializer
    
    # ============================================
    # NUEVO MÉTODO PARA GENERAR PDF
    # ============================================
    @action(detail=True, methods=['get'])
    def generar_pdf(self, request, pk=None):
        """Genera el PDF del contrato"""
        contrato = self.get_object()
        
        # Generar el PDF usando la utilidad
        pdf = PDFGenerator.generar_contrato(contrato)
        
        # Crear la respuesta HTTP con el PDF
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="contrato_{contrato.numero_contrato}.pdf"'
        
        return response
    # ============================================
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Lista contratos activos"""
        contratos = self.queryset.filter(estado='activo')
        serializer = ContratoListSerializer(contratos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def vencidos(self, request):
        """Lista contratos vencidos"""
        contratos = self.queryset.filter(estado='vencido')
        serializer = ContratoListSerializer(contratos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_vencer(self, request):
        """Lista contratos que vencen en los próximos 30 días"""
        fecha_limite = timezone.now().date() + timezone.timedelta(days=30)
        contratos = self.queryset.filter(
            estado='activo',
            fecha_fin__lte=fecha_limite,
            fecha_fin__gte=timezone.now().date()
        )
        serializer = ContratoListSerializer(contratos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def finalizar(self, request, pk=None):
        """Finaliza un contrato"""
        contrato = self.get_object()
        contrato.estado = 'finalizado'
        contrato.fecha_finalizacion = timezone.now()
        contrato.save()
        serializer = self.get_serializer(contrato)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def verificar_vencimientos(self, request):
        """Verifica y actualiza contratos vencidos"""
        contratos_activos = self.queryset.filter(estado='activo')
        actualizados = 0
        for contrato in contratos_activos:
            if contrato.verificar_vencimiento():
                actualizados += 1
        return Response({
            'mensaje': f'{actualizados} contratos actualizados a estado vencido',
            'contratos_actualizados': actualizados
        })


class RenovacionContratoViewSet(viewsets.ModelViewSet):
    queryset = RenovacionContrato.objects.all()
    serializer_class = RenovacionContratoSerializer