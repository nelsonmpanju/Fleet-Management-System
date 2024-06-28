<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-md">
      <form class="space-y-6" @submit.prevent="login">
        <h5 class="text-2xl font-medium text-gray-900">Sign in to MPANJU</h5>
        <div>
          <label for="email" class="block mb-2 text-sm font-medium text-gray-900">User ID</label>
          <input v-model="email" type="email" name="email" id="email" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" placeholder="johndoe@email.com" required />
        </div>
        <div>
          <label for="password" class="block mb-2 text-sm font-medium text-gray-900">Password</label>
          <input v-model="password" type="password" name="password" id="password" placeholder="••••••" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" required />
        </div>
        <button type="submit" class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">Login</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store';

const email = ref('');
const password = ref('');
const router = useRouter();
const authStore = useAuthStore();

const login = async () => {
  try {
    await authStore.login(email.value, password.value);
    router.push('/home');
  } catch (error) {
    alert(error.message);
  }
};
</script>

<!-- <style scoped>
body {
  @apply bg-gray-100;
}
</style> -->
