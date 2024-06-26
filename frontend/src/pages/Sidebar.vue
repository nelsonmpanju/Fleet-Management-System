<template>
<aside id="logo-sidebar" class="fixed top-0 left-0 z-40 w-70 h-screen pt-20 transition-transform -translate-x-full bg-white border-r border-gray-200 sm:translate-x-0" aria-label="Sidebar">
   <div class="px-3 pb-4">
      <!-- Search Form -->
      <form class="relative mb-4">
          <div class="relative">
              <div class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none">
                  <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
              </div>
              <input type="search" id="search-sidebar" class="block w-full pl-10 p-2.5 text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500" placeholder="Search..." required>
          </div>
      </form>
      <!-- Navigation Menu -->
      <ul class="space-y-2 font-medium overflow-y-auto">
         <li>
            <a class="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group">
               <span class="ms-3">Dashboard</span>
            </a>
         </li>
      </ul>
   </div>
</aside>
</template>

<style scoped>
#logo-sidebar {
  width: 330px; /* Adjusted width for better visibility */
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  background-color: white;
  z-index: 40;
}
</style>