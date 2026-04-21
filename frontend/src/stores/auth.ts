import { defineStore } from 'pinia'
import { auth } from '@/services/firebase'
import { 
  onAuthStateChanged, 
  signInWithPopup, 
  GoogleAuthProvider, 
  signOut,
  type User 
} from 'firebase/auth'
import api from '@/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    dbUser: null as any,
    token: '' as string,
    loading: true,
    needsOnboarding: false
  }),

  actions: {
    async updateDisplayName(newName: string) {
      try {
        const { data } = await api.put('/queues/users/me', { display_name: newName });
        this.dbUser = data;
        this.needsOnboarding = false;
        return data;
      } catch (error) {
        console.error("Erro ao salvar nome:", error);
        throw error;
      }
    },
    async init() {
      if (!this.loading) return
      
      return new Promise((resolve) => {
        onAuthStateChanged(auth, async (user) => {
          this.user = user
          if (user) {
            this.token = await user.getIdToken()
            await this.syncUser()
          }
          this.loading = false
          resolve(user)
        })
      })
    },

    async loginWithGoogle() {
      const provider = new GoogleAuthProvider()
      await signInWithPopup(auth, provider)
    },

    async logout() {
      await signOut(auth)
      this.user = null
      this.dbUser = null
      this.token = ''
    },

    async syncUser() {
      try {
        const { data } = await api.get('/queues/users/me')
        this.dbUser = data
        this.needsOnboarding = !data.display_name
      } catch (error) {
        console.error("Erro ao sincronizar usuário com o backend:", error)
      }
    }
  }
})