import { defineStore } from 'pinia'
import { db } from '@/services/firebase'
import { collection, query, where, onSnapshot, orderBy } from 'firebase/firestore'

export const useQueueStore = defineStore('queue', {
  state: () => ({
    activeQueue: null as any,
    entries: [] as any[],
    unsubscribe: null as (() => void) | null
  }),

  actions: {
    listenToQueue(queueId: string | number) {
      if (this.unsubscribe) this.unsubscribe()

      const q = query(
        collection(db, 'active_queues', String(queueId), 'entries'),
        where('status', 'in', ['WAITING', 'CALLED']),
        orderBy('position', 'asc')
      )

      this.unsubscribe = onSnapshot(q, (snapshot) => {
        this.entries = snapshot.docs.map(doc => ({
          id: doc.id,
          ...doc.data()
        }))
        console.log("🔥 Firestore atualizado:", this.entries)
      }, (error) => {
        console.error("Erro no listener do Firestore:", error)
      })
    },

    stopListening() {
      if (this.unsubscribe) {
        this.unsubscribe()
        this.unsubscribe = null
      }
    }
  }
})