<template>
  <div class="flex h-screen bg-gray-50">
    <AppSidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />
    
    <div class="flex-1 flex flex-col overflow-hidden">
      <AppHeader @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-6">
        <!-- Header Actions -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
          <div>
            <h1 class="text-2xl font-semibold text-gray-900">Estudiantes</h1>
            <p class="text-gray-600">Gestiona los estudiantes del sistema</p>
          </div>
          <button
            @click="showCreateModal = true"
            class="mt-4 sm:mt-0 btn-primary flex items-center space-x-2"
          >
            <Plus class="w-5 h-5" />
            <span>Nuevo Estudiante</span>
          </button>
        </div>

        <!-- Filters -->
        <div class="card mb-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Buscar</label>
              <div class="relative">
                <input
                  v-model="filters.search"
                  type="text"
                  placeholder="Nombre, código o DNI..."
                  class="input-field pl-10"
                  @input="debouncedSearch"
                />
                <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Escuela</label>
              <select v-model="filters.escuelaId" class="input-field" @change="fetchStudents">
                <option value="">Todas las escuelas</option>
                <option v-for="school in studentsStore.schools" :key="school.id" :value="school.id">
                  {{ school.nombre }}
                </option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select v-model="filters.estado" class="input-field" @change="fetchStudents">
                <option value="">Todos los estados</option>
                <option value="activo">Activo</option>
                <option value="egresado">Egresado</option>
                <option value="retirado">Retirado</option>
                <option value="suspendido">Suspendido</option>
              </select>
            </div>
            
            <div class="flex items-end">
              <button @click="clearFilters" class="btn-secondary w-full">
                <Filter class="w-4 h-4 mr-2" />
                Limpiar Filtros
              </button>
            </div>
          </div>
        </div>

        <!-- Students List -->
        <div class="card">
          <div v-if="studentsStore.loading" class="flex justify-center py-8">
            <LoadingSpinner size="medium" message="Cargando estudiantes..." />
          </div>
          
          <div v-else-if="studentsStore.students.length === 0" class="text-center py-8">
            <Users class="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p class="text-gray-600">No se encontraron estudiantes</p>
          </div>
          
          <div v-else class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Estudiante
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Código/DNI
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Escuela
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Ciclo
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Estado
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y