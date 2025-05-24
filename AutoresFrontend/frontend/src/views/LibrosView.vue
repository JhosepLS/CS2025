<template>
  <div class="libros">
    <div class="container">
      <div class="page-header">
        <h1>📚 Gestión de Libros</h1>
        <button
          v-if="isAuthenticated"
          @click="openCreateModal"
          class="btn btn-primary"
        >
          ➕ Nuevo Libro
        </button>
      </div>

      <!-- Filtros -->
      <div class="filters-section">
        <div class="filters">
          <div class="filter-group">
            <label>Buscar por título:</label>
            <input
              v-model="searchTerm"
              type="text"
              placeholder="Buscar libros..."
              class="search-input"
            />
          </div>
          <div class="filter-group">
            <label>Filtrar por género:</label>
            <select v-model="selectedGenero" class="filter-select">
              <option value="">Todos los géneros</option>
              <option
                v-for="genero in generos"
                :key="genero.genero_id"
                :value="genero.genero_id"
              >
                {{ genero.genero_nombre }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Lista de libros -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>

      <div v-else-if="filteredLibros.length === 0" class="empty-state">
        <h3>No hay libros registrados</h3>
        <p>
          {{
            searchTerm || selectedGenero
              ? "No se encontraron libros con los filtros aplicados"
              : "Comienza agregando tu primer libro"
          }}
        </p>
        <button
          v-if="searchTerm || selectedGenero"
          @click="clearFilters"
          class="btn btn-secondary"
        >
          Limpiar Filtros
        </button>
      </div>

      <div v-else class="libros-grid">
        <div
          v-for="libro in filteredLibros"
          :key="libro.libro_id"
          class="libro-card"
        >
          <div class="libro-info">
            <h3>{{ libro.libro_titulo }}</h3>
            <div class="libro-meta">
              <span v-if="libro.anio_publicacion" class="meta-item">
                📅 {{ libro.anio_publicacion }}
              </span>
              <span v-if="libro.genero_nombre" class="meta-item genero">
                🏷️ {{ libro.genero_nombre }}
              </span>
            </div>
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
              👁️ Ver Detalles
            </router-link>
            <button
              v-if="isAuthenticated"
              @click="openEditModal(libro)"
              class="btn btn-sm btn-warning"
            >
              ✏️ Editar
            </button>
            <button
              v-if="isAdmin"
              @click="confirmDelete(libro)"
              class="btn btn-sm btn-danger"
            >
              🗑️ Eliminar
            </button>
          </div>
        </div>
      </div>

      <!-- Modal para crear/editar libro -->
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal libro-modal" @click.stop>
          <div class="modal-header">
            <h3>
              {{ modalMode === "create" ? "Nuevo Libro" : "Editar Libro" }}
            </h3>
            <button @click="closeModal" class="close-btn">&times;</button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="handleSubmit">
              <div class="form-group">
                <label for="libro_titulo">Título del Libro *</label>
                <input
                  id="libro_titulo"
                  v-model="form.libro_titulo"
                  type="text"
                  placeholder="Ej: Cien años de soledad"
                  :class="{ error: errors.libro_titulo }"
                  @blur="validateField('libro_titulo')"
                />
                <div v-if="errors.libro_titulo" class="error-message">
                  {{ errors.libro_titulo }}
                </div>
              </div>

              <div class="form-group">
                <label for="anio_publicacion">Año de Publicación</label>
                <input
                  id="anio_publicacion"
                  v-model="form.anio_publicacion"
                  type="number"
                  placeholder="Ej: 1967"
                  min="0"
                  max="2100"
                  :class="{ error: errors.anio_publicacion }"
                  @blur="validateField('anio_publicacion')"
                />
                <div v-if="errors.anio_publicacion" class="error-message">
                  {{ errors.anio_publicacion }}
                </div>
              </div>

              <div class="form-group">
                <label for="genero_id">Género *</label>
                <select
                  id="genero_id"
                  v-model="form.genero_id"
                  :class="{ error: errors.genero_id }"
                  @change="validateField('genero_id')"
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
                <div v-if="errors.genero_id" class="error-message">
                  {{ errors.genero_id }}
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
                        v-model="form.autores_ids"
                        type="checkbox"
                        :value="autor.autor_id"
                        @change="validateField('autores_ids')"
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
                <div v-if="errors.autores_ids" class="error-message">
                  {{ errors.autores_ids }}
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
              ¿Estás seguro de que deseas eliminar el libro
              <strong>{{ libroToDelete?.libro_titulo }}</strong
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
  name: "LibrosView",
  data() {
    return {
      libros: [],
      autores: [],
      generos: [],
      loading: false,
      showModal: false,
      modalMode: "create", // 'create' o 'edit'
      modalLoading: false,
      showDeleteModal: false,
      deleteLoading: false,
      libroToDelete: null,
      searchTerm: "",
      selectedGenero: "",
      form: {
        libro_titulo: "",
        anio_publicacion: null,
        genero_id: "",
        autores_ids: [],
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
        this.form.libro_titulo.trim() &&
        this.form.genero_id &&
        this.form.autores_ids.length > 0 &&
        Object.keys(this.errors).length === 0
      );
    },
    filteredLibros() {
      let filtered = this.libros;

      // Filtrar por título
      if (this.searchTerm) {
        filtered = filtered.filter((libro) =>
          libro.libro_titulo
            .toLowerCase()
            .includes(this.searchTerm.toLowerCase())
        );
      }

      // Filtrar por género
      if (this.selectedGenero) {
        filtered = filtered.filter(
          (libro) => libro.genero_id == this.selectedGenero
        );
      }

      return filtered;
    },
  },
  async mounted() {
    await Promise.all([
      this.loadLibros(),
      this.loadAutores(),
      this.loadGeneros(),
    ]);
  },
  methods: {
    async loadLibros() {
      this.loading = true;
      try {
        const response = await libroService.getAll();
        this.libros = response.data;
      } catch (error) {
        console.error("Error loading libros:", error);
        this.toast.error("Error al cargar los libros");
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
        this.toast.error("Error al cargar los autores");
      }
    },

    async loadGeneros() {
      try {
        const response = await generoService.getAll();
        this.generos = response.data;
      } catch (error) {
        console.error("Error loading generos:", error);
        this.toast.error("Error al cargar los géneros");
      }
    },

    clearFilters() {
      this.searchTerm = "";
      this.selectedGenero = "";
    },

    openCreateModal() {
      this.modalMode = "create";
      this.resetForm();
      this.showModal = true;
    },

    openEditModal(libro) {
      this.modalMode = "edit";
      this.form = {
        libro_id: libro.libro_id,
        libro_titulo: libro.libro_titulo,
        anio_publicacion: libro.anio_publicacion || null,
        genero_id: libro.genero_id,
        autores_ids: libro.autores.map((autor) => autor.autor_id),
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
        libro_titulo: "",
        anio_publicacion: null,
        genero_id: "",
        autores_ids: [],
      };
      this.errors = {};
    },

    validateField(fieldName) {
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
          titulo: this.form.libro_titulo,
          anio: this.form.anio_publicacion || null,
          genero_id: parseInt(this.form.genero_id),
          autores_ids: this.form.autores_ids.map((id) => parseInt(id)),
        };

        if (this.modalMode === "create") {
          await libroService.create(data);
          this.toast.success("Libro creado exitosamente");
        } else {
          await libroService.update(this.form.libro_id, data);
          this.toast.success("Libro actualizado exitosamente");
        }

        this.closeModal();
        await this.loadLibros();
      } catch (error) {
        console.error("Error saving libro:", error);
        const message =
          error.response?.data?.error || "Error al guardar el libro";
        this.toast.error(message);
      } finally {
        this.modalLoading = false;
      }
    },

    confirmDelete(libro) {
      this.libroToDelete = libro;
      this.showDeleteModal = true;
    },

    closeDeleteModal() {
      this.showDeleteModal = false;
      this.libroToDelete = null;
    },

    async handleDelete() {
      if (!this.libroToDelete) return;

      this.deleteLoading = true;
      try {
        await libroService.delete(this.libroToDelete.libro_id);
        this.toast.success("Libro eliminado exitosamente");
        this.closeDeleteModal();
        await this.loadLibros();
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

.filters-section {
  margin-bottom: 30px;
  padding: 20px;
  background: white;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);

  .filters {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;

    .filter-group {
      flex: 1;
      min-width: 200px;

      label {
        display: block;
        margin-bottom: 8px;
        font-weight: 500;
        color: var(--secondary-color);
      }

      .search-input,
      .filter-select {
        width: 100%;
        padding: 10px;
        border: 2px solid var(--border-color);
        border-radius: var(--border-radius);
        font-size: 14px;

        &:focus {
          outline: none;
          border-color: var(--primary-color);
        }
      }
    }
  }
}

.libros-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
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

  .libro-info {
    margin-bottom: 20px;

    h3 {
      color: var(--secondary-color);
      margin-bottom: 12px;
      font-size: 1.3rem;
      line-height: 1.4;
    }

    .libro-meta {
      display: flex;
      gap: 12px;
      margin-bottom: 15px;
      flex-wrap: wrap;

      .meta-item {
        background-color: var(--light-color);
        padding: 6px 12px;
        border-radius: 15px;
        font-size: 0.85rem;
        color: var(--secondary-color);
        border: 1px solid var(--border-color);

        &.genero {
          background-color: var(--primary-color);
          color: white;
          border-color: var(--primary-color);
        }
      }
    }

    .autores {
      color: #666;
      font-size: 0.95rem;
      line-height: 1.4;

      strong {
        color: var(--secondary-color);
      }
    }
  }

  .libro-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;

    .btn {
      flex: 1;
      min-width: 100px;
    }
  }
}

.libro-modal {
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
}

@media (max-width: 768px) {
  .libros-grid {
    grid-template-columns: 1fr;
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;

    .btn {
      width: 100%;
    }
  }

  .filters {
    flex-direction: column;
  }

  .libro-actions {
    flex-direction: column;

    .btn {
      width: 100%;
    }
  }
}
</style>
