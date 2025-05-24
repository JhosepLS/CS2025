<template>
  <div class="autores">
    <div class="container">
      <div class="page-header">
        <h1>👨‍💼 Gestión de Autores</h1>
        <button
          v-if="isAuthenticated"
          @click="openCreateModal"
          class="btn btn-primary"
        >
          ➕ Nuevo Autor
        </button>
      </div>

      <!-- Lista de autores -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>

      <div v-else-if="autores.length === 0" class="empty-state">
        <h3>No hay autores registrados</h3>
        <p>Comienza agregando tu primer autor</p>
      </div>

      <div v-else class="autores-grid">
        <div v-for="autor in autores" :key="autor.autor_id" class="autor-card">
          <div class="autor-info">
            <h3>{{ autor.autor_nombre }}</h3>
            <p v-if="autor.autor_pais">🌍 {{ autor.autor_pais }}</p>
            <p v-if="autor.anio_nacimiento">📅 {{ autor.anio_nacimiento }}</p>
          </div>

          <div class="autor-actions">
            <router-link
              :to="`/autor/${autor.autor_id}`"
              class="btn btn-sm btn-outline"
            >
              👁️ Ver Detalles
            </router-link>
            <button
              v-if="isAuthenticated"
              @click="openEditModal(autor)"
              class="btn btn-sm btn-warning"
            >
              ✏️ Editar
            </button>
            <button
              v-if="isAdmin"
              @click="confirmDelete(autor)"
              class="btn btn-sm btn-danger"
            >
              🗑️ Eliminar
            </button>
          </div>
        </div>
      </div>

      <!-- Modal para crear/editar autor -->
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal" @click.stop>
          <div class="modal-header">
            <h3>
              {{ modalMode === "create" ? "Nuevo Autor" : "Editar Autor" }}
            </h3>
            <button @click="closeModal" class="close-btn">&times;</button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="handleSubmit">
              <div class="form-group">
                <label for="autor_nombre">Nombre del Autor *</label>
                <input
                  id="autor_nombre"
                  v-model="form.autor_nombre"
                  type="text"
                  placeholder="Ej: Gabriel García Márquez"
                  :class="{ error: errors.autor_nombre }"
                  @blur="validateField('autor_nombre')"
                />
                <div v-if="errors.autor_nombre" class="error-message">
                  {{ errors.autor_nombre }}
                </div>
              </div>

              <div class="form-group">
                <label for="autor_pais">País</label>
                <input
                  id="autor_pais"
                  v-model="form.autor_pais"
                  type="text"
                  placeholder="Ej: Colombia"
                  :class="{ error: errors.autor_pais }"
                  @blur="validateField('autor_pais')"
                />
                <div v-if="errors.autor_pais" class="error-message">
                  {{ errors.autor_pais }}
                </div>
              </div>

              <div class="form-group">
                <label for="anio_nacimiento">Año de Nacimiento</label>
                <input
                  id="anio_nacimiento"
                  v-model="form.anio_nacimiento"
                  type="number"
                  placeholder="Ej: 1927"
                  min="0"
                  max="2100"
                  :class="{ error: errors.anio_nacimiento }"
                  @blur="validateField('anio_nacimiento')"
                />
                <div v-if="errors.anio_nacimiento" class="error-message">
                  {{ errors.anio_nacimiento }}
                </div>
              </div>
            </form>
          </div>

          <div class="modal-footer">
            <button @click="closeModal" class="btn btn-secondary">
              Cancelar
            </button>
            <button
              @click="handleSubmit"
              class="btn btn-primary"
              :disabled="modalLoading || !isFormValid"
            >
              {{ modalLoading ? "Guardando..." : "Guardar" }}
            </button>
          </div>
        </div>
      </div>

      <!-- Modal de confirmación de eliminación -->
      <div
        v-if="showDeleteModal"
        class="modal-overlay"
        @click="closeDeleteModal"
      >
        <div class="modal" @click.stop>
          <div class="modal-header">
            <h3>Confirmar Eliminación</h3>
            <button @click="closeDeleteModal" class="close-btn">&times;</button>
          </div>

          <div class="modal-body">
            <p>
              ¿Estás seguro de que deseas eliminar al autor
              <strong>{{ autorToDelete?.autor_nombre }}</strong
              >?
            </p>
            <p class="warning-text">Esta acción no se puede deshacer.</p>
          </div>

          <div class="modal-footer">
            <button @click="closeDeleteModal" class="btn btn-secondary">
              Cancelar
            </button>
            <button
              @click="handleDelete"
              class="btn btn-danger"
              :disabled="deleteLoading"
            >
              {{ deleteLoading ? "Eliminando..." : "Eliminar" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { autorService, authService } from "@/services/api";
import { validations, validateForm } from "@/utils/validations";
import { useToast } from "vue-toastification";

export default {
  name: "AutoresView",
  data() {
    return {
      autores: [],
      loading: false,
      showModal: false,
      modalMode: "create", // 'create' o 'edit'
      modalLoading: false,
      showDeleteModal: false,
      deleteLoading: false,
      autorToDelete: null,
      form: {
        autor_nombre: "",
        autor_pais: "",
        anio_nacimiento: null,
      },
      errors: {},
    };
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  computed: {
    isAuthenticated() {
      return !!authService.getToken();
    },
    isAdmin() {
      const user = authService.getUser();
      return user.role === "admin";
    },
    isFormValid() {
      return (
        this.form.autor_nombre.trim() && Object.keys(this.errors).length === 0
      );
    },
  },
  async mounted() {
    await this.loadAutores();
  },
  methods: {
    async loadAutores() {
      this.loading = true;
      try {
        const response = await autorService.getAll();
        this.autores = response.data;
      } catch (error) {
        console.error("Error loading autores:", error);
        this.toast.error("Error al cargar los autores");
      } finally {
        this.loading = false;
      }
    },

    openCreateModal() {
      this.modalMode = "create";
      this.resetForm();
      this.showModal = true;
    },

    openEditModal(autor) {
      this.modalMode = "edit";
      this.form = {
        autor_id: autor.autor_id,
        autor_nombre: autor.autor_nombre,
        autor_pais: autor.autor_pais || "",
        anio_nacimiento: autor.anio_nacimiento || null,
      };
      this.errors = {};
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.resetForm();
    },

    resetForm() {
      this.form = {
        autor_nombre: "",
        autor_pais: "",
        anio_nacimiento: null,
      };
      this.errors = {};
    },

    validateField(fieldName) {
      const fieldValidations = {
        autor_nombre: [
          validations.autorNombre.required,
          validations.autorNombre.minLength,
          validations.autorNombre.maxLength,
        ],
        autor_pais: [validations.autorPais.maxLength],
        anio_nacimiento: [
          validations.anioNacimiento.validYear,
          validations.anioNacimiento.numeric,
        ],
      };

      const rules = fieldValidations[fieldName];
      if (rules) {
        for (const rule of rules) {
          const result = rule(this.form[fieldName]);
          if (result !== true) {
            this.errors[fieldName] = result; // Asignación directa funciona en Vue 3
            return;
          }
        }
        delete this.errors[fieldName];
      }
    },

    validateForm() {
      const validationRules = {
        autor_nombre: [
          validations.autorNombre.required,
          validations.autorNombre.minLength,
          validations.autorNombre.maxLength,
        ],
        autor_pais: [validations.autorPais.maxLength],
        anio_nacimiento: [
          validations.anioNacimiento.validYear,
          validations.anioNacimiento.numeric,
        ],
      };

      const { isValid, errors } = validateForm(this.form, validationRules);
      this.errors = errors;
      return isValid;
    },

    async handleSubmit() {
      if (!this.validateForm()) {
        this.toast.error("Por favor corrige los errores del formulario");
        return;
      }

      this.modalLoading = true;
      try {
        const data = {
          nombre: this.form.autor_nombre,
          pais: this.form.autor_pais || null,
          anio: this.form.anio_nacimiento || null,
        };

        if (this.modalMode === "create") {
          await autorService.create(data);
          this.toast.success("Autor creado exitosamente");
        } else {
          await autorService.update(this.form.autor_id, data);
          this.toast.success("Autor actualizado exitosamente");
        }

        this.closeModal();
        await this.loadAutores();
      } catch (error) {
        console.error("Error saving autor:", error);
        const message =
          error.response?.data?.error || "Error al guardar el autor";
        this.toast.error(message);
      } finally {
        this.modalLoading = false;
      }
    },

    confirmDelete(autor) {
      this.autorToDelete = autor;
      this.showDeleteModal = true;
    },

    closeDeleteModal() {
      this.showDeleteModal = false;
      this.autorToDelete = null;
    },

    async handleDelete() {
      if (!this.autorToDelete) return;

      this.deleteLoading = true;
      try {
        await autorService.delete(this.autorToDelete.autor_id);
        this.toast.success("Autor eliminado exitosamente");
        this.closeDeleteModal();
        await this.loadAutores();
      } catch (error) {
        console.error("Error deleting autor:", error);
        const message =
          error.response?.data?.error || "Error al eliminar el autor";
        this.toast.error(message);
      } finally {
        this.deleteLoading = false;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 20px;

  h1 {
    color: var(--secondary-color);
    margin: 0;
  }
}

.autores-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
}

.autor-card {
  background: white;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: 25px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  }

  .autor-info {
    margin-bottom: 20px;

    h3 {
      color: var(--secondary-color);
      margin-bottom: 10px;
      font-size: 1.3rem;
    }

    p {
      color: #666;
      margin: 5px 0;
      font-size: 0.95rem;
    }
  }

  .autor-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;

    .btn {
      flex: 1;
      min-width: 100px;
    }
  }
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;

  h3 {
    margin-bottom: 10px;
    color: var(--secondary-color);
  }
}

.warning-text {
  color: var(--warning-color);
  font-style: italic;
  margin-top: 10px;
}

@media (max-width: 768px) {
  .autores-grid {
    grid-template-columns: 1fr;
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;

    .btn {
      width: 100%;
    }
  }

  .autor-actions {
    flex-direction: column;

    .btn {
      width: 100%;
    }
  }
}
</style>
