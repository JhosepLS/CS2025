<template>
  <div class="login">
    <div class="container">
      <div class="login-container">
        <div class="card">
          <div class="card-header">
            <h3>Iniciar Sesión</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleLogin">
              <div class="form-group">
                <label for="username">Usuario</label>
                <input
                  id="username"
                  v-model="form.username"
                  type="text"
                  placeholder="Ingresa tu usuario"
                  :class="{ error: errors.username }"
                  @blur="validateField('username')"
                />
                <div v-if="errors.username" class="error-message">
                  {{ errors.username }}
                </div>
              </div>

              <div class="form-group">
                <label for="password">Contraseña</label>
                <input
                  id="password"
                  v-model="form.password"
                  type="password"
                  placeholder="Ingresa tu contraseña"
                  :class="{ error: errors.password }"
                  @blur="validateField('password')"
                />
                <div v-if="errors.password" class="error-message">
                  {{ errors.password }}
                </div>
              </div>

              <button
                type="submit"
                class="btn btn-primary btn-lg"
                :disabled="loading || !isFormValid"
              >
                {{ loading ? "Iniciando sesión..." : "Iniciar Sesión" }}
              </button>
            </form>

            <div class="login-footer">
              <p>
                ¿No tienes cuenta?
                <router-link to="/register">Regístrate aquí</router-link>
              </p>
            </div>

            <!-- Credenciales de prueba -->
            <div class="test-credentials">
              <h4>Credenciales de prueba:</h4>
              <div class="credentials-grid">
                <div class="credential-item">
                  <strong>Administrador:</strong><br />
                  Usuario: admin<br />
                  Contraseña: admin123
                  <button
                    @click="fillCredentials('admin', 'admin123')"
                    class="btn btn-sm btn-outline"
                  >
                    Usar
                  </button>
                </div>
                <div class="credential-item">
                  <strong>Usuario normal:</strong><br />
                  Usuario: usuario<br />
                  Contraseña: user123
                  <button
                    @click="fillCredentials('usuario', 'user123')"
                    class="btn btn-sm btn-outline"
                  >
                    Usar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { authService } from "@/services/api";
import { validations, validateForm } from "@/utils/validations";
import { useToast } from "vue-toastification";

export default {
  name: "LoginView",
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
      errors: {},
      loading: false,
    };
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  computed: {
    isFormValid() {
      return (
        this.form.username.trim() &&
        this.form.password.trim() &&
        Object.keys(this.errors).length === 0
      );
    },
  },
  methods: {
    validateField(fieldName) {
      const fieldValidations = {
        username: [validations.username.required],
        password: [validations.password.required],
      };

      const rules = fieldValidations[fieldName];
      if (rules) {
        for (const rule of rules) {
          const result = rule(this.form[fieldName]);
          if (result !== true) {
            this.errors = {
              ...this.errors,
              [fieldName]: result,
            };
            return;
          }
        }
        const { [fieldName]: _, ...rest } = this.errors;
        this.errors = rest;
      }
    },

    validateForm() {
      const validationRules = {
        username: [validations.username.required],
        password: [validations.password.required],
      };

      const { isValid, errors } = validateForm(this.form, validationRules);
      this.errors = errors;
      return isValid;
    },

    fillCredentials(username, password) {
      this.form.username = username;
      this.form.password = password;
      this.errors = {};
    },

    async handleLogin() {
      if (!this.validateForm()) {
        this.toast.error("Por favor corrige los errores del formulario");
        return;
      }

      this.loading = true;
      try {
        const response = await authService.login(this.form);
        authService.setAuthData(response.data.token, response.data.user);
        this.toast.success(`Bienvenido, ${response.data.user.username}!`);
        this.$router.push("/");
      } catch (error) {
        console.error("Login error:", error);
        const message =
          error.response?.data?.error || "Error al iniciar sesión";
        this.toast.error(message);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.login {
  min-height: calc(100vh - 100px);
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.login-container {
  max-width: 500px;
  margin: 0 auto;
  width: 100%;
}

.card {
  margin: 20px 0;
}

.login-footer {
  margin-top: 20px;
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);

  a {
    color: var(--primary-color);
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
}

.test-credentials {
  margin-top: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);

  h4 {
    margin-bottom: 15px;
    color: var(--secondary-color);
    font-size: 1rem;
  }

  .credentials-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;

    @media (max-width: 480px) {
      grid-template-columns: 1fr;
    }
  }

  .credential-item {
    padding: 15px;
    background: white;
    border-radius: var(--border-radius);
    border: 1px solid var(--border-color);
    font-size: 0.9rem;
    position: relative;

    .btn {
      margin-top: 10px;
      width: 100%;
    }
  }
}
</style>
