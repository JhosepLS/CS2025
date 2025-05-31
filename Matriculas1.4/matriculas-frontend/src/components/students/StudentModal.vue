<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen px-4 text-center sm:block sm:p-0">
      <!-- Overlay -->
      <div 
        class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
        @click="$emit('close')"
      ></div>

      <!-- Modal -->
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <form @submit.prevent="handleSubmit">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                  {{ student ? 'Editar Estudiante' : 'Nuevo Estudiante' }}
                </h3>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <!-- Información Personal -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Nombre *
                    </label>
                    <input
                      v-model="form.nombre"
                      type="text"
                      required
                      class="input-field"
                      placeholder="Nombre del estudiante"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Apellido *
                    </label>
                    <input
                      v-model="form.apellido"
                      type="text"
                      required
                      class="input-field"
                      placeholder="Apellido del estudiante"
                    />
                  </div>

                  <div class="md:col-span-2">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Email *
                    </label>
                    <input
                      v-model="form.email"
                      type="email"
                      required
                      class="input-field"
                      placeholder="email@universidad.edu"
                    />
                  </div>

                  <div v-if="!student">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Contraseña *
                    </label>
                    <input
                      v-model="form.password"
                      type="password"
                      :required="!student"
                      class="input-field"
                      placeholder="Contraseña"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Código *
                    </label>
                    <input
                      v-model="form.codigo"
                      type="text"
                      required
                      class="input-field"
                      placeholder="ALU001"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      DNI *
                    </label>
                    <input
                      v-model="form.dni"
                      type="text"
                      required
                      class="input-field"
                      placeholder="12345678"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Fecha de Nacimiento *
                    </label>
                    <input
                      v-model="form.fechaNacimiento"
                      type="date"
                      required
                      class="input-field"
                    />
                  </div>

                  <!-- Información Académica -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Escuela *
                    </label>
                    <select
                      v-model="form.escuelaId"
                      required
                      class="input-field"
                      @change="handleSchoolChange"
                    >
                      <option value="">Seleccionar escuela</option>
                      <option v-for="school in schools" :key="school.id" :value="school.id">
                        {{ school.nombre }}
                      </option>
                    </select>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Plan de Estudio *
                    </label>
                    <select
                      v-model="form.planEstudioId"
                      required
                      class="input-field"
                      :disabled="!form.escuelaId"
                    >
                      <option value="">Seleccionar plan</option>
                      <option v-for="plan in studyPlans" :key="plan.id" :value="plan.id">
                        {{ plan.nombre }}
                      </option>
                    </select>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Ciclo Actual
                    </label>
                    <input
                      v-model.number="form.cicloActual"
                      type="number"
                      min="1"
                      max="12"
                      class="input-field"
                      placeholder="1"
                    />
                  </div>

                  <div v-if="student">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Estado
                    </label>
                    <select v-model="form.estado" class="input-field">
                      <option value="activo">Activo</option>
                      <option value="egresado">Egresado</option>
                      <option value="retirado">Retirado</option>
                      <option value="suspendido">Suspendido</option>
                    </select>
                  </div>

                  <!-- Información de Contacto -->
                  <div class="md:col-span-2">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Dirección
                    </label>
                    <input
                      v-model="form.direccion"
                      type="text"
                      class="input-field"
                      placeholder="Dirección completa"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Teléfono
                    </label>
                    <input
                      v-model="form.telefono"
                      type="text"
                      class="input-field"
                      placeholder="123456789"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Fecha de Ingreso
                    </label>
                    <input
                      v-model="form.fechaIngreso"
                      type="date"
                      class="input-field"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="submit"
              :disabled="loading"
              class="btn-primary sm:ml-3 sm:w-auto w-full"
            >
              <span v-if="loading">Guardando...</span>
              <span v-else>{{ student ? 'Actualizar' : 'Crear' }}</span>
            </button>
            <button
              type="button"
              @click="$emit('close')"
              class="btn-secondary mt-3 sm:mt-0 sm:w-auto w-full"
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  student: Object,
  schools: Array,
  studyPlans: Array
})

const emit = defineEmits(['close', 'save', 'school-change'])

const loading = ref(false)
const form = ref({
  nombre: '',
  apellido: '',
  email: '',
  password: '',
  codigo: '',
  dni: '',
  fechaNacimiento: '',
  escuelaId: '',
  planEstudioId: '',
  cicloActual: 1,
  estado: 'activo',
  direccion: '',
  telefono: '',
  fechaIngreso: new Date().toISOString().split('T')[0]
})

const resetForm = () => {
  form.value = {
    nombre: '',
    apellido: '',
    email: '',
    password: '',
    codigo: '',
    dni: '',
    fechaNacimiento: '',
    escuelaId: '',
    planEstudioId: '',
    cicloActual: 1,
    estado: 'activo',
    direccion: '',
    telefono: '',
    fechaIngreso: new Date().toISOString().split('T')[0]
  }
}

const loadStudentData = () => {
  if (props.student) {
    form.value = {
      nombre: props.student.usuario?.nombre || '',
      apellido: props.student.usuario?.apellido || '',
      email: props.student.usuario?.email || '',
      password: '',
      codigo: props.student.codigo || '',
      dni: props.student.dni || '',
      fechaNacimiento: props.student.fechaNacimiento || '',
      escuelaId: props.student.escuelaId || '',
      planEstudioId: props.student.planEstudioId || '',
      cicloActual: props.student.cicloActual || 1,
      estado: props.student.estado || 'activo',
      direccion: props.student.direccion || '',
      telefono: props.student.telefono || '',
      fechaIngreso: props.student.fechaIngreso || ''
    }
  } else {
    resetForm()
  }
}

const handleSchoolChange = () => {
  form.value.planEstudioId = ''
  if (form.value.escuelaId) {
    emit('school-change', form.value.escuelaId)
  }
}

const handleSubmit = async () => {
  loading.value = true
  try {
    const data = { ...form.value }
    if (props.student && !data.password) {
      delete data.password
    }
    emit('save', data)
  } finally {
    loading.value = false
  }
}

watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    loadStudentData()
  }
})

onMounted(() => {
  if (props.isOpen) {
    loadStudentData()
  }
})
</script>