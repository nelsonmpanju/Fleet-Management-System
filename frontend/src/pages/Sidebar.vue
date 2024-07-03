<template>
  <div class="flex">
    <!-- Fixed vertical navigation -->
    <nav aria-label="Options" class="fixed top-0 left-0 z-20 flex flex-col items-center h-screen py-5 pt-20 bg-white">
      <div class="flex flex-col items-center flex-1 p-4 space-y-4 bg-white-100 w-full">
        <!-- Menu button -->
        <Button @click="toggleSidebar('linksTab')" 
                class="p-3 w-full transition-colors duration-300 rounded-lg shadow-md hover:bg-indigo-800 hover:text-white focus:outline-none focus:ring focus:ring-indigo-600 focus:ring-offset-2"
                :class="sidebarStore.isOpen && sidebarStore.currentTab == 'linksTab' ? 'text-white bg-indigo-600' : 'text-gray-500 bg-white'">
          <svg aria-hidden="true" class="w-6 h-6 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" />
          </svg>
        </Button>
        <!-- Messages button -->
        <Button @click="handleFetchDocTypes('Truck')" 
                class="p-3 w-full transition-colors duration-300 rounded-lg shadow-md hover:bg-indigo-800 hover:text-white focus:outline-none focus:ring focus:ring-indigo-600 focus:ring-offset-2"
                :class="sidebarStore.isOpen && sidebarStore.currentTab == 'messagesTab' ? 'text-white bg-indigo-900' : 'text-gray-500 bg-gray-100'">
          <svg aria-hidden="true" class="w-6 h-6 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        </Button>
        <!-- Notifications button -->
        <Button @click="toggleSidebar('notificationsTab')" 
                class="p-3 w-full transition-colors duration-300 rounded-lg shadow-md hover:bg-indigo-800 hover:text-white focus:outline-none focus:ring focus:ring-indigo-600 focus:ring-offset-2"
                :class="sidebarStore.isOpen && sidebarStore.currentTab == 'notificationsTab' ? 'text-white bg-indigo-600' : 'text-gray-500 bg-white'">
          <svg aria-hidden="true" class="w-6 h-6 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
        </Button>
      </div>
    </nav>

    <!-- Sidebar -->
    <aside
      v-if="sidebarStore.isOpen"
      :class="[
        'fixed top-0 ml-[80px] z-40 w-64 h-screen pt-20 transition-transform bg-white border-r border-gray-200',
        sidebarStore.isOpen ? 'translate-x-0' : '-translate-x-full',
      ]"
      aria-label="Sidebar"
    >
      <div class="px-3 pb-4">
        <!-- Search Form -->
        <form class="relative mb-4" @submit.prevent="search">
          <div class="relative">
            <div class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none">
              <svg
                class="w-5 h-5 text-gray-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                ></path>
              </svg>
            </div>
            <input
              v-model="sidebarStore.searchQuery"
              type="search"
              id="search-sidebar"
              class="block w-full pl-10 p-2.5 text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Search..."
              required
            />
          </div>
        </form>
        <!-- Navigation Menu -->
        <ul class="space-y-2 font-medium overflow-y-auto">
          <li v-for="item in filteredItems" :key="item.name" class="flex items-center justify-between">
            <a class="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group">
              <span class="ms-3">{{ item.name }}</span>
              <Badge :variant="'solid'" :theme="gray" size="sm" label="Badge">
                {{ item.status }}
              </Badge>
            </a>
              <Badge  size="l" label="Badge">
                {{ item.status }}
              </Badge>
          </li>
        </ul>

      </div>
    </aside>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Badge, Button } from 'frappe-ui';
import { useSidebarStore } from '@/store';
import { fetchDocTypes } from '@/utils';

const sidebarStore = useSidebarStore();

const toggleSidebar = (tab) => {
  if (sidebarStore.currentTab === tab) {
    sidebarStore.isOpen = !sidebarStore.isOpen;
  } else {
    sidebarStore.currentTab = tab;
    sidebarStore.isOpen = true;
  }
};

const handleFetchDocTypes = async (doc) => {
  await fetchDocTypes(doc, sidebarStore);
  toggleSidebar('messagesTab'); // Ensure the main sidebar is open and switched to the messages tab
};

const filteredItems = computed(() => {
  return sidebarStore.docTypes.filter((item) =>
    item.name.toLowerCase().includes(sidebarStore.searchQuery.toLowerCase())
  );
});

const search = () => {
  console.log('Search query:', sidebarStore.searchQuery);
};

const colorMap = {
  Draft: 'gray',
  Pending: 'yellow',
  Completed: 'green',
  Error: 'red',
  'In Progress': 'blue',
};
</script>

<style scoped>
/* Add any scoped styles if needed */
</style>
