<template>
  <div class="h-full w-full flex flex-col bg-[#121317] p-6 text-white overflow-hidden">
    <!-- Top Meta & Title Bar -->
    <div class="flex items-center justify-between pb-3 border-b border-gray-800 shrink-0">
      <div class="flex items-center gap-3">
        <h2 class="text-2xl font-bold text-gray-100 m-0">
          {{ $frontmatter.title || 'Skill Architecture' }}
        </h2>
      </div>

      <div class="flex items-center gap-3 text-xs text-gray-400 font-mono">
        <span v-if="$frontmatter.skill">{{ $frontmatter.skill }}</span>
        <span v-if="$frontmatter.skill && $frontmatter.step">&middot;</span>
        <span v-if="$frontmatter.step">{{ $frontmatter.step }}</span>
      </div>
    </div>

    <!-- Content Card -->
    <div
      class="flex-1 w-full min-h-0 mt-4 rounded-xl border p-5 flex flex-col overflow-y-auto"
      :class="getCardBorderClass($frontmatter.way)"
    >
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
function getCardBorderClass(way: string | number): string {
  const str = String(way).toLowerCase()
  if (str.includes('1') || str.includes('library')) return 'border-cyan-500/30 bg-cyan-950/10'
  if (str.includes('2') || str.includes('dfu') || str.includes('operational')) return 'border-amber-500/30 bg-amber-950/10'
  if (str.includes('3') || str.includes('hardware') || str.includes('discovery')) return 'border-emerald-500/30 bg-emerald-950/10'
  if (str.includes('mashup') || str.includes('usb')) return 'border-purple-500/30 bg-purple-950/10'
  return 'border-gray-800 bg-gray-900/40'
}
</script>
