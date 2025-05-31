<template>
  <div 
    v-if="notifications.length > 0"
    class="fixed top-4 right-4 z-50 space-y-2"
  >
    <TransitionGroup name="toast" tag="div">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        :class="[
          'max-w-sm rounded-lg shadow-lg p-4 text-white',
          {
            'bg-green-500': notification.type === 'success',
            'bg-red-500': notification.type === 'error',
            'bg-blue-500': notification.type === 'info',
            'bg-yellow-500': notification.type === 'warning'
          }
        ]"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <CheckCircle v-if="notification.type === 'success'" class="w-5 h-5" />
            <XCircle v-else-if="notification.type === 'error'" class="w-5 h-5" />
            <Info v-else-if="notification.type === 'info'" class="w-5 h-5" />
            <AlertTriangle v-else-if="notification.type === 'warning'" class="w-5 h-5" />
            <span class="text-sm font-medium">{{ notification.message }}</span>
          </div>
          <button 
            @click="removeNotification(notification.id)"
            class="ml-2 text-white hover:text-gray-200"
          >
            <X class="w-4 h-4" />
          </button>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { CheckCircle, XCircle, Info, AlertTriangle, X } from 'lucide-vue-next'

const notifications = ref([])

let notificationId = 0

const addNotification = (message, type = 'info', duration = 5000) => {
  const id = ++notificationId
  notifications.value.push({ id, message, type })
  
  setTimeout(() => {
    removeNotification(id)
  }, duration)
}

const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
}

// Global notification function
window.notify = addNotification

defineExpose({
  addNotification,
  removeNotification
})
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>