<script setup lang="ts">
import AsciinemaPlayer from '../components/AsciinemaPlayer.vue'
</script>

<template>
  <div class="h-full w-full flex flex-col bg-[#121317] p-5 text-white overflow-hidden">
    <!-- Header Bar (~10-12% height) -->
    <div class="flex items-center justify-between pb-2 border-b border-gray-800/80 shrink-0">
      <div class="flex items-center gap-3">
        <h2 class="text-lg font-bold text-gray-100 tracking-wide m-0">
          {{ $frontmatter.title || 'Terminal Session Recording' }}
        </h2>
      </div>

      <div class="flex items-center gap-3">
        <span class="text-xs text-gray-400 bg-gray-800/90 px-2.5 py-1 rounded border border-gray-700/80 flex items-center gap-1.5 shadow-sm">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          Click terminal to play
        </span>
      </div>
    </div>

    <!-- Main Viewport Area (85-90% height) -->
    <div class="flex-1 w-full min-h-0 pt-3 flex items-center justify-center">
      <AsciinemaPlayer
        v-if="$frontmatter.cast || $frontmatter.castSrc"
        :src="$frontmatter.cast || $frontmatter.castSrc"
        :autoPlay="$frontmatter.autoPlay ?? false"
        :speed="$frontmatter.speed ?? 2.0"
        :idleTimeLimit="$frontmatter.idleTimeLimit ?? 1.0"
        :fit="$frontmatter.fit ?? 'both'"
        :theme="$frontmatter.theme ?? 'dracula'"
        class="w-full h-full"
      />
      <div v-else class="w-full h-full flex flex-col justify-center">
        <slot />
      </div>
    </div>
  </div>
</template>
