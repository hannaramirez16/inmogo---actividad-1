import api from './api';

export const uploadService = {
  // Subir un archivo
  upload: async (file, tipo = 'otro') => {
    const formData = new FormData();
    formData.append('archivo', file);
    formData.append('tipo', tipo);

    const response = await api.post('/uploads/archivos/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Subir múltiples archivos
  uploadMultiple: async (files, tipo = 'otro') => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('archivos', file);
    });
    formData.append('tipo', tipo);

    const response = await api.post('/uploads/archivos/upload_multiple/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Obtener mis archivos
  getMisArchivos: async () => {
    const response = await api.get('/uploads/archivos/mis_archivos/');
    return response.data;
  },

  // Eliminar archivo
  delete: async (id) => {
    const response = await api.delete(`/uploads/archivos/${id}/`);
    return response.data;
  },
};