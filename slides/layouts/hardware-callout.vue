<script setup lang="ts">
/**
 * Normalizes asset paths against Vite's base URL for GitHub Pages compatibility
 */
function resolveUrl(rawSrc: string | undefined): string {
  if (!rawSrc) return ''
  if (
    rawSrc.startsWith('http://') ||
    rawSrc.startsWith('https://') ||
    rawSrc.startsWith('data:') ||
    rawSrc.startsWith('blob:')
  ) {
    return rawSrc
  }
  const base = import.meta.env.BASE_URL || '/'
  const normalizedBase = base.endsWith('/') ? base : `${base}/`
  const cleanPath = rawSrc.replace(/^\.?\//, '')
  return `${normalizedBase}${cleanPath}`
}
</script>

<template>
  <div class="h-full w-full flex flex-col bg-[#121317] p-6 text-white overflow-hidden">
    <!-- Header Bar -->
    <div class="flex items-center justify-between pb-3 border-b border-gray-800 shrink-0">
      <div class="flex items-center gap-3">
        <h2 class="text-2xl font-bold text-gray-100 m-0">
          {{ $frontmatter.title || 'Hardware Architecture' }}
        </h2>
      </div>

      <div v-if="$frontmatter.subtitle" class="text-xs text-gray-400 font-mono">
        {{ $frontmatter.subtitle }}
      </div>
    </div>

    <!-- 2-Column Split: Hardware Asset Frame + Annotated Details -->
    <div class="flex-1 w-full min-h-0 mt-4 grid grid-cols-12 gap-6 items-center">
      <!-- Media Frame (Left 6 cols) -->
      <div class="col-span-6 h-full flex flex-col justify-center">
        <div class="relative w-full h-[360px] rounded-xl border border-gray-700/60 bg-[#0d0e12] overflow-hidden flex items-center justify-center p-3 shadow-lg">
          <img
            v-if="$frontmatter.image"
            :src="resolveUrl($frontmatter.image)"
            :alt="$frontmatter.title || 'Hardware Image'"
            class="max-w-full max-h-full object-contain rounded"
          />
          <div v-else class="text-gray-500 text-sm italic">
            Hardware visual asset placeholder
          </div>

          <!-- Caption overlay -->
          <div
            v-if="$frontmatter.imageCaption"
            class="absolute bottom-2 left-2 right-2 bg-black/75 backdrop-blur-sm border border-gray-800 px-3 py-1.5 rounded text-xs text-gray-300 flex items-center justify-between"
          >
            <span>{{ $frontmatter.imageCaption }}</span>
          </div>
        </div>
      </div>

      <!-- Detail / Callout Column (Right 6 cols) -->
      <div class="col-span-6 h-full flex flex-col justify-center overflow-y-auto pr-2">
        <slot />
      </div>
    </div>
  </div>
</template>
