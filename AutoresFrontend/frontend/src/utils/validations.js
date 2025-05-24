// Validaciones para el frontend
export const validations = {
  // Validaciones de usuario
  username: {
    required: (value) => !!value || "El nombre de usuario es requerido",
    minLength: (value) => (value && value.length >= 3) || "Mínimo 3 caracteres",
    maxLength: (value) =>
      (value && value.length <= 50) || "Máximo 50 caracteres",
  },

  password: {
    required: (value) => !!value || "La contraseña es requerida",
    minLength: (value) => (value && value.length >= 6) || "Mínimo 6 caracteres",
    maxLength: (value) =>
      (value && value.length <= 255) || "Máximo 255 caracteres",
  },

  email: {
    required: (value) => !!value || "El email es requerido",
    email: (value) => {
      const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return pattern.test(value) || "Email inválido";
    },
  },

  // Validaciones de autor
  autorNombre: {
    required: (value) => !!value?.trim() || "El nombre del autor es requerido",
    minLength: (value) =>
      (value && value.trim().length >= 2) || "Mínimo 2 caracteres",
    maxLength: (value) =>
      (value && value.length <= 100) || "Máximo 100 caracteres",
  },

  autorPais: {
    maxLength: (value) =>
      !value || value.length <= 50 || "Máximo 50 caracteres",
  },

  anioNacimiento: {
    validYear: (value) => {
      if (!value) return true;
      const year = parseInt(value);
      return (year >= 0 && year <= 2100) || "El año debe estar entre 0 y 2100";
    },
    numeric: (value) => !value || /^\d+$/.test(value) || "Solo números",
  },

  // Validaciones de libro
  libroTitulo: {
    required: (value) => !!value?.trim() || "El título del libro es requerido",
    minLength: (value) =>
      (value && value.trim().length >= 1) || "El título no puede estar vacío",
    maxLength: (value) =>
      (value && value.length <= 200) || "Máximo 200 caracteres",
  },

  anioPublicacion: {
    validYear: (value) => {
      if (!value) return true;
      const year = parseInt(value);
      return (year >= 0 && year <= 2100) || "El año debe estar entre 0 y 2100";
    },
    numeric: (value) => !value || /^\d+$/.test(value) || "Solo números",
  },

  generoId: {
    required: (value) => !!value || "El género es requerido",
  },

  autoresIds: {
    required: (value) =>
      (value && value.length > 0) || "Debe seleccionar al menos un autor",
  },

  // Validaciones de género
  generoNombre: {
    required: (value) => !!value?.trim() || "El nombre del género es requerido",
    minLength: (value) =>
      (value && value.trim().length >= 2) || "Mínimo 2 caracteres",
    maxLength: (value) =>
      (value && value.length <= 50) || "Máximo 50 caracteres",
  },

  descripcion: {
    maxLength: (value) =>
      !value || value.length <= 500 || "Máximo 500 caracteres",
  },
};

// Función para validar un campo
export const validateField = (value, fieldValidations) => {
  for (const validation of fieldValidations) {
    const result = validation(value);
    if (result !== true) {
      return result;
    }
  }
  return true;
};

// Función para validar un formulario completo
export const validateForm = (formData, validationRules) => {
  const errors = {};
  let isValid = true;

  Object.keys(validationRules).forEach((field) => {
    const fieldRules = validationRules[field];
    const value = formData[field];

    for (const rule of fieldRules) {
      const result = rule(value);
      if (result !== true) {
        errors[field] = result;
        isValid = false;
        break;
      }
    }
  });

  return { isValid, errors };
};
