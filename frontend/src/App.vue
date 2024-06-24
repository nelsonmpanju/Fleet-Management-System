<template>
  <div>
    <router-view />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const isUserLoggedIn = ref(false); 
</script>