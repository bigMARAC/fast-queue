<template>
  <div class="space-y-32 pb-20 overflow-hidden">
    <!-- HERO SECTION -->
    <section class="relative pt-20 pb-10 text-center space-y-10">
      <!-- Glow decorativo de fundo -->
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-brand-purple/20 blur-[120px] -z-10 rounded-full"></div>

      <div class="space-y-6">
        <span class="inline-block bg-brand-purple/10 border border-brand-purple/30 text-brand-purple px-4 py-2 rounded-full text-xs font-black tracking-[0.2em] uppercase">
          A Evolução da Interação
        </span>
        <h1 class="text-6xl md:text-9xl font-black italic tracking-tighter leading-[0.85] uppercase">
          Sua live, <br/>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-purple to-brand-neon">suas regras.</span>
        </h1>
        <p class="text-brand-gray text-lg md:text-xl max-w-2xl mx-auto font-medium">
          Monetize sua stream permitindo que seus viewers paguem para jogar com você. 
          Filas em tempo real, pagamentos automáticos e controle total.
        </p>
      </div>

      <div class="flex flex-col md:flex-row items-center justify-center gap-6">
        <router-link to="/dashboard" class="group relative px-10 py-5 bg-brand-purple rounded-2xl font-black text-xl transition-all hover:scale-105 shadow-[0_0_30px_rgba(124,58,237,0.4)]">
          CRIAR MINHA FILA
          <div class="absolute inset-0 rounded-2xl bg-white opacity-0 group-hover:opacity-20 transition-opacity"></div>
        </router-link>
        <a href="#buscar" class="px-10 py-5 bg-white/5 border border-white/10 rounded-2xl font-black text-xl hover:bg-white/10 transition-all">
          ENCONTRAR STREAMER
        </a>
      </div>
    </section>

    <!-- FEATURES SECTION -->
    <section class="grid grid-cols-1 md:grid-cols-3 gap-8 px-4">
      <div class="p-10 bg-brand-surface border border-white/5 rounded-[3rem] space-y-4">
        <div class="text-4xl">⚡</div>
        <h3 class="text-xl font-black uppercase tracking-tighter">Tempo Real</h3>
        <p class="text-brand-gray leading-relaxed text-sm">Nada de F5. Acompanhe sua posição na fila com latência zero.</p>
      </div>
      <div class="p-10 bg-brand-surface border border-white/5 rounded-[3rem] space-y-4 shadow-xl">
        <div class="text-4xl">💰</div>
        <h3 class="text-xl font-black uppercase tracking-tighter">Pix Instantâneo</h3>
        <p class="text-brand-gray leading-relaxed text-sm">O dinheiro cai, a vaga é liberada na hora.</p>
      </div>
      <div class="p-10 bg-brand-surface border border-white/5 rounded-[3rem] space-y-4">
        <div class="text-4xl">🛡️</div>
        <h3 class="text-xl font-black uppercase tracking-tighter">Estorno Seguro</h3>
        <p class="text-brand-gray leading-relaxed text-sm">O streamer não te chamou? O sistema processa o estorno automaticamente.</p>
      </div>
    </section>

    <!-- SEARCH SECTION (O que tínhamos antes) -->
    <section id="buscar" class="space-y-16 py-20 bg-brand-surface/30 rounded-[4rem] border border-white/5 px-6">
      <div class="text-center space-y-4">
        <h2 class="text-4xl md:text-6xl font-black italic tracking-tighter">QUEM ESTÁ <span class="text-brand-neon">ON-LINE?</span></h2>
        <p class="text-brand-gray">Busque por nicks ou jogos e entre na ação agora mesmo.</p>
      </div>

      <div class="max-w-3xl mx-auto relative group">
        <input 
          v-model="searchQuery"
          @input="handleSearch"
          type="text"
          placeholder="Ex: CS, Valorant..."
          class="w-full bg-brand-black border-2 border-white/5 p-6 rounded-[2rem] focus:border-brand-purple focus:outline-none transition-all text-xl shadow-inner"
        />
        <button class="absolute right-4 top-1/2 -translate-y-1/2 bg-brand-purple p-3 rounded-2xl font-black text-xs">
          BUSCAR
        </button>
      </div>

      <!-- Resultados -->
      <div v-if="results.length" class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div v-for="res in results" :key="res.queue_id" 
          class="bg-brand-black border border-white/5 p-8 rounded-[2.5rem] hover:border-brand-purple/50 transition-all group">
          <div class="flex items-center gap-4 mb-6">
            <div class="w-12 h-12 rounded-2xl bg-brand-purple flex items-center justify-center font-black">
              {{ res.display_name?.charAt(0) }}
            </div>
            <div>
              <h3 class="font-bold">{{ res.display_name }}</h3>
              <span v-if="res.is_live" class="text-[10px] text-brand-neon font-black uppercase tracking-widest">Live Ativa</span>
              <span v-else class="text-[10px] text-brand-gray font-black uppercase tracking-widest">Offline</span>
            </div>
          </div>
          <p class="text-brand-gray text-sm mb-8 h-10 line-clamp-2">{{ res.queue_title }}</p>
          <router-link :to="'/queue/' + res.queue_id" class="block w-full py-4 rounded-xl bg-white/5 group-hover:bg-brand-purple text-center font-black transition-all">
            ENTRAR NA FILA
          </router-link>
        </div>
      </div>
      
      <div v-else-if="searchQuery.length >= 2" class="text-center text-brand-gray italic">
        Nenhum streamer encontrado para "{{ searchQuery }}"
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="text-center text-brand-gray text-xs font-bold uppercase tracking-[0.3em] pb-10">
      Fast Queue © 2026 - O próximo nível da sua stream.
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '@/api'

const searchQuery = ref('')
const results = ref<any[]>([])

const handleSearch = async () => {
  if (searchQuery.value.length < 2) {
    results.value = []
    return
  }
  try {
    const { data } = await api.get(`/search?q=${searchQuery.value}`)
    results.value = data.results
  } catch (e) {
    console.error(e)
  }
}
</script>