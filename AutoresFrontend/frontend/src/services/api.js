import axios from "axios";

const API_BASE_URL = "http://localhost:5000";

// Crear instancia de axios
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor para agregar token a las peticiones
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para manejar respuestas y errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// Servicios de autenticación
export const authService = {
  login: (credentials) => api.post("/auth/login", credentials),
  register: (userData) => api.post("/auth/register", userData),
  verify: () => api.get("/auth/verify"),

  // Métodos auxiliares
  getToken: () => localStorage.getItem("token"),
  getUser: () => JSON.parse(localStorage.getItem("user") || "{}"),
  setAuthData: (token, user) => {
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(user));
  },
  clearAuthData: () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  },
};

// Servicios de autores
export const autorService = {
  getAll: () => api.get("/autores"),
  getById: (id) => api.get(`/autor/${id}`),
  create: (data) => api.post("/autor", data),
  update: (id, data) => api.put(`/autor/${id}`, data),
  delete: (id) => api.delete(`/autor/${id}`),
  getLibros: (id) => api.get(`/autor/${id}/libros`),
};

// Servicios de libros
export const libroService = {
  getAll: () => api.get("/libros"),
  getById: (id) => api.get(`/libro/${id}`),
  create: (data) => api.post("/libro", data),
  update: (id, data) => api.put(`/libro/${id}`, data),
  delete: (id) => api.delete(`/libro/${id}`),
  getAutores: (id) => api.get(`/libro/${id}/autores`),
};

// Servicios de géneros
export const generoService = {
  getAll: () => api.get("/generos"),
  getById: (id) => api.get(`/genero/${id}`),
  create: (data) => api.post("/genero", data),
  update: (id, data) => api.put(`/genero/${id}`, data),
  delete: (id) => api.delete(`/genero/${id}`),
};

export default api;
