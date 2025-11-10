import api from './api';

export const notificacionService = {
  // Listar todas las notificaciones
  getAll: async (params = {}) => {
    const response = await api.get('/notificaciones/notificaciones/', { params });
    return response.data;
  },

  // Obtener notificaciones no leídas
  getNoLeidas: async (usuarioId) => {
    const response = await api.get(`/notificaciones/notificaciones/no_leidas/?usuario_id=${usuarioId}`);
    return response.data;
  },

  // Contador de no leídas
  getContadorNoLeidas: async (usuarioId) => {
    const response = await api.get(`/notificaciones/notificaciones/contador_no_leidas/?usuario_id=${usuarioId}`);
    return response.data;
  },

  // Marcar como leída
  marcarLeida: async (id) => {
    const response = await api.post(`/notificaciones/notificaciones/${id}/marcar_leida/`);
    return response.data;
  },

  // Marcar todas como leídas
  marcarTodasLeidas: async (usuarioId) => {
    const response = await api.post('/notificaciones/notificaciones/marcar_todas_leidas/', {
      usuario_id: usuarioId,
    });
    return response.data;
  },

  // Eliminar notificaciones leídas
  eliminarLeidas: async (usuarioId) => {
    const response = await api.delete(`/notificaciones/notificaciones/eliminar_leidas/?usuario_id=${usuarioId}`);
    return response.data;
  },
};