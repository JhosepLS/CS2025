<script>
import {
  autorService,
  libroService,
  generoService,
  authService,
} from "@/services/api";

export default {
  name: "HomeView",
  data() {
    return {
      stats: null,
      loading: false,
    };
  },
  computed: {
    isAuthenticated() {
      return !!authService.getToken();
    },
  },
  async mounted() {
    await this.loadStats();
  },
  methods: {
    async loadStats() {
      this.loading = true;
      try {
        const [autoresRes, librosRes, generosRes] = await Promise.all([
          autorService.getAll(),
          libroService.getAll(),
          generoService.getAll(),
        ]);

        this.stats = {
          autores: autoresRes.data.length,
          libros: librosRes.data.length,
          generos: generosRes.data.length,
        };
      } catch (error) {
        console.error("Error loading stats:", error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<template>
  <div class="home">
    <div class="container">
      <div class="hero">
        <h1>📚 Sistema de Biblioteca</h1>
        <p>Gestiona autores, libros y géneros de manera eficiente</p>

        <div v-if="!isAuthenticated" class="hero-actions">
          <router-link to="/login" class="btn btn-primary btn-lg">
            Iniciar Sesión
          </router-link>
          <router-link to="/register" class="btn btn-outline btn-lg">
            Registrarse
          </router-link>
        </div>
      </div>

      <div class="features">
        <div class="feature-grid">
          <div class="feature-card">
            <div class="feature-icon">👨‍💼</div>
            <h3>Gestión de Autores</h3>
            <p>
              Administra información completa de autores incluyendo país y año
              de nacimiento
            </p>
            <router-link to="/autores" class="btn btn-primary">
              Ver Autores
            </router-link>
          </div>

          <div class="feature-card">
            <div class="feature-icon">📖</div>
            <h3>Catálogo de Libros</h3>
            <p>
              Organiza libros con múltiples autores, géneros y años de
              publicación
            </p>
            <router-link to="/libros" class="btn btn-primary">
              Ver Libros
            </router-link>
          </div>

          <div v-if="isAuthenticated" class="feature-card">
            <div class="feature-icon">🏷️</div>
            <h3>Géneros Literarios</h3>
            <p>Clasifica y organiza libros por géneros literarios</p>
            <router-link to="/generos" class="btn btn-primary">
              Ver Géneros
            </router-link>
          </div>
        </div>
      </div>

      <div v-if="stats" class="stats">
        <h2>Estadísticas del Sistema</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-number">{{ stats?.autores ?? 0 }}</div>
            <div class="stat-label">Autores</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.libros || 0 }}</div>
            <div class="stat-label">Libros</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.generos || 0 }}</div>
            <div class="stat-label">Géneros</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.home {
  min-height: calc(100vh - 100px);
}

.hero {
  text-align: center;
  padding: 60px 0;
  background: linear-gradient(
    135deg,
    var(--primary-color),
    var(--secondary-color)
  );
  color: white;
  border-radius: var(--border-radius);
  margin-bottom: 40px;

  h1 {
    font-size: 3rem;
    margin-bottom: 20px;
    font-weight: 300;
  }

  p {
    font-size: 1.2rem;
    margin-bottom: 30px;
    opacity: 0.9;
  }

  .hero-actions {
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
  }
}

.features {
  margin-bottom: 60px;

  .feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    margin-top: 40px;
  }

  .feature-card {
    background: white;
    padding: 40px 30px;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;

    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }

    .feature-icon {
      font-size: 3rem;
      margin-bottom: 20px;
    }

    h3 {
      color: var(--secondary-color);
      margin-bottom: 15px;
      font-size: 1.4rem;
    }

    p {
      color: #666;
      margin-bottom: 25px;
      line-height: 1.6;
    }
  }
}

.stats {
  text-align: center;
  padding: 40px 0;

  h2 {
    color: var(--secondary-color);
    margin-bottom: 40px;
    font-size: 2rem;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 30px;
    max-width: 800px;
    margin: 0 auto;
  }

  .stat-card {
    background: white;
    padding: 30px;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    border-top: 4px solid var(--primary-color);

    .stat-number {
      font-size: 3rem;
      font-weight: bold;
      color: var(--primary-color);
      margin-bottom: 10px;
    }

    .stat-label {
      color: var(--secondary-color);
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 1px;
      font-size: 0.9rem;
    }
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 40px 20px;

    h1 {
      font-size: 2rem;
    }

    .hero-actions {
      flex-direction: column;
      align-items: center;
    }
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
