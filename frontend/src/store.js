import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false,
  }),
  actions: {
    login(email, password) {
      if (email === 'user@example.com' && password === 'password') {
        this.isLoggedIn = true;
        localStorage.setItem('isLoggedIn', 'true');
      } else {
        throw new Error('Invalid credentials');
      }
    },
    logout() {
      this.isLoggedIn = false;
      localStorage.removeItem('isLoggedIn');
    },
    checkLogin() {
      this.isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    }
  },
});
