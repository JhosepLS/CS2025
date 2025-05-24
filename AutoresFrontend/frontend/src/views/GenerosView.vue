<template>
  <div class="generos">
    <div class="container">
      <div class="page-header">
        <h1>🏷️ Gestión de Géneros</h1>
        <button v-if="isAdmin" @click="openCreateModal" class="btn btn-primary">
          ➕ Nuevo Género
        </button>
      </div>

      <!-- Mensaje de permisos -->
      <div v-if="!isAuthenticated" class="alert alert-info">
        <p>
          <strong>Información:</strong> Debes iniciar sesión para gestionar
          géneros.
        </p>
      </div>

      <div v-else-if="!isAdmin" class="alert alert-warning">
        <p>
          <strong>Acceso Restringido:</strong> Solo los administradores pueden
          gestionar géneros.
        </p>
      </div>

      <!-- Lista de géneros -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>

      <div v-else-if="generos.length === 0" class="empty-state">
        <h3>No hay géneros registrados</h3>
        <p>Comienza agregando tu primer género</p>
      </div>

      <div v-else class="generos-grid">
        <div
          v-for="genero in generos"
          :key="genero.genero_id"
          class="genero-card"
        >
          <div class="genero-info">
            <h3>{{ genero.genero_nombre }}</h3>
            <p v-if="genero.descripcion" class="descripcion">
              {{ genero.descripcion }}
            </p>
            <p v-else class="no-descripcion">Sin descripción disponible</p>
            <div class="genero-meta">
              <span class="meta-item">
                📅 Creado: {{ formatDate(genero.created_at) }}
              </span>
              <span
                v-if="genero.updated_at !== genero.created_at"
                class="meta-item"
              >
                🔄 Actualizado: {{ formatDate(genero.updated_at) }}
              </span>
            </div>
          </div>

          <div class="genero-actions">
            <button
              @click="loadLibrosByGenero(genero)"
              class="btn btn-sm btn-outline"
            >
              📚 Ver Libros
            </button>
            <button
              v-if="isAdmin"
              @click="openEditModal(genero)"
              class="btn btn-sm btn-warning"
            >
              ✏️ Editar
            </button>
            <button
              v-if="isAdmin"
              @click="confirmDelete(genero)"
              class="btn btn-sm btn-danger"
            >
              🗑️ Eliminar
            </button>
          </div>
        </div>
      </div>

      <!-- Modal para crear/editar género -->
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal" @click.stop>
          <div class="modal-header">
            <h3>
              {{ modalMode === "create" ? "Nuevo Género" : "Editar Género" }}
            </h3>
            <button @click="closeModal" class="close-btn">&times;</button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="handleSubmit">
              <div class="form-group">
                <label for="genero_nombre">Nombre del Género *</label>
                <input
                  id="genero_nombre"
                  v-model="form.genero_nombre"
                  type="text"
                  placeholder="Ej: Ciencia Ficción"
                  :class="{ error: errors.genero_nombre }"
                  @blur="validateField('genero_nombre')"
                />
                <div v-if="errors.genero_nombre" class="error-message">
                  {{ errors.genero_nombre }}
                </div>
              </div>

              <div class="form-group">
                <label for="descripcion">Descripción</label>
                <textarea
                  id="descripcion"
                  v-model="form.descripcion"
                  placeholder="Describe las características de este género..."
                  rows="4"
                  :class="{ error: errors.descripcion }"
                  @blur="validateField('descripcion')"
                ></textarea>
                <div v-if="errors.descripcion" class="error-message">
                  {{ errors.descripcion }}
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
              ¿Estás seguro de que deseas eliminar el género
              <strong>{{ generoToDelete?.genero_nombre }}</strong
              >?
            </p>
            <p class="warning-text">
              Esta acción no se puede deshacer. Solo se puede eliminar si no
              tiene libros asociados.
            </p>
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

      <!-- Modal para mostrar libros del género -->
      <div
        v-if="showLibrosModal"
        class="modal-overlay"
        @click="closeLibrosModal"
      >
        <div class="modal libros-modal" @click.stop>
          <div class="modal-header">
            <h3>📚 Libros de {{ selectedGenero?.genero_nombre }}</h3>
            <button @click="closeLibrosModal" class="close-btn">&times;</button>
          </div>

          <div class="modal-body">
            <div v-if="loadingLibros" class="loading">
              <div class="spinner"></div>
            </div>

            <div v-else-if="librosDelGenero.length === 0" class="empty-state">
              <p>No hay libros registrados en este género.</p>
            </div>

            <div v-else class="libros-list">
              <div
                v-for="libro in librosDelGenero"
                :key="libro.libro_id"
                class="libro-item"
              >
                <div class="libro-info">
                  <h4>{{ libro.libro_titulo }}</h4>
                  <p v-if="libro.anio_publicacion">
                    📅 {{ libro.anio_publicacion }}
                  </p>
                  <div
                    v-if="libro.autores && libro.autores.length > 0"
                    class="autores"
                  >
                    <strong>Autores:</strong>
                    <span
                      v-for="(autor, index) in libro.autores"
                      :key="autor.autor_id"
                    >
                      {{ autor.autor_nombre
                      }}{{ index < libro.autores.length - 1 ? ", " : "" }}
                    </span>
                  </div>
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

          <div class="modal-footer">
            <button @click="closeLibrosModal" class="btn btn-secondary">
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { generoService, libroService, authService } from "@/services/api";
import { validations, validateForm } from "@/utils/validations";
import { useToast } from "vue-toastification";

export default {
  name: "GenerosView",
  data() {
    return {
      generos: [],
      loading: false,
      showModal: false,
      modalMode: "create", // 'create' o 'edit'
      modalLoading: false,
      showDeleteModal: false,
      deleteLoading: false,
      generoToDelete: null,
      showLibrosModal: false,
      loadingLibros: false,
      selectedGenero: null,
      librosDelGenero: [],
      form: {
        genero_nombre: "",
        descripcion: "",
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
        this.form.genero_nombre.trim() && Object.keys(this.errors).length === 0
      );
    },
  },
  async mounted() {
    await this.loadGeneros();
  },
  methods: {
    async loadGeneros() {
      this.loading = true;
      try {
        const response = await generoService.getAll();
        this.generos = response.data;
      } catch (error) {
        console.error("Error loading generos:", error);
        this.toast.error("Error al cargar los géneros");
      } finally {
        this.loading = false;
      }
    },

    formatDate(dateString) {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      return date.toLocaleDateString("es-ES", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    },

    openCreateModal() {
      this.modalMode = "create";
      this.resetForm();
      this.showModal = true;
    },

    openEditModal(genero) {
      this.modalMode = "edit";
      this.form = {
        genero_id: genero.genero_id,
        genero_nombre: genero.genero_nombre,
        descripcion: genero.descripcion || "",
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
        genero_nombre: "",
        descripcion: "",
      };
      this.errors = {};
    },

    validateField(fieldName) {
      const fieldValidations = {
        genero_nombre: [
          validations.generoNombre.required,
          validations.generoNombre.minLength,
          validations.generoNombre.maxLength,
        ],
        descripcion: [validations.descripcion.maxLength],
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
        genero_nombre: [
          validations.generoNombre.required,
          validations.generoNombre.minLength,
          validations.generoNombre.maxLength,
        ],
        descripcion: [validations.descripcion.maxLength],
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
          nombre: this.form.genero_nombre,
          descripcion: this.form.descripcion || null,
        };

        if (this.modalMode === "create") {
          await generoService.create(data);
          this.toast.success("Género creado exitosamente");
        } else {
          await generoService.update(this.form.genero_id, data);
          this.toast.success("Género actualizado exitosamente");
        }

        this.closeModal();
        await this.loadGeneros();
      } catch (error) {
        console.error("Error saving genero:", error);
        const message =
          error.response?.data?.error || "Error al guardar el género";
        this.toast.error(message);
      } finally {
        this.modalLoading = false;
      }
    },

    confirmDelete(genero) {
      this.generoToDelete = genero;
      this.showDeleteModal = true;
    },

    closeDeleteModal() {
      this.showDeleteModal = false;
      this.generoToDelete = null;
    },

    async handleDelete() {
      if (!this.generoToDelete) return;

      this.deleteLoading = true;
      try {
        await generoService.delete(this.generoToDelete.genero_id);
        this.toast.success("Género eliminado exitosamente");
        this.closeDeleteModal();
        await this.loadGeneros();
      } catch (error) {
        console.error("Error deleting genero:", error);
        const message =
          error.response?.data?.error || "Error al eliminar el género";
        this.toast.error(message);
      } finally {
        this.deleteLoading = false;
      }
    },

    async loadLibrosByGenero(genero) {
      this.selectedGenero = genero;
      this.showLibrosModal = true;
      this.loadingLibros = true;

      try {
        const response = await libroService.getAll();
        this.librosDelGenero = response.data.filter(
          (libro) => libro.genero_id === genero.genero_id
        );
      } catch (error) {
        console.error("Error loading libros del genero:", error);
        this.toast.error("Error al cargar los libros del género");
      } finally {
        this.loadingLibros = false;
      }
    },

    closeLibrosModal() {
      this.showLibrosModal = false;
      this.selectedGenero = null;
      this.librosDelGenero = [];
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

.generos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 25px;
}

.genero-card {
  background: white;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: 25px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-left: 4px solid var(--primary-color);

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  }

  .genero-info {
    margin-bottom: 20px;

    h3 {
      color: var(--secondary-color);
      margin-bottom: 12px;
      font-size: 1.4rem;
    }

    .descripcion {
      color: #666;
      line-height: 1.5;
      margin-bottom: 15px;
      font-style: italic;
    }

    .no-descripcion {
      color: #999;
      font-style: italic;
      margin-bottom: 15px;
    }

    .genero-meta {
      display: flex;
      flex-direction: column;
      gap: 5px;

      .meta-item {
        background-color: var(--light-color);
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        color: var(--secondary-color);
        border: 1px solid var(--border-color);
        width: fit-content;
      }
    }
  }

  .genero-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;

    .btn {
      flex: 1;
      min-width: 100px;
    }
  }
}

.libros-modal {
  max-width: 700px;
  max-height: 80vh;

  .libros-list {
    max-height: 400px;
    overflow-y: auto;

    .libro-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 15px;
      border: 1px solid var(--border-color);
      border-radius: var(--border-radius);
      margin-bottom: 15px;
      background-color: #fafafa;
      transition: background-color 0.3s ease;

      &:hover {
        background-color: var(--light-color);
      }

      &:last-child {
        margin-bottom: 0;
      }

      .libro-info {
        flex: 1;

        h4 {
          color: var(--secondary-color);
          margin-bottom: 8px;
          font-size: 1.1rem;
        }

        p {
          color: #666;
          margin: 5px 0;
          font-size: 0.9rem;
        }

        .autores {
          color: #666;
          font-size: 0.9rem;

          strong {
            color: var(--secondary-color);
          }
        }
      }

      .libro-actions {
        margin-left: 15px;
      }
    }
  }
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);

  h3 {
    margin-bottom: 15px;
    color: var(--secondary-color);
  }

  p {
    color: #666;
    margin-bottom: 20px;
  }
}

.warning-text {
  color: var(--warning-color);
  font-style: italic;
  margin-top: 10px;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .generos-grid {
    grid-template-columns: 1fr;
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;

    .btn {
      width: 100%;
    }
  }

  .genero-actions {
    flex-direction: column;

    .btn {
      width: 100%;
    }
  }

  .libro-item {
    flex-direction: column;
    align-items: stretch;
    text-align: center;

    .libro-actions {
      margin-left: 0;
      margin-top: 15px;
    }
  }
}
</style>
