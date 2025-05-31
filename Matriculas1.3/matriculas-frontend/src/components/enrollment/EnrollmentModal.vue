<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen px-4 text-center sm:block sm:p-0">
      <!-- Overlay -->
      <div 
        class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
        @click="$emit('close')"
      ></div>

      <!-- Modal -->
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
        <form @submit.prevent="handleSubmit">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                  Nueva Matrícula
                </h3>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <!-- Estudiante -->
                  <div class="md:col-span-2">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Estudiante *
                    </label>
                    <select
                      v-model="form.alumnoId"
                      required
                      class="input-field"
                      @change="handleStudentChange"
                    >
                      <option value="">Seleccionar estudiante</option>
                      <option v-for="student in students" :key="student.id" :value="student.id">
                        {{ student.usuario?.nombre }} {{ student.usuario?.apellido }} - {{ student.codigo }}
                      </option>
                    </select>
                  </div>

                  <!-- Periodo Académico -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Periodo Académico *
                    </label>
                    <select
                      v-model="form.periodoAcademicoId"
                      required
                      class="input-field"
                      @change="handlePeriodChange"
                    >
                      <option value="">Seleccionar periodo</option>
                      <option v-for="period in academicPeriods" :key="period.id" :value="period.id">
                        {{ period.nombre }}
                      </option>
                    </select>
                  </div>

                  <!-- Tipo de Matrícula -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Tipo de Matrícula *
                    </label>
                    <select
                      v-model="form.tipoMatricula"
                      required
                      class="input-field"
                    >
                      <option value="regular">Regular</option>
                      <option value="extemporanea">Extemporánea</option>
                    </select>
                  </div>

                  <!-- Información del estudiante seleccionado -->
                  <div v-if="selectedStudent" class="md:col-span-2">
                    <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <h4 class="text-sm font-medium text-blue-900 mb-2">Información del Estudiante</h4>
                      <div class="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span class="text-blue-700 font-medium">Escuela:</span>
                          <span class="text-blue-600 ml-1">{{ selectedStudent.escuela?.nombre }}</span>
                        </div>
                        <div>
                          <span class="text-blue-700 font-medium">Ciclo Actual:</span>
                          <span class="text-blue-600 ml-1">{{ selectedStudent.cicloActual }}</span>
                        </div>
                        <div>
                          <span class="text-blue-700 font-medium">Plan de Estudio:</span>
                          <span class="text-blue-600 ml-1">{{ selectedStudent.planEstudio?.nombre }}</span>
                        </div>
                        <div>
                          <span class="text-blue-700 font-medium">Estado:</span>
                          <span class="text-blue-600 ml-1">{{ selectedStudent.estado }}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Secciones disponibles -->
                  <div v-if="availableSections.length > 0" class="md:col-span-2">
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                      Seleccionar Cursos/Secciones *
                    </label>
                    <div class="border border-gray-300 rounded-lg max-h-60 overflow-y-auto">
                      <div 
                        v-for="section in availableSections" 
                        :key="section.id"
                        class="flex items-center p-3 border-b border-gray-200 last:border-b-0"
                      >
                        <input
                          :id="`section-${section.id}`"
                          v-model="selectedSections"
                          type="checkbox"
                          :value="section.id"
                          class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-300 focus:ring focus:ring-primary-200 focus:ring-opacity-50"
                        />
                        <label :for="`section-${section.id}`" class="ml-3 flex-1 cursor-pointer">
                          <div class="flex justify-between items-center">
                            <div>
                              <p class="font-medium text-gray-900">
                                {{ section.curso?.nombre }} - Sección {{ section.nombre }}
                              </p>
                              <p class="text-sm text-gray-600">
                                {{ section.curso?.codigo }} | Ciclo {{ section.curso?.ciclo }} | {{ section.curso?.creditos }} créditos
                              </p>
                              <p class="text-xs text-gray-500">
                                Docente: {{ section.docente?.usuario?.nombre }} {{ section.docente?.usuario?.apellido }}
                              </p>
                            </div>
                            <div class="text-right">
                              <p class="text-sm font-medium text-gray-900">
                                {{ section.capacidadActual }}/{{ section.capacidadMaxima }}
                              </p>
                              <p class="text-xs text-gray-500">Cupos</p>
                            </div>
                          </div>
                        </label>
                      </div>
                    </div>
                    <p class="text-xs text-gray-500 mt-2">
                      Total de créditos seleccionados: {{ totalCredits }}
                    </p>
                  </div>

                  <!-- Resumen de matrícula -->
                  <div v-if="selectedSections.length > 0" class="md:col-span-2">
                    <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                      <h4 class="text-sm font-medium text-green-900 mb-2">Resumen de Matrícula</h4>
                      <div class="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span class="text-green-700 font-medium">Cursos seleccionados:</span>
                          <span class="text-green-600 ml-1">{{ selectedSections.length }}</span>
                        </div>
                        <div>
                          <span class="text-green-700 font-medium">Total créditos:</span>
                          <span class="text-green-600 ml-1">{{ totalCredits }}</span>
                        </div>
                        <div>
                          <span class="text-green-700 font-medium">Costo estimado:</span>
                          <span class="text-green-600 ml-1">S/. {{ estimatedCost }}</span>
                        </div>
                        <div>
                          <span class="text-green-700 font-medium">Tipo:</span>
                          <span class="text-green-600 ml-1">{{ form.tipoMatricula }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="submit"
              :disabled="loading || selectedSections.length === 0"
              class="btn-primary sm:ml-3 sm:w-auto w-full"
            >
              <span v-if="loading">Creando...</span>
              <span v-else>Crear Matrícula</span>
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
import { ref, computed, watch } from 'vue'
import { sectionsAPI } from '@/services/api'

const props = defineProps({
  isOpen: Boolean,
  students: Array,
  academicPeriods: Array
})

const emit = defineEmits(['close', 'save'])

const loading = ref(false)
const availableSections = ref([])
const selectedSections = ref([])

const form = ref({
  alumnoId: '',
  periodoAcademicoId: '',
  tipoMatricula: 'regular'
})

const selectedStudent = computed(() => {
  return props.students.find(s => s.id === form.value.alumnoId)
})

const totalCredits = computed(() => {
  return availableSections.value
    .filter(section => selectedSections.value.includes(section.id))
    .reduce((total, section) => total + (section.curso?.creditos || 0), 0)
})

const estimatedCost = computed(() => {
  const costPerCredit = form.value.tipoMatricula === 'extemporanea' ? 120 : 100
  return totalCredits.value * costPerCredit
})

const handleStudentChange = () => {
  selectedSections.value = []
  availableSections.value = []
  if (form.value.alumnoId && form.value.periodoAcademicoId) {
    fetchAvailableSections()
  }
}

const handlePeriodChange = () => {
  selectedSections.value = []
  availableSections.value = []
  if (form.value.alumnoId && form.value.periodoAcademicoId) {
    fetchAvailableSections()
  }
}

const fetchAvailableSections = async () => {
  try {
    loading.value = true
    const response = await sectionsAPI.getAll({
      periodoAcademicoId: form.value.periodoAcademicoId,
      activo: true
    })
    
    // Filtrar secciones que tienen cupo disponible
    availableSections.value = (response.data.data || []).filter(
      section => section.capacidadActual < section.capacidadMaxima
    )
    
    console.log('Secciones disponibles:', availableSections.value)
  } catch (error) {
    console.error('Error al cargar secciones:', error)
    window.notify?.('Error al cargar secciones disponibles', 'error')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (selectedSections.value.length === 0) {
    window.notify?.('Debe seleccionar al menos un curso', 'warning')
    return
  }

  loading.value = true
  try {
    const enrollmentData = {
      alumnoId: form.value.alumnoId,
      periodoAcademicoId: form.value.periodoAcademicoId,
      tipoMatricula: form.value.tipoMatricula,
      secciones: selectedSections.value.map(seccionId => ({ seccionId }))
    }
    
    emit('save', enrollmentData)
  } finally {
    loading.value = false
  }
}

watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    // Reset form
    form.value = {
      alumnoId: '',
      periodoAcademicoId: '',
      tipoMatricula: 'regular'
    }
    selectedSections.value = []
    availableSections.value = []
  }
})
</script>