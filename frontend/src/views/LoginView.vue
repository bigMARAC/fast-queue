<template>
  <div class="min-h-[80vh] flex items-center justify-center">
    <div class="w-full max-w-md bg-brand-surface border border-white/10 p-10 rounded-[2rem] shadow-2xl">
      <div class="text-center mb-10">
        <h2 class="text-3xl font-black italic tracking-tighter mb-2">ENTRAR NO <span
            class="text-brand-purple">FASTQUEUE</span></h2>
        <!-- <p class="text-brand-gray text-sm">Escolha uma forma de acesso para continuar</p> -->
      </div>

      <div class="space-y-4">
        <button @click="handleGoogleLogin"
          class="cursor-pointer w-full flex items-center justify-center gap-3 bg-white text-black py-4 rounded-2xl font-bold hover:bg-brand-gray transition-all active:scale-95">
          <img width="28" height="28" src="https://img.icons8.com/color/48/google-logo.png" alt="google-logo" />
          Entrar com Google
        </button>

        <div class="relative py-4">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-white/5"></div>
          </div>
          <!-- <div class="relative flex justify-center text-xs uppercase"><span class="bg-brand-surface px-2 text-brand-gray font-bold">Ou</span></div> -->
        </div>

        <p class="text-center text-xs text-brand-gray">
          Ao entrar, você concorda com nossos termos de serviço.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const handleGoogleLogin = async () => {
  try {
    await authStore.loginWithGoogle();
    router.push('/');
  } catch (error) {
    console.error("Falha no login:", error);
  }
};
</script>