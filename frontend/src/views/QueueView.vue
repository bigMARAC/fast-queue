<template>
  <div v-if="loading" class="flex justify-center py-20">
    <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-brand-purple"></div>
  </div>

  <div v-else-if="queue" class="max-w-3xl mx-auto py-10 space-y-8">
    <!-- Header do Streamer -->
    <div class="bg-brand-surface border border-white/5 p-10 rounded-[2.5rem] text-center space-y-4">
      <div
        class="w-20 h-20 bg-brand-purple rounded-3xl mx-auto flex items-center justify-center text-3xl font-black shadow-2xl">
        {{ queue.streamer_name?.charAt(0) }}
      </div>
      <h1 class="text-3xl font-black">{{ queue.streamer_name }}</h1>
      <p class="text-brand-gray">{{ queue.title }}</p>

      <div class="pt-6">
        <span class="text-5xl font-black text-white">R$ {{ (queue.entry_fee / 100).toFixed(2) }}</span>
        <p class="text-brand-neon text-xs font-bold uppercase mt-2">Taxa única de entrada</p>
      </div>
    </div>

    <!-- Ação: Entrar ou Acompanhar -->
    <div class="bg-brand-surface border border-white/5 p-8 rounded-[2.5rem]">
      <!-- Caso 1: Usuário não está na fila -->
      <div v-if="!myEntry" class="space-y-6 text-center">
        <div class="space-y-4 text-left mb-6">
          <div>
            <label class="text-xs font-black text-brand-purple uppercase">Seu Nick no Jogo *</label>
            <input v-model="joinForm.game_nick" placeholder="Ex: MaracBot#BR1"
              class="w-full bg-brand-black p-4 rounded-xl border border-white/5" />
          </div>
          <div>
            <label class="text-xs font-black text-brand-purple uppercase">Rede Social (Opcional)</label>
            <input v-model="joinForm.social_handle" placeholder="Ex: @twitter_user"
              class="w-full bg-brand-black p-4 rounded-xl border border-white/5" />
          </div>
        </div>
        <h3 class="text-xl font-bold">Pronto para a partida?</h3>
        <p class="text-brand-gray">Ao clicar no botão abaixo, você será redirecionado para o pagamento via Pix.</p>
        <button @click="handleJoinQueue" :disabled="joining || queue.status !== 'OPEN'"
          class="w-full bg-brand-purple py-5 rounded-2xl font-black text-xl hover:scale-[1.02] transition-all disabled:opacity-50">
          {{ joining ? 'PROCESSANDO...' : 'ENTRAR NA FILA AGORA' }}
        </button>
      </div>

      <!-- Caso 2: Usuário já pagou e está na fila -->
      <div v-else class="text-center space-y-6">
        <div v-if="myEntry.status === 'REJECTED'"
          class="space-y-6 p-8 bg-red-500/10 border border-red-500/20 rounded-[2rem]">
          <div class="text-5xl">💸</div>
          <h3 class="text-2xl font-black text-red-500 uppercase italic">Entrada Recusada</h3>
          <p class="text-brand-gray text-sm">
            O streamer recusou sua entrada. <br />
            O estorno do seu Pix foi solicitado e cairá em breve.
          </p>
          <button @click="myEntry = null" class="bg-white/5 px-6 py-2 rounded-xl font-bold text-xs">
            TENTAR NOVAMENTE
          </button>
        </div>
        <div v-else-if="['WAITING', 'CALLED'].includes(myEntry.status)">
          <div class="inline-block bg-brand-neon/10 text-brand-neon px-4 py-2 rounded-full font-bold text-sm mb-4">
            VOCÊ ESTÁ NA FILA!
          </div>
          <div class="text-7xl font-black text-white leading-none">
            #{{ peopleAhead + 1 }}
          </div>
          <p class="text-brand-gray">Pessoas na sua frente: {{ peopleAhead }}</p>
          <div v-if="myEntry.status === 'CALLED'"
            class="bg-brand-neon text-black p-6 rounded-2xl font-black text-xl animate-bounce">
            É A SUA VEZ! FIQUE ATENTO AO DISCORD/STREAM
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="showPixModal"
    class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-[100] p-4">
    <div
      class="bg-brand-surface border border-white/10 p-8 rounded-[2.5rem] max-w-sm w-full text-center space-y-6 shadow-2xl">
      <h3 class="text-2xl font-black">PAGAMENTO PIX</h3>

      <!-- QR Code -->
      <div class="bg-white p-4 rounded-3xl inline-block mx-auto">
        <img :src="pixData.brCodeBase64" alt="QR Code Pix" class="w-48 h-48" />
      </div>

      <div class="space-y-4">
        <p class="text-brand-gray text-sm">Escaneie o QR Code ou copie o código abaixo para pagar.</p>

        <button @click="copyPix"
          class="w-full bg-white/5 hover:bg-white/10 p-4 rounded-xl text-xs font-mono break-all border border-white/5 transition-all">
          {{ pixData.brCode }}
        </button>
      </div>

      <button @click="showPixModal = false" class="text-brand-gray font-bold hover:text-white transition-all">
        FECHAR
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { db } from '@/services/firebase'
import { doc, onSnapshot, collection, query, where, orderBy, limit } from 'firebase/firestore'
import api from '@/api'
import { useUIStore } from '@/stores/ui'

const route = useRoute()
const authStore = useAuthStore()

const queue = ref<any>(null)
const loading = ref(true)
const joining = ref(false)
const myEntry = ref<any>(null)
const showPixModal = ref(false)
const pixData = ref({ brCode: '', brCodeBase64: '' })
const peopleAhead = ref(0);
let unsubscribeAhead: any = null
const ui = useUIStore()

const fetchQueue = async () => {
  try {
    loading.value = true
    const { data } = await api.get(`/queues/${route.params.id}`)
    queue.value = data
    checkMyEntry()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const checkMyEntry = () => {
  if (!authStore.user) return

  const q = query(
    collection(db, 'active_queues', String(route.params.id), 'entries'),
    where('viewer_id', '==', authStore.user.uid),
    orderBy('created_at', 'desc'),
    limit(1)
  )

  onSnapshot(q, (snapshot) => {
    if (!snapshot.empty) {
      const entryData = snapshot.docs[0].data()
      myEntry.value = entryData

      console.log("📡 [FIRESTORE] Dados recebidos:", entryData)

      if (entryData.status === 'WAITING' && entryData.position > 0) {

        if (unsubscribeAhead) unsubscribeAhead()

        const qAhead = query(
          collection(db, 'active_queues', String(route.params.id), 'entries'),
          where('status', '==', 'WAITING'),
          where('position', '<', entryData.position)
        )

        unsubscribeAhead = onSnapshot(qAhead, (snapAhead) => {
          peopleAhead.value = snapAhead.size
          console.log(`👥 Atualizado: ${snapAhead.size} pessoas na frente`)
        })
      }

      if (entryData.status === 'CALLED') {
        peopleAhead.value = 0
        if (unsubscribeAhead) unsubscribeAhead()
      }

      const currentStatus = entryData.status?.toUpperCase()

      if (currentStatus === 'WAITING' || currentStatus === 'CALLED') {
        console.log("✅ Pagamento confirmado! Fechando modal automaticamente.")
        showPixModal.value = false
      }
    }
  }, (error) => {
    console.error("❌ Erro no listener do Firestore:", error)
  })
}

const joinForm = ref({ game_nick: '', social_handle: '' });

const handleJoinQueue = async () => {
  if (!joinForm.value.game_nick) return ui.notify("Nick no jogo é obrigatório!", "info");

  try {
    joining.value = true;
    const { data } = await api.post(`/queues/${queue.value.id}/join`, {
      game_nick: joinForm.value.game_nick,
      social_handle: joinForm.value.social_handle
    });
    pixData.value = data;
    console.log("Dados do Pix recebidos:", pixData.value);
    showPixModal.value = true;
  } catch (e) {
    ui.notify("Erro ao entrar na fila.", "error");
  } finally {
    joining.value = false;
  }
};

watch(() => myEntry.value?.status, (newStatus) => {
  if (newStatus === 'WAITING' || newStatus === 'CALLED') {
    showPixModal.value = false;
  }
});

const copyPix = () => {
  navigator.clipboard.writeText(pixData.value.brCode)
  ui.notify("Código Pix copiado!", "success")
}

onMounted(fetchQueue)
onUnmounted(() => {
  if (unsubscribeAhead) unsubscribeAhead()
})
</script>