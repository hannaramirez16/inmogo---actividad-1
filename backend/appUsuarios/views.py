from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario
from .serializers import UsuarioSerializer, UsuarioListSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UsuarioListSerializer
        return UsuarioSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Registro de nuevo usuario"""
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            
            # Generar tokens JWT
            refresh = RefreshToken.for_user(usuario)
            
            return Response({
                'user': UsuarioSerializer(usuario).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Login de usuario"""
        from django.contrib.auth import authenticate
        
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Se requiere username y password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        usuario = authenticate(username=username, password=password)
        
        if usuario is None:
            return Response(
                {'error': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not usuario.activo:
            return Response(
                {'error': 'Usuario inactivo'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(usuario)
        
        return Response({
            'user': UsuarioSerializer(usuario).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Obtiene información del usuario actual"""
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def propietarios(self, request):
        """Lista todos los propietarios activos"""
        propietarios = Usuario.objects.filter(rol='propietario', activo=True)
        serializer = UsuarioListSerializer(propietarios, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inquilinos(self, request):
        """Lista todos los inquilinos activos"""
        inquilinos = Usuario.objects.filter(rol='inquilino', activo=True)
        serializer = UsuarioListSerializer(inquilinos, many=True)
        return Response(serializer.data)