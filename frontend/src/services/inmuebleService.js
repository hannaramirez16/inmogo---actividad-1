import api from './api';

export const inmuebleService = {
  // Listar todos los inmuebles
  getAll: async (params = {}) => {
    const response = await api.get('/inmuebles/inmuebles/', { params });
    return response.data;
  },

  // Obtener un inmueble por ID
  getById: async (id) => {
    const response = await api.get(`/inmuebles/inmuebles/${id}/`);
    return response.data;
  },

  // Crear inmueble
  create: async (inmuebleData) => {
    const response = await api.post('/inmuebles/inmuebles/', inmuebleData);
    return response.data;
  },

  // Actualizar inmueble
  update: async (id, inmuebleData) => {
    const response = await api.put(`/inmuebles/inmuebles/${id}/`, inmuebleData);
    return response.data;
  },

  // Eliminar inmueble
  delete: async (id) => {
    const response = await api.delete(`/inmuebles/inmuebles/${id}/`);
    return response.data;
  },

  // Obtener inmuebles disponibles
  getDisponibles: async () => {
    const response = await api.get('/inmuebles/inmuebles/disponibles/');
    return response.data;
  },

  // Obtener mis inmuebles
  getMisInmuebles: async () => {
    const response = await api.get('/inmuebles/inmuebles/mis_inmuebles/');
    return response.data;
  },

  // Obtener categorías
  getCategorias: async () => {
    const response = await api.get('/inmuebles/categorias/');
    return response.data;
  },

  // Obtener muebles de un inmueble
  getMuebles: async (inmuebleId) => {
    const response = await api.get(`/inmuebles/inmuebles/${inmuebleId}/muebles/`);
    return response.data;
  },

  // Agregar mueble a un inmueble
  agregarMueble: async (inmuebleId, muebleData) => {
    const response = await api.post(`/inmuebles/inmuebles/${inmuebleId}/agregar_mueble/`, muebleData);
    return response.data;
  },
};