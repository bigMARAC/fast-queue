<template>
  <div class="min-h-screen bg-brand-black text-white antialiased">
    <nav class="border-b border-white/5 bg-brand-surface/80 backdrop-blur-xl sticky top-0 z-[100]">
      <div class="max-w-7xl mx-auto px-4 h-20 flex items-center justify-between">
        <!-- Logo -->
        <router-link to="/" class="text-2xl font-black tracking-tighter italic">
          FAST<span class="text-brand-purple">QUEUE</span>
        </router-link>

        <!-- Botão Hambúrguer (Mobile Only) -->
        <button @click="isMenuOpen = !isMenuOpen" class="md:hidden p-2 text-brand-gray">
          <svg v-if="!isMenuOpen" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <!-- Menu Desktop -->
        <div class="hidden md:flex items-center gap-8">
          <template v-if="authStore.user">
            <router-link to="/" class="text-sm font-black tracking-widest text-brand-gray hover:text-white">HOME</router-link>
            <router-link to="/dashboard" class="text-sm font-black tracking-widest text-brand-gray hover:text-white">DASHBOARD</router-link>
            <button @click="authStore.logout" class="text-xs font-bold text-red-500">SAIR</button>
          </template>
          <router-link v-else to="/login" class="bg-white text-black px-6 py-2 rounded-xl font-black text-xs">ENTRAR</router-link>
        </div>
      </div>

      <!-- Menu Mobile Overlay -->
      <transition name="slide">
        <div v-if="isMenuOpen" class="md:hidden absolute top-20 left-0 w-full bg-brand-surface border-b border-white/5 p-6 space-y-6 shadow-2xl">
          <template v-if="authStore.user">
            <router-link @click="isMenuOpen = false" to="/" class="block text-xl font-black italic">HOME</router-link>
            <router-link @click="isMenuOpen = false" to="/dashboard" class="block text-xl font-black italic">DASHBOARD</router-link>
            <div class="h-[1px] bg-white/5"></div>
            <button @click="authStore.logout(); isMenuOpen = false" class="block w-full text-left text-red-500 font-bold">SAIR DA CONTA</button>
          </template>
          <button v-else @click="authStore.loginWithGoogle(); isMenuOpen = false" class="w-full bg-brand-purple py-4 rounded-2xl font-black">ENTRAR COM GOOGLE</button>
        </div>
      </transition>
    </nav>

    <main class="max-w-7xl mx-auto px-4 py-8">
      <router-view />
      <div v-if="authStore.needsOnboarding" class="fixed inset-0 bg-brand-black/98 z-[999] flex items-center justify-center p-6 backdrop-blur-xl">
        <div class="max-w-md w-full bg-brand-surface border border-brand-purple p-10 rounded-[3rem] text-center space-y-8 shadow-[0_0_50px_rgba(124,58,237,0.2)]">
          <h2 class="text-3xl font-black italic">QUASE LÁ!</h2>
          <p class="text-brand-gray">Como os streamers e viewers devem te chamar na plataforma?</p>
          
          <input 
            v-model="onboardingName" 
            type="text" 
            placeholder="Seu Nome ou Nick"
            class="w-full bg-brand-black border border-white/10 p-5 rounded-2xl outline-none focus:border-brand-purple text-xl text-center font-bold"
          />
          
          <button 
            @click="saveOnboardingName"
            :disabled="!onboardingName"
            class="w-full bg-brand-purple py-5 rounded-2xl font-black text-lg hover:scale-105 transition-all disabled:opacity-30"
          >
            COMEÇAR A USAR
          </button>
        </div>
      </div>
    </main>
    <AppSnackbar /> 
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router'
import AppSnackbar from '@/components/AppSnackbar.vue'

const authStore = useAuthStore();
const onboardingName = ref('');
const router = useRouter()
const isMenuOpen = ref(false)

const saveOnboardingName = async () => {
  await authStore.updateDisplayName(onboardingName.value);
};

watch(() => authStore.user, (newUser, oldUser) => {
  if (oldUser && !newUser) {
    router.push('/login')
  }
  
  if (!oldUser && newUser) {
    if (router.currentRoute.value.path === '/login') {
      router.push('/dashboard')
    }
  }
})
</script>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>