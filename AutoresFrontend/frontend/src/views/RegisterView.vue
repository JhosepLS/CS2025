<template>
  <div class="register">
    <div class="container">
      <div class="register-container">
        <div class="card">
          <div class="card-header">
            <h3>Crear Cuenta</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleRegister">
              <div class="form-group">
                <label for="username">Usuario</label>
                <input
                  id="username"
                  v-model="form.username"
                  type="text"
                  placeholder="Mínimo 3 caracteres"
                  :class="{ error: errors.username }"
                  @blur="validateField('username')"
                />
                <div v-if="errors.username" class="error-message">
                  {{ errors.username }}
                </div>
              </div>

              <div class="form-group">
                <label for="email">Email</label>
                <input
                  id="email"
                  v-model="form.email"
                  type="email"
                  placeholder="tu@email.com"
                  :class="{ error: errors.email }"
                  @blur="validateField('email')"
                />
                <div v-if="errors.email" class="error-message">
                  {{ errors.email }}
                </div>
              </div>

              <div class="form-group">
                <label for="password">Contraseña</label>
                <input
                  id="password"
                  v-model="form.password"
                  type="password"
                  placeholder="Mínimo 6 caracteres"
                  :class="{ error: errors.password }"
                  @blur="validateField('password')"
                />
                <div v-if="errors.password" class="error-message">
                  {{ errors.password }}
                </div>
              </div>

              <div class="form-group">
                <label for="confirmPassword">Confirmar Contraseña</label>
                <input
                  id="confirmPassword"
                  v-model="form.confirmPassword"
                  type="password"
                  placeholder="Repite la contraseña"
                  :class="{ error: errors.confirmPassword }"
                  @blur="validateField('confirmPassword')"
                />
                <div v-if="errors.confirmPassword" class="error-message">
                  {{ errors.confirmPassword }}
                </div>
              </div>

              <button
                type="submit"
                class="btn btn-primary btn-lg"
                :disabled="loading || !isFormValid"
              >
                {{ loading ? "Creando cuenta..." : "Crear Cuenta" }}
              </button>
            </form>

            <div class="register-footer">
              <p>
                ¿Ya tienes cuenta?
                <router-link to="/login">Inicia sesión aquí</router-link>
              </p>
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
  name: "RegisterView",
  data() {
    return {
      form: {
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
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
        this.form.email.trim() &&
        this.form.password.trim() &&
        this.form.confirmPassword.trim() &&
        this.form.password === this.form.confirmPassword &&
        Object.keys(this.errors).length === 0
      );
    },
  },
  methods: {
    validateField(fieldName) {
      const fieldValidations = {
        username: [
          validations.username.required,
          validations.username.minLength,
          validations.username.maxLength,
        ],
        email: [validations.email.required, validations.email.email],
        password: [
          validations.password.required,
          validations.password.minLength,
          validations.password.maxLength,
        ],
        confirmPassword: [
          (value) => !!value || "La confirmación de contraseña es requerida",
          (value) =>
            value === this.form.password || "Las contraseñas no coinciden",
        ],
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
        username: [
          validations.username.required,
          validations.username.minLength,
          validations.username.maxLength,
        ],
        email: [validations.email.required, validations.email.email],
        password: [
          validations.password.required,
          validations.password.minLength,
          validations.password.maxLength,
        ],
        confirmPassword: [
          (value) => !!value || "La confirmación de contraseña es requerida",
          (value) =>
            value === this.form.password || "Las contraseñas no coinciden",
        ],
      };

      const { isValid, errors } = validateForm(this.form, validationRules);
      this.errors = errors;
      return isValid;
    },

    async handleRegister() {
      if (!this.validateForm()) {
        this.toast.error("Por favor corrige los errores del formulario");
        return;
      }

      this.loading = true;
      try {
        // eslint-disable-next-line no-unused-vars
        const { confirmPassword, ...registerData } = this.form;
        await authService.register(registerData);

        this.toast.success(
          "Cuenta creada exitosamente. Ahora puedes iniciar sesión."
        );

        this.$router.push("/login");
      } catch (error) {
        console.error("Register error:", error);
        const message =
          error.response?.data?.error || "Error al crear la cuenta";
        this.toast.error(message);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.register {
  min-height: calc(100vh - 100px);
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 0;
}

.register-container {
  max-width: 500px;
  margin: 0 auto;
  width: 100%;
}

.card {
  margin: 20px 0;
}

.register-footer {
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
</style>
