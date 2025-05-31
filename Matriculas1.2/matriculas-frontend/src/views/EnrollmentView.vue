<template>
  <div class="flex h-screen bg-gray-50">
    <AppSidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />
    
    <div class="flex-1 flex flex-col overflow-hidden">
      <AppHeader @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-6">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
          <div>
            <h1 class="text-2xl font-semibold text-gray-900">Matrículas</h1>
            <p class="text-gray-600">Proceso de matrícula de estudiantes</p>
          </div>
          <button class="mt-4 sm:mt-0 btn-primary flex items-center space-x-2">
            <Plus class="w-5 h-5" />
            <span>Nueva Matrícula</span>
          </button>
        </div>

        <div class="card">
          <div class="text-center py-8">
            <FileText class="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p class="text-gray-600">Vista de matrículas en desarrollo</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppHeader from '@/components/common/AppHeader.vue'
import AppSidebar from '@/components/common/AppSidebar.vue'
import { Plus, FileText } from 'lucide-vue-next'

const sidebarOpen = ref(false)
</script>