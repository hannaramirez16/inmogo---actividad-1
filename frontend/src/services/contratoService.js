import api from './api';

export const contratoService = {
  // Listar todos los contratos
  getAll: async (params = {}) => {
    const response = await api.get('/contratos/contratos/', { params });
    return response.data;
  },

  // Obtener contrato por ID
  getById: async (id) => {
    const response = await api.get(`/contratos/contratos/${id}/`);
    return response.data;
  },

  // Crear contrato
  create: async (contratoData) => {
    const response = await api.post('/contratos/contratos/', contratoData);
    return response.data;
  },

  // Actualizar contrato
  update: async (id, contratoData) => {
    const response = await api.put(`/contratos/contratos/${id}/`, contratoData);
    return response.data;
  },

  // Obtener contratos activos
  getActivos: async () => {
    const response = await api.get('/contratos/contratos/activos/');
    return response.data;
  },

  // Obtener contratos vencidos
  getVencidos: async () => {
    const response = await api.get('/contratos/contratos/vencidos/');
    return response.data;
  },

  // Obtener contratos por vencer
  getPorVencer: async () => {
    const response = await api.get('/contratos/contratos/por_vencer/');
    return response.data;
  },

  // Finalizar contrato
  finalizar: async (id) => {
    const response = await api.post(`/contratos/contratos/${id}/finalizar/`);
    return response.data;
  },

  // Generar PDF del contrato
  generarPDF: async (id) => {
    const response = await api.get(`/contratos/contratos/${id}/generar_pdf/`, {
      responseType: 'blob',
    });
    // Crear un link para descargar el PDF
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `contrato_${id}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },
};