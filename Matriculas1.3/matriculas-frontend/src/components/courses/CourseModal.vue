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
                  {{ course ? 'Editar Curso' : 'Nuevo Curso' }}
                </h3>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <!-- Información básica -->
                  <div class="md:col-span-2">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Plan de Estudio *
                    </label>
                    <select
                      v-model="form.planEstudioId"
                      required
                      class="input-field"
                    >
                      <option value="">Seleccionar plan de estudio</option>
                      <option v-for="plan in studyPlans" :key="plan.id" :value="plan.id">
                        {{ plan.nombre }}
                      </option>
                    </select>
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
                      placeholder="MAT101"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Ciclo *
                    </label>
                    <select v-model="form.ciclo" required class="input-field">
                      <option value="">Seleccionar ciclo</option>
                      <option v-for="i in 10" :key="i" :value="i">{{ i }}</option>
                    </select>
                  </div>

                  <div class="md:col-span-2">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Nombre *
                    </label>
                    <input
                      v-model="form.nombre"
                      type="text"
                      required
                      class="input-field"
                      placeholder="Nombre del curso"
                    />
                  </div>

                  <div class="md:col-span-2">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Descripción
                    </label>
                    <textarea
                      v-model="form.descripcion"
                      rows="3"
                      class="input-field"
                      placeholder="Descripción del curso"
                    ></textarea>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Créditos *
                    </label>
                    <input
                      v-model.number="form.creditos"
                      type="number"
                      min="1"
                      max="10"
                      required
                      class="input-field"
                      placeholder="4"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Tipo *
                    </label>
                    <select v-model="form.tipo" required class="input-field">
                      <option value="obligatorio">Obligatorio</option>
                      <option value="electivo">Electivo</option>
                    </select>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Horas Teóricas *
                    </label>
                    <input
                      v-model.number="form.horasTeoricas"
                      type="number"
                      min="0"
                      max="8"
                      required
                      class="input-field"
                      placeholder="3"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Horas Prácticas *
                    </label>
                    <input
                      v-model.number="form.horasPracticas"
                      type="number"
                      min="0"
                      max="8"
                      required
                      class="input-field"
                      placeholder="2"
                    />
                  </div>

                  <div v-if="course" class="md:col-span-2">
                    <label class="flex items-center">
                      <input
                        v-model="form.activo"
                        type="checkbox"
                        class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-300 focus:ring focus:ring-primary-200 focus:ring-opacity-50"
                      />
                      <span class="ml-2 text-sm text-gray-700">Curso activo</span>
                    </label>
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
              <span v-else>{{ course ? 'Actualizar' : 'Crear' }}</span>
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
  course: Object,
  studyPlans: Array
})

const emit = defineEmits(['close', 'save'])

const loading = ref(false)
const form = ref({
  planEstudioId: '',
  codigo: '',
  nombre: '',
  descripcion: '',
  ciclo: '',
  creditos: 1,
  horasTeoricas: 0,
  horasPracticas: 0,
  tipo: 'obligatorio',
  activo: true
})

const resetForm = () => {
  form.value = {
    planEstudioId: '',
    codigo: '',
    nombre: '',
    descripcion: '',
    ciclo: '',
    creditos: 1,
    horasTeoricas: 0,
    horasPracticas: 0,
    tipo: 'obligatorio',
    activo: true
  }
}

const loadCourseData = () => {
  if (props.course) {
    form.value = {
      planEstudioId: props.course.planEstudioId || '',
      codigo: props.course.codigo || '',
      nombre: props.course.nombre || '',
      descripcion: props.course.descripcion || '',
      ciclo: props.course.ciclo || '',
      creditos: props.course.creditos || 1,
      horasTeoricas: props.course.horasTeoricas || 0,
      horasPracticas: props.course.horasPracticas || 0,
      tipo: props.course.tipo || 'obligatorio',
      activo: props.course.activo !== undefined ? props.course.activo : true
    }
  } else {
    resetForm()
  }
}

const handleSubmit = async () => {
  loading.value = true
  try {
    const data = { ...form.value }
    emit('save', data)
  } finally {
    loading.value = false
  }
}

watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    loadCourseData()
  }
})

onMounted(() => {
  if (props.isOpen) {
    loadCourseData()
  }
})
</script>