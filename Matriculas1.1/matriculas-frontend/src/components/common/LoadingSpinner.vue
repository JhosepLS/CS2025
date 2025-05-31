<template>
  <div :class="containerClass">
    <div :class="spinnerClass">
      <div class="animate-spin rounded-full border-2 border-current border-t-transparent"></div>
    </div>
    <p v-if="message" :class="messageClass">{{ message }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  message: {
    type: String,
    default: ''
  },
  overlay: {
    type: Boolean,
    default: false
  }
})

const containerClass = computed(() => {
  const base = 'flex flex-col items-center justify-center'
  if (props.overlay) {
    return `${base} fixed inset-0 bg-white bg-opacity-75 z-50`
  }
  return `${base} py-8`
})

const spinnerClass = computed(() => {
  const sizes = {
    small: 'w-6 h-6',
    medium: 'w-8 h-8',
    large: 'w-12 h-12'
  }
  return `${sizes[props.size]} text-primary-600`
})

const messageClass = computed(() => {
  const sizes = {
    small: 'text-sm',
    medium: 'text-base',
    large: 'text-lg'
  }
  return `mt-2 ${sizes[props.size]} text-gray-600`
})
</script>