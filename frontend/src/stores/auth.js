import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(username, password) {
      try {
        const params = new URLSearchParams();
        params.append('username', username);
        params.append('password', password);

        const response = await axios.post('/auth/token', params);

        this.token = response.data.access_token;
        localStorage.setItem('token', this.token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
        this.router.push('/');
      } catch (error) {
        console.error('Login failed:', error);
        throw error;
      }
    },
    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('token');
      delete axios.defaults.headers.common['Authorization'];
      this.router.push('/login');
    },
    async register(username, password) {
        try {
            const params = new URLSearchParams();
            params.append('username', username);
            params.append('password', password);
            await axios.post('/auth/register', params);
            // After successful registration, log the user in
            await this.login(username, password);
        } catch (error) {
            console.error('Registration failed:', error);
            throw error;
        }
    }
  },
})
