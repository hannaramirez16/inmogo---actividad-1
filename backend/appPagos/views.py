from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.utils import timezone
from backend.utils.pdf_generator import PDFGenerator
from .models import CuentaCobro, Pago, EstadoCuenta
from .serializers import (
    CuentaCobroSerializer, CuentaCobroListSerializer,
    PagoSerializer, PagoListSerializer,
    EstadoCuentaSerializer
)

class CuentaCobroViewSet(viewsets.ModelViewSet):
    queryset = CuentaCobro.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CuentaCobroListSerializer
        return CuentaCobroSerializer
    
    @action(detail=True, methods=['get'])
    def generar_pdf(self, request, pk=None):
        """Genera el PDF de la cuenta de cobro"""
        cuenta = self.get_object()
        
        pdf = PDFGenerator.generar_cuenta_cobro(cuenta)
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="cuenta_cobro_{cuenta.numero_cuenta}.pdf"'
        
        return({
            'mensaje': f'{actualizadas} cuentas actualizadas',
            'cuentas_actualizadas': actualizadas
        })


class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PagoListSerializer
        return PagoSerializer
    
    @action(detail=False, methods=['get'])
    def pendientes_aprobacion(self, request):
        """Lista pagos pendientes de aprobación"""
        pagos = self.queryset.filter(estado='pendiente')
        serializer = PagoListSerializer(pagos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def aprobar(self, request, pk=None):
        """Aprueba un pago"""
        pago = self.get_object()
        # En un caso real, obtener el usuario del request.user
        usuario = request.user if request.user.is_authenticated else None
        pago.aprobar(usuario)
        serializer = self.get_serializer(pago)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def rechazar(self, request, pk=None):
        """Rechaza un pago"""
        pago = self.get_object()
        observaciones = request.data.get('observaciones', None)
        pago.rechazar(observaciones)
        serializer = self.get_serializer(pago)
        return Response(serializer.data)


class EstadoCuentaViewSet(viewsets.ModelViewSet):
    queryset = EstadoCuenta.objects.all()
    serializer_class = EstadoCuentaSerializer
    
    @action(detail=False, methods=['get'])
    def por_contrato(self, request):
        """Lista estados de cuenta de un contrato específico"""
        contrato_id = request.query_params.get('contrato_id')
        if not contrato_id:
            return Response({'error': 'Se requiere contrato_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        estados = self.queryset.filter(contrato_id=contrato_id)
        serializer = self.get_serializer(estados, many=True)
        return Response(serializer.data)