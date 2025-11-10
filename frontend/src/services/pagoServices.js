import api from './api';

export const pagoService = {
  // Cuentas de Cobro
  cuentasCobro: {
    getAll: async (params = {}) => {
      const response = await api.get('/pagos/cuentas-cobro/', { params });
      return response.data;
    },

    getById: async (id) => {
      const response = await api.get(`/pagos/cuentas-cobro/${id}/`);
      return response.data;
    },

    create: async (cuentaData) => {
      const response = await api.post('/pagos/cuentas-cobro/', cuentaData);
      return response.data;
    },

    getPendientes: async () => {
      const response = await api.get('/pagos/cuentas-cobro/pendientes/');
      return response.data;
    },

    getVencidas: async () => {
      const response = await api.get('/pagos/cuentas-cobro/vencidas/');
      return response.data;
    },

    generarPDF: async (id) => {
      const response = await api.get(`/pagos/cuentas-cobro/${id}/generar_pdf/`, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `cuenta_cobro_${id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    },
  },

  // Pagos
  pagos: {
    getAll: async (params = {}) => {
      const response = await api.get('/pagos/pagos/', { params });
      return response.data;
    },

    getById: async (id) => {
      const response = await api.get(`/pagos/pagos/${id}/`);
      return response.data;
    },

    create: async (pagoData) => {
      const response = await api.post('/pagos/pagos/', pagoData);
      return response.data;
    },

    aprobar: async (id) => {
      const response = await api.post(`/pagos/pagos/${id}/aprobar/`);
      return response.data;
    },

    rechazar: async (id, observaciones) => {
      const response = await api.post(`/pagos/pagos/${id}/rechazar/`, { observaciones });
      return response.data;
    },

    getPendientesAprobacion: async () => {
      const response = await api.get('/pagos/pagos/pendientes_aprobacion/');
      return response.data;
    },
  },
};