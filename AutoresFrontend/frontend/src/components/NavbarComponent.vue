<template>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-content">
        <div class="navbar-brand">
          <router-link to="/" class="brand-link"> 📚 Biblioteca </router-link>
        </div>

        <div class="navbar-menu" :class="{ active: menuOpen }">
          <div class="navbar-nav">
            <router-link to="/" class="nav-link">Inicio</router-link>
            <router-link to="/autores" class="nav-link">Autores</router-link>
            <router-link to="/libros" class="nav-link">Libros</router-link>
            <router-link v-if="isAuthenticated" to="/generos" class="nav-link">
              Géneros
            </router-link>
          </div>

          <div class="navbar-auth">
            <template v-if="!isAuthenticated">
              <router-link to="/login" class="btn btn-outline btn-sm">
                Iniciar Sesión
              </router-link>
              <router-link to="/register" class="btn btn-primary btn-sm">
                Registrarse
              </router-link>
            </template>
            <template v-else>
              <span class="user-info">
                Hola, {{ user.username }}
                <span v-if="user.role === 'admin'" class="admin-badge"
                  >Admin</span
                >
              </span>
              <button @click="logout" class="btn btn-secondary btn-sm">
                Cerrar Sesión
              </button>
            </template>
          </div>
        </div>

        <button class="navbar-toggle" @click="toggleMenu">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
import { authService } from "@/services/api";
import { useToast } from "vue-toastification";

export default {
  name: "Navbar",
  data() {
    return {
      menuOpen: false,
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
    user() {
      return authService.getUser();
    },
  },
  methods: {
    toggleMenu() {
      this.menuOpen = !this.menuOpen;
    },
    async logout() {
      try {
        authService.clearAuthData();
        this.toast.success("Sesión cerrada correctamente");
        this.$router.push("/");
      } catch (error) {
        console.error("Error al cerrar sesión:", error);
        this.toast.error("Error al cerrar sesión");
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.navbar {
  background-color: var(--secondary-color);
  color: white;
  box-shadow: var(--shadow);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 60px;
}

.navbar-brand {
  .brand-link {
    font-size: 24px;
    font-weight: bold;
    color: white;
    text-decoration: none;

    &:hover {
      color: var(--light-color);
    }
  }
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 40px;

  @media (max-width: 768px) {
    position: fixed;
    top: 60px;
    left: 0;
    width: 100%;
    background-color: var(--secondary-color);
    flex-direction: column;
    gap: 0;
    transform: translateX(-100%);
    transition: transform 0.3s ease;

    &.active {
      transform: translateX(0);
    }
  }
}

.navbar-nav {
  display: flex;
  gap: 20px;

  @media (max-width: 768px) {
    flex-direction: column;
    width: 100%;
    padding: 20px;
    gap: 10px;
  }

  .nav-link {
    color: white;
    text-decoration: none;
    padding: 8px 16px;
    border-radius: var(--border-radius);
    transition: background-color 0.3s ease;

    &:hover,
    &.router-link-active {
      background-color: rgba(255, 255, 255, 0.1);
    }
  }
}

.navbar-auth {
  display: flex;
  align-items: center;
  gap: 15px;

  @media (max-width: 768px) {
    flex-direction: column;
    width: 100%;
    padding: 20px;
    gap: 10px;
  }

  .user-info {
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 8px;

    .admin-badge {
      background-color: var(--warning-color);
      color: white;
      padding: 2px 8px;
      border-radius: 12px;
      font-size: 10px;
      font-weight: bold;
    }
  }
}

.navbar-toggle {
  display: none;
  flex-direction: column;
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;

  @media (max-width: 768px) {
    display: flex;
  }

  span {
    width: 25px;
    height: 3px;
    background-color: white;
    margin: 2px 0;
    transition: 0.3s;
  }
}
</style>
