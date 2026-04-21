<template>
  <transition name="slide-up">
    <div v-if="ui.snackbar.show" 
      class="fixed bottom-10 left-1/2 -translate-x-1/2 z-[1000] px-6 py-4 rounded-2xl font-black text-sm shadow-2xl flex items-center gap-3 border"
      :class="{
        'bg-brand-neon text-black border-white/20': ui.snackbar.type === 'success',
        'bg-red-500 text-white border-white/20': ui.snackbar.type === 'error',
        'bg-brand-purple text-white border-white/20': ui.snackbar.type === 'info'
      }"
    >
      <span>{{ ui.snackbar.message }}</span>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { useUIStore } from '@/stores/ui'
const ui = useUIStore()
</script>

<style scoped>
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.slide-up-enter-from { opacity: 0; transform: translate(-50%, 20px); }
.slide-up-leave-to { opacity: 0; transform: translate(-50%, 20px); }
</style>