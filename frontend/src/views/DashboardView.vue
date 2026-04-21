<template>
  <div v-if="loadingQueue" class="flex justify-center py-20">
    <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-brand-purple"></div>
  </div>
  <div class="max-w-5xl mx-auto px-2 md:px-4 space-y-6 md:space-y-10 pb-20">
    <!-- Header -->
    <header class="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
      <div>
        <h1 class="text-3xl md:text-4xl font-black italic tracking-tighter">DASHBOARD</h1>
        <p class="text-brand-gray text-sm md:text-lg font-medium">Gerencie suas sessões de jogo.</p>
      </div>
    </header>

    <!-- ESTADO: SEM FILA ATIVA -->
    <section v-if="!activeQueue"
      class="bg-brand-surface border border-white/5 p-6 md:p-10 rounded-[2rem] md:rounded-[2.5rem] shadow-2xl">
      <div class="mx-auto md:mx-0  text-center md:text-left">
        <h2 class="text-2xl font-bold mb-6 flex items-center gap-2">
          <span class="text-brand-purple">⚡</span> Criar Nova Fila
        </h2>
        <form @submit.prevent="handleCreateQueue" class="space-y-5">
          <div class="space-y-2">
            <label class="block text-[10px] font-black uppercase tracking-widest text-brand-purple">Título da
              Partida</label>
            <input v-model="form.title" type="text" placeholder="Ex: Jogando Ranqueada com Subs"
              class="w-full bg-brand-black border border-white/10 p-4 rounded-xl focus:border-brand-purple outline-none transition-all"
              required />
          </div>
          <div class="space-y-2">
            <label class="block text-[10px] font-black uppercase tracking-widest text-brand-purple">Valor de Entrada
              (R$)</label>
            <input v-model.number="form.entry_fee_brl" type="number" step="0.01"
              class="w-full bg-brand-black border border-white/10 p-4 rounded-xl focus:border-brand-purple outline-none transition-all"
              required />
          </div>
          <button :disabled="loading" type="submit"
            class="cursor-pointer w-full bg-brand-purple py-4 rounded-xl font-black text-lg hover:scale-[1.02] active:scale-95 transition-all shadow-lg shadow-brand-purple/20 disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-3">
            <svg v-if="loading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>

            {{ loading ? 'CRIANDO...' : 'ABRIR FILA AGORA' }}
          </button>
        </form>
      </div>
    </section>

    <!-- ESTADO: FILA ATIVA -->
    <section v-else class="grid grid-cols-1 lg:grid-cols-12 gap-6 md:gap-8">

      <!-- LADO ESQUERDO: CONTROLES E LISTA -->
      <div class="lg:col-span-12 space-y-6">

        <!-- CARD DE CONTROLE PRINCIPAL -->
        <div
          class="bg-brand-surface border border-brand-purple/30 p-6 md:p-8 rounded-[2rem] relative overflow-hidden shadow-2xl">
          <div class="relative z-10 flex flex-col md:flex-row justify-between gap-6">
            <div class="space-y-1">
              <span
                class="bg-brand-neon text-black text-[9px] font-black px-2 py-0.5 rounded uppercase tracking-tighter">Fila
                Ativa</span>
              <h2 class="text-2xl md:text-3xl font-black truncate max-w-xs md:max-w-md">{{ activeQueue.title }}</h2>
              <p class="text-brand-gray text-sm font-bold">Taxa: <span class="text-white">R$ {{ (activeQueue.entry_fee /
                100).toFixed(2) }}</span></p>
            </div>

            <button :disabled="loading" @click="handleCallNext"
              class="cursor-pointer w-full md:w-auto md:px-12 min-w-[220px] py-4 rounded-2xl font-black text-lg bg-brand-purple shadow-xl shadow-brand-purple/30 hover:bg-opacity-90 active:scale-95 transition-all disabled:opacity-70 disabled:cursor-not-allowed inline-flex items-center justify-center gap-3">
              <svg v-if="loading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>

              {{ loading ? 'PROCESSANDO...' : 'CHAMAR PRÓXIMO' }}
            </button>
          </div>
        </div>

        <!-- BOTÕES DE GESTÃO (WRAP NO MOBILE) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 md:flex gap-3">
          <button @click="toggleQueueStatus" :disabled="loading" :class="activeQueue.status === 'OPEN'
            ? 'bg-orange-500/10 text-orange-500 border-orange-500/30'
            : 'bg-brand-neon/10 text-brand-neon border-brand-neon/30'"
            class="cursor-pointer flex-1 min-w-[220px] border px-6 py-4 rounded-xl font-black text-xs uppercase tracking-widest transition-all hover:bg-opacity-20 disabled:opacity-70 disabled:cursor-not-allowed inline-flex items-center justify-center gap-3">
            <svg class="h-4 w-4 animate-spin" :class="loading ? 'opacity-100' : 'opacity-0'"
              xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>

            <span>
              {{
                loading
                  ? 'PROCESSANDO...'
                  : activeQueue.status === 'OPEN'
                    ? 'PAUSAR ENTRADAS'
              : 'REABRIR FILA'
              }}
            </span>
          </button>

          <button @click="showEditModal = true" :disabled="true"
            class="bg-white/5 border border-white/10 px-6 py-4 rounded-xl font-black text-xs uppercase tracking-widest hover:bg-white/10 transition-all">
            CONFIGURAÇÕES
          </button>

          <button :disabled="loading" @click="deleteQueue"
              class="cursor-pointer min-w-[220px] bg-red-500/10 border border-red-500/30 text-red-500 px-6 py-4 rounded-xl font-black text-xs uppercase tracking-widest hover:bg-red-500 hover:text-white transition-all inline-flex items-center justify-center gap-3">
              <svg v-if="loading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>

              {{ loading ? 'PROCESSANDO...' : 'ENCERRAR TUDO' }}
            </button>
        </div>
        <transition name="fade">
          <div v-if="currentPlayer" class="relative group">
            <!-- Glow de fundo animado -->
            <div
              class="absolute -inset-1 bg-gradient-to-r from-brand-purple to-brand-neon rounded-[2.5rem] blur opacity-25 group-hover:opacity-50 transition duration-1000">
            </div>

            <div
              class="relative bg-brand-surface border border-white/10 p-8 rounded-[2.5rem] shadow-2xl overflow-hidden">
              <div class="flex flex-col md:flex-row items-center justify-between gap-8">

                <!-- Info do Player -->
                <div class="flex items-center gap-6">
                  <div class="relative">
                    <div
                      class="w-20 h-20 bg-brand-purple rounded-3xl flex items-center justify-center text-3xl font-black shadow-2xl">
                      {{ currentPlayer.game_nick?.charAt(0) }}
                    </div>
                    <!-- Badge Online -->
                    <div
                      class="absolute -bottom-1 -right-1 w-6 h-6 bg-brand-neon border-4 border-brand-surface rounded-full animate-pulse">
                    </div>
                  </div>

                  <div class="text-center md:text-left">
                    <p class="text-brand-neon text-[10px] font-black uppercase tracking-[0.2em] mb-1">Jogando Agora</p>
                    <h2 class="text-4xl font-black text-white italic tracking-tighter uppercase leading-none mb-2">
                      {{ currentPlayer.game_nick }}
                    </h2>
                    <p class="text-brand-gray font-bold flex items-center gap-2 justify-center md:justify-start">
                      <span class="text-brand-purple">@</span> {{ currentPlayer.social_handle || 'Sem rede social' }}
                    </p>
                  </div>
                </div>

                <div class="flex flex-wrap justify-center gap-3 w-full md:w-auto">
                  <button @click="copyNick(currentPlayer.game_nick)"
                    class="cursor-pointer flex-1 md:flex-none flex items-center justify-center gap-3 px-8 py-4 bg-white text-black rounded-2xl font-black hover:bg-brand-neon transition-all active:scale-95">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
                      <path
                        d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
                    </svg>
                    COPIAR NICK
                  </button>

                  <button v-if="currentPlayer.social_handle" @click="copyNick(currentPlayer.social_handle)"
                    class="cursor-pointer flex-1 md:flex-none flex items-center justify-center gap-3 px-8 py-4 bg-white/5 border border-white/10 rounded-2xl font-black hover:bg-white/10 transition-all active:scale-95">
                    COPIAR SOCIAL
                  </button>
                </div>
              </div>
            </div>
          </div>
        </transition>

        <!-- LISTA DE ESPERA -->
        <div
          class="bg-brand-surface border border-white/5 p-6 md:p-8 rounded-[2rem] shadow-2xl relative overflow-hidden">
          <div class="absolute -top-24 -right-24 w-48 h-48 bg-brand-purple/5 blur-[80px] -z-0"></div>

          <div class="flex items-center justify-between mb-8 relative z-10">
            <h3 class="text-xl md:text-2xl font-black italic tracking-tighter">LISTA DE ESPERA</h3>
            <span
              class="bg-white/5 px-4 py-1 rounded-full text-[10px] font-black text-brand-gray uppercase tracking-widest border border-white/5">
              {{queueStore.entries.filter(e => e.status === 'WAITING').length}} Players
            </span>
          </div>

          <TransitionGroup name="list" tag="div" class="space-y-3 relative z-10">
            <div v-if="queueStore.entries.length === 0" key="empty"
              class="text-center py-12 border-2 border-dashed border-white/5 rounded-3xl">
              <div class="text-3xl mb-2">🎮</div>
              <p class="text-brand-gray text-sm font-bold italic uppercase tracking-tighter">Aguardando desafiantes...
              </p>
            </div>

            <div v-for="(entry, index) in queueStore.entries.filter(e => e.status === 'WAITING')" :key="entry.id"
              class="group flex items-center justify-between p-4 md:p-5 bg-brand-black/40 border border-white/5 rounded-2xl hover:border-brand-purple/40 transition-all"
              :class="{ 'border-brand-neon/40 bg-brand-neon/[0.02]': index === 0 }">
              <div class="flex items-center gap-4">
                <!-- Posição Real-time -->
                <div
                  class="w-10 h-10 md:w-12 md:h-12 rounded-xl bg-brand-surface border border-white/10 flex items-center justify-center font-black text-base md:text-lg">
                  <span :class="index === 0 ? 'text-brand-neon' : 'text-white'">{{ index + 1 }}</span>
                </div>

                <div class="flex flex-col min-w-0">
                  <div class="flex items-center gap-2">
                    <span class="font-black text-base md:text-xl truncate">{{ entry.game_nick }}</span>
                    <span v-if="index === 0"
                      class="hidden sm:inline text-[8px] bg-brand-neon text-black px-1.5 py-0.5 rounded font-black uppercase">Next</span>
                  </div>
                  <span class="text-[10px] md:text-xs font-bold text-brand-gray uppercase truncate">
                    <span class="text-brand-purple">@</span>{{ entry.social_handle || 'N/A' }}
                  </span>
                </div>
              </div>

              <div class="flex items-center gap-2">
                <button @click="copyNick(entry.game_nick)"
                  class="cursor-pointer flex items-center gap-2 p-3 md:px-4 md:py-2 bg-white/5 hover:bg-brand-purple rounded-xl font-bold text-[10px] transition-all">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                  </svg>
                  <span class="hidden md:inline">COPIAR NICK</span>
                </button>

                <button @click="handleReject(entry.id)"
                  class="cursor-pointer p-3 bg-red-500/5 hover:bg-red-500 text-red-500 hover:text-white rounded-xl transition-all">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </TransitionGroup>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'
import { useQueueStore } from '@/stores/queue'
import { useRouter } from 'vue-router'
import { useUIStore } from '@/stores/ui'

const ui = useUIStore()
const authStore = useAuthStore()
const queueStore = useQueueStore()
const activeQueue = ref<any>(null)
const entries = ref<any[]>([])
const loading = ref(false)
const showEditModal = ref(false)
const router = useRouter()
const loadingQueue = ref(true)

const currentPlayer = computed(() => {
  return queueStore.entries.find(e => e.status === 'CALLED')
})

const toggleQueueStatus = async () => {
  const newStatus = activeQueue.value.status === 'OPEN' ? 'CLOSED' : 'OPEN';
  try {
    loading.value = true
    const { data } = await api.patch(`/queues/${activeQueue.value.id}`, { status: newStatus });
    activeQueue.value = data;
  } catch (e) { 
    ui.notify("Erro ao mudar status", "error");
  } finally { 
    loading.value = false; 
  }
};

const deleteQueue = async () => {
  if (!confirm("ISSO IRÁ REEMBOLSAR TODOS E EXCLUIR A FILA. Tem certeza?")) return;

  try {
    loading.value = true
    await api.delete(`/queues/${activeQueue.value.id}`);
    activeQueue.value = null;
    queueStore.stopListening()
    ui.notify("Fila encerrada com sucesso!", "success");
  } catch (e) {
    ui.notify("Erro ao deletar", "error"); 
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  try {
    loadingQueue.value = true
    const { data: allQueues } = await api.get('/queues/')
    if (allQueues.length === 0) return
    activeQueue.value = allQueues[0]
    queueStore.listenToQueue(allQueues[0].id)
  } catch (e) {
    ui.notify("Erro ao carregar fila ativa. Tente recarregar a página.", "error")
  } finally {
    loadingQueue.value = false
  }
})

const form = ref({ title: '', entry_fee_brl: 5.0, max_slots: 10 });

const handleCreateQueue = async () => {
  try {
    loading.value = true
    const { data } = await api.post('/queues/', {
      title: form.value.title,
      entry_fee: Math.round(form.value.entry_fee_brl * 100),
      max_slots: form.value.max_slots,
      streamer_id: authStore.dbUser.id
    });
    activeQueue.value = data;
    queueStore.listenToQueue(data.id);
  } catch (e) {
    ui.notify("Erro ao criar fila. Verifique se já não existe uma aberta.", "error");
  } finally {
    loading.value = false
  }
};
watch(() => activeQueue.value, (newQueue) => {
  if (newQueue && newQueue.id) {
    queueStore.listenToQueue(newQueue.id)
  }
})

onUnmounted(() => {
  queueStore.stopListening()
})

const handleCallNext = async () => {
  try {
    loading.value = true
    await api.post(`/queues/${activeQueue.value.id}/next`)
  } catch (e) {
    ui.notify("Não há ninguém na fila!", "info")
  } finally {
    loading.value = false
  }
}

const handleReject = async (entryId: number) => {
  if (!confirm("Isso irá remover o viewer e solicitar o estorno do Pix. Confirmar?")) return;

  try {
    await api.post(`/queues/${activeQueue.value.id}/reject/${entryId}`);
  } catch (e) {
    ui.notify("Erro ao rejeitar viewer.", "error");
  }
};

const copyNick = (nick: string) => {
  navigator.clipboard.writeText(nick);
  if (navigator.vibrate) navigator.vibrate(50);
  ui.notify(`Nick ${nick} copiado para a área de transferência!`, "success");
};
</script>
<style>
.list-enter-active,
.list-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.list-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.list-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.list-move {
  transition: transform 0.5s ease;
}
</style>