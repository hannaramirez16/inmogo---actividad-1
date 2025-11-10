import api from './api';

export const mantenimientoService = {
  // Listar todas las solicitudes
  getAll: async (params = {}) => {
    const response = await api.get('/mantenimiento/solicitudes/', { params });
    return response.data;
  },

  // Obtener solicitud por ID
  getById: async (id) => {
    const response = await api.get(`/mantenimiento/solicitudes/${id}/`);
    return response.data;
  },

  // Crear solicitud
  create: async (solicitudData) => {
    const response = await api.post('/mantenimiento/solicitudes/', solicitudData);
    return response.data;
  },

  // Actualizar solicitud
  update: async (id, solicitudData) => {
    const response = await api.put(`/mantenimiento/solicitudes/${id}/`, solicitudData);
    return response.data;
  },

  // Obtener solicitudes pendientes
  getPendientes: async () => {
    const response = await api.get('/mantenimiento/solicitudes/pendientes/');
    return response.data;
  },

  // Obtener solicitudes urgentes
  getUrgentes: async () => {
    const response = await api.get('/mantenimiento/solicitudes/urgentes/');
    return response.data;
  },

  // Obtener solicitudes en progreso
  getEnProgreso: async () => {
    const response = await api.get('/mantenimiento/solicitudes/en_progreso/');
    return response.data;
  },

  // Asignar técnico
  asignar: async (id, usuarioId) => {
    const response = await api.post(`/mantenimiento/solicitudes/${id}/asignar/`, {
      usuario_id: usuarioId,
    });
    return response.data;
  },

  // Iniciar trabajo
  iniciar: async (id) => {
    const response = await api.post(`/mantenimiento/solicitudes/${id}/iniciar/`);
    return response.data;
  },

  // Completar trabajo
  completar: async (id, data) => {
    const response = await api.post(`/mantenimiento/solicitudes/${id}/completar/`, data);
    return response.data;
  },

  // Calificar servicio
  calificar: async (id, calificacion, comentario) => {
    const response = await api.post(`/mantenimiento/solicitudes/${id}/calificar/`, {
      calificacion,
      comentario,
    });
    return response.data;
  },

  // Agregar seguimiento
  agregarSeguimiento: async (id, descripcion, fotos = []) => {
    const response = await api.post(`/mantenimiento/solicitudes/${id}/agregar_seguimiento/`, {
      descripcion,
      fotos,
    });
    return response.data;
  },
};