import { createRouter, createWebHashHistory } from "vue-router";
import { authService } from "@/services/api";

// Importar vistas
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import AutoresView from "@/views/AutoresView.vue";
import AutorDetailView from "@/views/AutorDetailView.vue";
import LibrosView from "@/views/LibrosView.vue";
import LibroDetailView from "@/views/LibroDetailView.vue";
import GenerosView from "@/views/GenerosView.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
  },
  {
    path: "/login",
    name: "Login",
    component: LoginView,
    meta: { requiresGuest: true },
  },
  {
    path: "/register",
    name: "Register",
    component: RegisterView,
    meta: { requiresGuest: true },
  },
  {
    path: "/autores",
    name: "Autores",
    component: AutoresView,
  },
  {
    path: "/autor/:id",
    name: "AutorDetail",
    component: AutorDetailView,
    props: true,
  },
  {
    path: "/libros",
    name: "Libros",
    component: LibrosView,
  },
  {
    path: "/libro/:id",
    name: "LibroDetail",
    component: LibroDetailView,
    props: true,
  },
  {
    path: "/generos",
    name: "Generos",
    component: GenerosView,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// Guard de navegación para rutas protegidas
router.beforeEach((to, from, next) => {
  const token = authService.getToken();
  const isAuthenticated = !!token;

  // Si la ruta requiere autenticación y el usuario no está autenticado
  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login");
    return;
  }

  // Si la ruta es solo para invitados y el usuario está autenticado
  if (to.meta.requiresGuest && isAuthenticated) {
    next("/");
    return;
  }

  next();
});

export default router;
