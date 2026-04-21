import { defineStore } from 'pinia'

export const useUIStore = defineStore('ui', {
  state: () => ({
    snackbar: {
      show: false,
      message: '',
      type: 'success' as 'success' | 'error' | 'info'
    }
  }),
  actions: {
    notify(message: string, type: 'success' | 'error' | 'info' = 'success') {
      this.snackbar.message = message
      this.snackbar.type = type
      this.snackbar.show = true
      
      setTimeout(() => {
        this.snackbar.show = false
      }, 3000)
    }
  }
})