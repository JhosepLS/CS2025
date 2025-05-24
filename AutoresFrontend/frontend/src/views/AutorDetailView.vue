<template>
  <div class="autor-detail">
    <div class="container">
      <!-- Loading -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="alert alert-danger">
        <h3>Error</h3>
        <p>{{ error }}</p>
        <router-link to="/autores" class="btn btn-primary">
          Volver a Autores
        </router-link>
      </div>

      <!-- Contenido del autor -->
      <div v-else-if="autor" class="autor-content">
        <!-- Header -->
        <div class="autor-header">
          <div class="autor-info">
            <h1>{{ autor.autor_nombre }}</h1>
            <div class="autor-meta">
              <span v-if="autor.autor_pais" class="meta-item">
                🌍 {{ autor.autor_pais }}
              </span>
              <span v-if="autor.anio_nacimiento" class="meta-item">
                📅 {{ autor.anio_nacimiento }}
              </span>
            </div>
          </div>
          <div class="autor-actions">
            <router-link to="/autores" class="btn btn-secondary">
              ← Volver
            </router-link>
            <button
              v-if="isAuthenticated"
              @click="openEditModal"
              class="btn btn-warning"
            >
              ✏️ Editar
            </button>
            <button
              v-if="isAdmin"
              @click="confirmDelete"
              class="btn btn-danger"
            >
              🗑️ Eliminar
            </button>
          </div>
        </div>

        <!-- Libros del autor -->
        <div class="libros-section">
          <h2>📚 Libros de {{ autor.autor_nombre }}</h2>

          <div v-if="loadingLibros" class="loading">
            <div class="spinner"></div>
          </div>

          <div v-else-if="libros.length === 0" class="empty-state">
            <p>Este autor no tiene libros registrados.</p>
            <router-link
              v-if="isAuthenticated"
              to="/libros"
              class="btn btn-primary"
            >
              Agregar Libro
            </router-link>
          </div>

          <div v-else class="libros-grid">
            <div
              v-for="libro in libros"
              :key="libro.libro_id"
              class="libro-card"
            >
              <h3>{{ libro.libro_titulo }}</h3>
              <div class="libro-meta">
                <span v-if="libro.anio_publicacion" class="meta-item">
                  📅 {{ libro.anio_publicacion }}
                </span>
                <span v-if="libro.genero_nombre" class="meta-item">
                  🏷️ {{ libro.genero_nombre }}
                </span>
              </div>
              <div class="libro-actions">
                <router-link
                  :to="`/libro/${libro.libro_id}`"
                  class="btn btn-sm btn-outline"
                >
                  Ver Detalles
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal para editar autor -->
      <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
        <div class="modal" @click.stop>
          <div class="modal-header">
            <h3>Editar Autor</h3>
            <button @click="closeEditModal" class="close-btn">&times;</button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="handleEdit">
              <div class="form-group">
                <label for="autor_nombre">Nombre del Autor *</label>
                <input
                  id="autor_nombre"
                  v-model="editForm.autor_nombre"
                  type="text"
                  placeholder="Ej: Gabriel García Márquez"
                  :class="{ error: editErrors.autor_nombre }"
                  @blur="validateEditField('autor_nombre')"
                />
                <div v-if="editErrors.autor_nombre" class="error-message">
                  {{ editErrors.autor_nombre }}
                </div>
              </div>

              <div class="form-group">
                <label for="autor_pais">País</label>
                <input
                  id="autor_pais"
                  v-model="editForm.autor_pais"
                  type="text"
                  placeholder="Ej: Colombia"
                  :class="{ error: editErrors.autor_pais }"
                  @blur="validateEditField('autor_pais')"
                />
                <div v-if="editErrors.autor_pais" class="error-message">
                  {{ editErrors.autor_pais }}
                </div>
              </div>

              <div class="form-group">
                <label for="anio_nacimiento">Año de Nacimiento</label>
                <input
                  id="anio_nacimiento"
                  v-model="editForm.anio_nacimiento"
                  type="number"
                  placeholder="Ej: 1927"
                  min="0"
                  max="2100"
                  :class="{ error: editErrors.anio_nacimiento }"
                  @blur="validateEditField('anio_nacimiento')"
                />
                <div v-if="editErrors.anio_nacimiento" class="error-message">
                  {{ editErrors.anio_nacimiento }}
                </div>
              </div>
            </form>
          </div>

          <div class="modal-footer">
            <button @click="closeEditModal" class="btn btn-secondary">
              Cancelar
            </button>
            <button
              @click="handleEdit"
              class="btn btn-primary"
              :disabled="editLoading || !isEditFormValid"
            >
              {{ editLoading ? "Guardando..." : "Guardar" }}
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
              <strong>{{ autor?.autor_nombre }}</strong
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
  name: "AutorDetailView",
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      autor: null,
      libros: [],
      loading: false,
      loadingLibros: false,
      error: null,
      showEditModal: false,
      editLoading: false,
      showDeleteModal: false,
      deleteLoading: false,
      editForm: {
        autor_nombre: "",
        autor_pais: "",
        anio_nacimiento: null,
      },
      editErrors: {},
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
    isEditFormValid() {
      return (
        this.editForm.autor_nombre.trim() &&
        Object.keys(this.editErrors).length === 0
      );
    },
  },
  async mounted() {
    await this.loadAutor();
    await this.loadLibros();
  },
  methods: {
    async loadAutor() {
      this.loading = true;
      this.error = null;
      try {
        const response = await autorService.getById(this.id);
        this.autor = response.data[0];
      } catch (error) {
        console.error("Error loading autor:", error);
        this.error = error.response?.data?.error || "Error al cargar el autor";
      } finally {
        this.loading = false;
      }
    },

    async loadLibros() {
      this.loadingLibros = true;
      try {
        const response = await autorService.getLibros(this.id);
        this.libros = response.data.libros || [];
      } catch (error) {
        console.error("Error loading libros:", error);
        this.toast.error("Error al cargar los libros del autor");
      } finally {
        this.loadingLibros = false;
      }
    },

    openEditModal() {
      this.editForm = {
        autor_nombre: this.autor.autor_nombre,
        autor_pais: this.autor.autor_pais || "",
        anio_nacimiento: this.autor.anio_nacimiento || null,
      };
      this.editErrors = {};
      this.showEditModal = true;
    },

    closeEditModal() {
      this.showEditModal = false;
      this.editForm = {
        autor_nombre: "",
        autor_pais: "",
        anio_nacimiento: null,
      };
      this.editErrors = {};
    },

    validateEditField(fieldName) {
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
          const result = rule(this.editForm[fieldName]);
          if (result !== true) {
            this.editErrors[fieldName] = result;
            return;
          }
        }
        delete this.editErrors[fieldName];
      }
    },

    validateEditForm() {
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

      const { isValid, errors } = validateForm(this.editForm, validationRules);
      this.editErrors = errors;
      return isValid;
    },

    async handleEdit() {
      if (!this.validateEditForm()) {
        this.toast.error("Por favor corrige los errores del formulario");
        return;
      }

      this.editLoading = true;
      try {
        const data = {
          nombre: this.editForm.autor_nombre,
          pais: this.editForm.autor_pais || null,
          anio: this.editForm.anio_nacimiento || null,
        };

        await autorService.update(this.id, data);
        this.toast.success("Autor actualizado exitosamente");
        this.closeEditModal();
        await this.loadAutor();
      } catch (error) {
        console.error("Error updating autor:", error);
        const message =
          error.response?.data?.error || "Error al actualizar el autor";
        this.toast.error(message);
      } finally {
        this.editLoading = false;
      }
    },

    confirmDelete() {
      this.showDeleteModal = true;
    },

    closeDeleteModal() {
      this.showDeleteModal = false;
    },

    async handleDelete() {
      this.deleteLoading = true;
      try {
        await autorService.delete(this.id);
        this.toast.success("Autor eliminado exitosamente");
        this.$router.push("/autores");
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
.autor-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 40px;
  padding: 30px;
  background: white;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  gap: 20px;

  @media (max-width: 768px) {
    flex-direction: column;
    align-items: stretch;
  }

  .autor-info {
    flex: 1;

    h1 {
      color: var(--secondary-color);
      margin-bottom: 15px;
      font-size: 2.5rem;

      @media (max-width: 768px) {
        font-size: 2rem;
      }
    }

    .autor-meta {
      display: flex;
      gap: 20px;
      flex-wrap: wrap;

      .meta-item {
        background-color: var(--light-color);
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        color: var(--secondary-color);
        border: 1px solid var(--border-color);
      }
    }
  }

  .autor-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;

    @media (max-width: 768px) {
      flex-direction: column;
    }
  }
}

.libros-section {
  h2 {
    color: var(--secondary-color);
    margin-bottom: 30px;
    font-size: 1.8rem;
    padding-left: 5px;
  }
}

.libros-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 25px;
}

.libro-card {
  background: white;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: 25px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  }

  h3 {
    color: var(--secondary-color);
    margin-bottom: 15px;
    font-size: 1.2rem;
    line-height: 1.4;
  }

  .libro-meta {
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
    flex-wrap: wrap;

    .meta-item {
      background-color: var(--light-color);
      padding: 5px 12px;
      border-radius: 15px;
      font-size: 0.85rem;
      color: var(--secondary-color);
      border: 1px solid var(--border-color);
    }
  }

  .libro-actions {
    display: flex;
    gap: 10px;
  }
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);

  p {
    color: #666;
    margin-bottom: 20px;
    font-size: 1.1rem;
  }
}

.warning-text {
  color: var(--warning-color);
  font-style: italic;
  margin-top: 10px;
}

@media (max-width: 768px) {
  .libros-grid {
    grid-template-columns: 1fr;
  }

  .autor-meta {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
