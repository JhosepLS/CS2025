<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <RouterView />
    <NotificationToast />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import NotificationToast from './components/common/NotificationToast.vue'
</script>