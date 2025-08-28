<template>
  <div class="login-container">
    <div class="login-box">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="p-field">
          <label for="username">Username</label>
          <InputText id="username" v-model="username" type="text" />
        </div>
        <div class="p-field">
          <label for="password">Password</label>
          <InputText id="password" v-model="password" type="password" />
        </div>
        <Button label="Login" type="submit" :loading="loading" />
        <Button label="Register" @click="handleRegister" :loading="loading" class="p-button-secondary" />
      </form>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';

const username = ref('');
const password = ref('');
const error = ref(null);
const loading = ref(false);
const authStore = useAuthStore();

const handleLogin = async () => {
  loading.value = true;
  error.value = null;
  try {
    await authStore.login(username.value, password.value);
  } catch (err) {
    error.value = 'Failed to login. Please check your credentials.';
  } finally {
    loading.value = false;
  }
};

const handleRegister = async () => {
  loading.value = true;
  error.value = null;
  try {
    await authStore.register(username.value, password.value);
  } catch (err) {
    error.value = 'Failed to register. The username might already be taken.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.login-box {
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 300px;
}
.p-field {
  margin-bottom: 1rem;
}
.p-field label {
  display: block;
  margin-bottom: 0.5rem;
}
.p-field input {
  width: 100%;
}
.error {
    color: red;
    margin-top: 1rem;
}
</style>
