<template>
  <div class="libro-detail">
    <div class="container">
      <!-- Loading -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="alert alert-danger">
        <h3>Error</h3>
        <p>{{ error }}</p>
        <router-link to="/libros" class="btn btn-primary">
          Volver a Libros
        </router-link>
      </div>

      <!-- Contenido del libro -->
      <div v-else-if="libro" class="libro-content">
        <!-- Header -->
        <div class="libro-header">
          <div class="libro-info">
            <h1>{{ libro.libro.libro_titulo }}</h1>
            <div class="libro-meta">
              <span v-if="libro.libro.anio_publicacion" class="meta-item">
                📅 {{ libro.libro.anio_publicacion }}
              </span>
              <span v-if="libro.libro.genero_nombre" class="meta-item genero">
                🏷️ {{ libro.libro.genero_nombre }}
              </span>
            </div>
            <div
              v-if="libro.autores && libro.autores.length > 0"
              class="autores-info"
            >
              <h3>📝 Autores</h3>
              <div class="autores-list">
                <div
                  v-for="autor in libro.autores"
                  :key="autor.autor_id"
                  class="autor-item"
                >
                  <router-link
                    :to="`/autor/${autor.autor_id}`"
                    class="autor-link"
                  >
                    <strong>{{ autor.autor_nombre }}</strong>
                    <span v-if="autor.autor_pais" class="autor-country">
                      ({{ autor.autor_pais }})
                    </span>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
          <div class="libro-actions">
            <router-link to="/libros" class="btn btn-secondary">
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

        <!-- Información adicional -->
        <div class="additional-info">
          <div class="info-grid">
            <div class="info-card">
              <h3>📊 Detalles</h3>
              <div class="detail-item">
                <strong>Título:</strong>
                <span>{{ libro.libro.libro_titulo }}</span>
              </div>
              <div v-if="libro.libro.anio_publicacion" class="detail-item">
                <strong>Año de Publicación:</strong>
                <span>{{ libro.libro.anio_publicacion }}</span>
              </div>
              <div v-if="libro.libro.genero_nombre" class="detail-item">
                <strong>Género:</strong>
                <span>{{ libro.libro.genero_nombre }}</span>
              </div>
              <div class="detail-item">
                <strong>Número de Autores:</strong>
                <span>{{ libro.autores.length }}</span>
              </div>
            </div>

            <div class="info-card">
              <h3>🕒 Información del Sistema</h3>
              <div v-if="libro.libro.created_at" class="detail-item">
                <strong>Registrado:</strong>
                <span>{{ formatDate(libro.libro.created_at) }}</span>
              </div>
              <div v-if="libro.libro.updated_at" class="detail-item">
                <strong>Última Actualización:</strong>
                <span>{{ formatDate(libro.libro.updated_at) }}</span>
              </div>
              <div class="detail-item">
                <strong>Estado:</strong>
                <span class="status-badge">
                  {{ libro.libro.is_active ? "Activo" : "Inactivo" }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Otros libros del mismo género -->
        <div v-if="librosRelacionados.length > 0" class="related-books">
          <h2>📚 Otros libros de {{ libro.libro.genero_nombre }}</h2>
          <div class="related-grid">
            <div
              v-for="libroRel in librosRelacionados"
              :key="libroRel.libro_id"
              class="related-book"
            >
              <h4>{{ libroRel.libro_titulo }}</h4>
              <p v-if="libroRel.anio_publicacion">
                📅 {{ libroRel.anio_publicacion }}
              </p>
              <router-link
                :to="`/libro/${libroRel.libro_id}`"
                class="btn btn-sm btn-outline"
              >
                Ver Detalles
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal para editar libro -->
      <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
        <div class="modal libro-edit-modal" @click.stop>
          <div class="modal-header">
            <h3>Editar Libro</h3>
            <button @click="closeEditModal" class="close-btn">&times;</button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="handleEdit">
              <div class="form-group">
                <label for="libro_titulo">Título del Libro *</label>
                <input
                  id="libro_titulo"
                  v-model="editForm.libro_titulo"
                  type="text"
                  placeholder="Ej: Cien años de soledad"
                  :class="{ error: editErrors.libro_titulo }"
                  @blur="validateEditField('libro_titulo')"
                />
                <div v-if="editErrors.libro_titulo" class="error-message">
                  {{ editErrors.libro_titulo }}
                </div>
              </div>

              <div class="form-group">
                <label for="anio_publicacion">Año de Publicación</label>
                <input
                  id="anio_publicacion"
                  v-model="editForm.anio_publicacion"
                  type="number"
                  placeholder="Ej: 1967"
                  min="0"
                  max="2100"
                  :class="{ error: editErrors.anio_publicacion }"
                  @blur="validateEditField('anio_publicacion')"
                />
                <div v-if="editErrors.anio_publicacion" class="error-message">
                  {{ editErrors.anio_publicacion }}
                </div>
              </div>

              <div class="form-group">
                <label for="genero_id">Género *</label>
                <select
                  id="genero_id"
                  v-model="editForm.genero_id"
                  :class="{ error: editErrors.genero_id }"
                  @change="validateEditField('genero_id')"
                >
                  <option value="">Selecciona un género</option>
                  <option
                    v-for="genero in generos"
                    :key="genero.genero_id"
                    :value="genero.genero_id"
                  >
                    {{ genero.genero_nombre }}
                  </option>
                </select>
                <div v-if="editErrors.genero_id" class="error-message">
                  {{ editErrors.genero_id }}
                </div>
              </div>

              <div class="form-group">
                <label>Autores *</label>
                <div class="authors-selection">
                  <div
                    v-for="autor in autores"
                    :key="autor.autor_id"
                    class="author-checkbox"
                  >
                    <label class="checkbox-label">
                      <input
                        v-model="editForm.autores_ids"
                        type="checkbox"
                        :value="autor.autor_id"
                        @change="validateEditField('autores_ids')"
                      />
                      <span class="checkbox-text">{{
                        autor.autor_nombre
                      }}</span>
                      <span v-if="autor.autor_pais" class="author-country">
                        ({{ autor.autor_pais }})
                      </span>
                    </label>
                  </div>
                </div>
                <div v-if="editErrors.autores_ids" class="error-message">
                  {{ editErrors.autores_ids }}
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
              ¿Estás seguro de que deseas eliminar el libro
              <strong>{{ libro?.libro?.libro_titulo }}</strong
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
import {
  libroService,
  autorService,
  generoService,
  authService,
} from "@/services/api";
import { validations, validateForm } from "@/utils/validations";
import { useToast } from "vue-toastification";

export default {
  name: "LibroDetailView",
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      libro: null,
      librosRelacionados: [],
      autores: [],
      generos: [],
      loading: false,
      error: null,
      showEditModal: false,
      editLoading: false,
      showDeleteModal: false,
      deleteLoading: false,
      editForm: {
        libro_titulo: "",
        anio_publicacion: null,
        genero_id: "",
        autores_ids: [],
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
        this.editForm.libro_titulo.trim() &&
        this.editForm.genero_id &&
        this.editForm.autores_ids.length > 0 &&
        Object.keys(this.editErrors).length === 0
      );
    },
  },
  async mounted() {
    await this.loadLibro();
    await this.loadAutores();
    await this.loadGeneros();
    await this.loadLibrosRelacionados();
  },
  methods: {
    async loadLibro() {
      this.loading = true;
      this.error = null;
      try {
        const response = await libroService.getById(this.id);
        this.libro = response.data;
      } catch (error) {
        console.error("Error loading libro:", error);
        this.error = error.response?.data?.error || "Error al cargar el libro";
      } finally {
        this.loading = false;
      }
    },

    async loadAutores() {
      try {
        const response = await autorService.getAll();
        this.autores = response.data;
      } catch (error) {
        console.error("Error loading autores:", error);
      }
    },

    async loadGeneros() {
      try {
        const response = await generoService.getAll();
        this.generos = response.data;
      } catch (error) {
        console.error("Error loading generos:", error);
      }
    },

    async loadLibrosRelacionados() {
      if (!this.libro?.libro?.genero_id) return;

      try {
        const response = await libroService.getAll();
        this.librosRelacionados = response.data
          .filter(
            (lib) =>
              lib.genero_id === this.libro.libro.genero_id &&
              lib.libro_id !== parseInt(this.id)
          )
          .slice(0, 4); // Máximo 4 libros relacionados
      } catch (error) {
        console.error("Error loading related books:", error);
      }
    },

    formatDate(dateString) {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      return date.toLocaleDateString("es-ES", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },

    openEditModal() {
      this.editForm = {
        libro_titulo: this.libro.libro.libro_titulo,
        anio_publicacion: this.libro.libro.anio_publicacion || null,
        genero_id: this.libro.libro.genero_id,
        autores_ids: this.libro.autores.map((autor) => autor.autor_id),
      };
      this.editErrors = {};
      this.showEditModal = true;
    },

    closeEditModal() {
      this.showEditModal = false;
      this.editForm = {
        libro_titulo: "",
        anio_publicacion: null,
        genero_id: "",
        autores_ids: [],
      };
      this.editErrors = {};
    },

    validateEditField(fieldName) {
      const fieldValidations = {
        libro_titulo: [
          validations.libroTitulo.required,
          validations.libroTitulo.minLength,
          validations.libroTitulo.maxLength,
        ],
        anio_publicacion: [
          validations.anioPublicacion.validYear,
          validations.anioPublicacion.numeric,
        ],
        genero_id: [validations.generoId.required],
        autores_ids: [validations.autoresIds.required],
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
        libro_titulo: [
          validations.libroTitulo.required,
          validations.libroTitulo.minLength,
          validations.libroTitulo.maxLength,
        ],
        anio_publicacion: [
          validations.anioPublicacion.validYear,
          validations.anioPublicacion.numeric,
        ],
        genero_id: [validations.generoId.required],
        autores_ids: [validations.autoresIds.required],
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
          titulo: this.editForm.libro_titulo,
          anio: this.editForm.anio_publicacion || null,
          genero_id: parseInt(this.editForm.genero_id),
          autores_ids: this.editForm.autores_ids.map((id) => parseInt(id)),
        };

        await libroService.update(this.id, data);
        this.toast.success("Libro actualizado exitosamente");
        this.closeEditModal();
        await this.loadLibro();
        await this.loadLibrosRelacionados();
      } catch (error) {
        console.error("Error updating libro:", error);
        const message =
          error.response?.data?.error || "Error al actualizar el libro";
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
        await libroService.delete(this.id);
        this.toast.success("Libro eliminado exitosamente");
        this.$router.push("/libros");
      } catch (error) {
        console.error("Error deleting libro:", error);
        const message =
          error.response?.data?.error || "Error al eliminar el libro";
        this.toast.error(message);
      } finally {
        this.deleteLoading = false;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.libro-header {
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

  .libro-info {
    flex: 1;

    h1 {
      color: var(--secondary-color);
      margin-bottom: 15px;
      font-size: 2.5rem;
      line-height: 1.2;

      @media (max-width: 768px) {
        font-size: 2rem;
      }
    }

    .libro-meta {
      display: flex;
      gap: 15px;
      margin-bottom: 25px;
      flex-wrap: wrap;

      .meta-item {
        background-color: var(--light-color);
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        color: var(--secondary-color);
        border: 1px solid var(--border-color);

        &.genero {
          background-color: var(--primary-color);
          color: white;
          border-color: var(--primary-color);
        }
      }
    }

    .autores-info {
      h3 {
        color: var(--secondary-color);
        margin-bottom: 15px;
        font-size: 1.3rem;
      }

      .autores-list {
        display: flex;
        flex-direction: column;
        gap: 10px;

        .autor-item {
          .autor-link {
            display: inline-block;
            padding: 10px 15px;
            background-color: var(--light-color);
            border-radius: var(--border-radius);
            text-decoration: none;
            color: var(--secondary-color);
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;

            &:hover {
              background-color: var(--primary-color);
              color: white;
              border-color: var(--primary-color);
            }

            .autor-country {
              margin-left: 8px;
              opacity: 0.8;
            }
          }
        }
      }
    }
  }

  .libro-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;

    @media (max-width: 768px) {
      flex-direction: column;
    }
  }
}

.additional-info {
  margin-bottom: 40px;

  .info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 25px;

    .info-card {
      background: white;
      padding: 25px;
      border-radius: var(--border-radius);
      box-shadow: var(--shadow);

      h3 {
        color: var(--secondary-color);
        margin-bottom: 20px;
        font-size: 1.3rem;
        border-bottom: 2px solid var(--light-color);
        padding-bottom: 10px;
      }

      .detail-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        padding: 10px 0;
        border-bottom: 1px solid #f0f0f0;

        &:last-child {
          margin-bottom: 0;
          border-bottom: none;
        }

        strong {
          color: var(--secondary-color);
          flex: 1;
        }

        span {
          color: #666;
          text-align: right;
        }

        .status-badge {
          background-color: var(--success-color);
          color: white;
          padding: 4px 12px;
          border-radius: 15px;
          font-size: 0.85rem;
          font-weight: 500;
        }
      }
    }
  }
}

.related-books {
  h2 {
    color: var(--secondary-color);
    margin-bottom: 25px;
    font-size: 1.8rem;
  }

  .related-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;

    .related-book {
      background: white;
      padding: 20px;
      border-radius: var(--border-radius);
      box-shadow: var(--shadow);
      text-align: center;
      transition: transform 0.3s ease;

      &:hover {
        transform: translateY(-3px);
      }

      h4 {
        color: var(--secondary-color);
        margin-bottom: 10px;
        font-size: 1.1rem;
        line-height: 1.3;
      }

      p {
        color: #666;
        margin-bottom: 15px;
        font-size: 0.9rem;
      }
    }
  }
}

.libro-edit-modal {
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;

  .authors-selection {
    max-height: 200px;
    overflow-y: auto;
    border: 2px solid var(--border-color);
    border-radius: var(--border-radius);
    padding: 15px;
    background-color: #fafafa;

    .author-checkbox {
      margin-bottom: 10px;

      .checkbox-label {
        display: flex;
        align-items: center;
        cursor: pointer;
        padding: 8px;
        border-radius: var(--border-radius);
        transition: background-color 0.2s ease;

        &:hover {
          background-color: var(--light-color);
        }

        input[type="checkbox"] {
          margin-right: 10px;
          width: auto;
        }

        .checkbox-text {
          font-weight: 500;
          color: var(--secondary-color);
        }

        .author-country {
          margin-left: 8px;
          color: #666;
          font-size: 0.9rem;
        }
      }
    }
  }
}

.warning-text {
  color: var(--warning-color);
  font-style: italic;
  margin-top: 10px;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .related-grid {
    grid-template-columns: 1fr;
  }

  .autores-list {
    .autor-item {
      .autor-link {
        display: block;
        text-align: center;
      }
    }
  }
}
</style>
