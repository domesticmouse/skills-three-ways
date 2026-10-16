<template>
  <div class="h-full w-full flex flex-col bg-[#121317] p-6 text-white overflow-hidden">
    <!-- Top Meta & Title Bar -->
    <div class="flex items-center justify-between pb-3 border-b border-gray-800 shrink-0">
      <div class="flex items-center gap-3">
        <span
          v-if="$frontmatter.way"
          class="text-xs font-semibold px-2.5 py-0.5 rounded-full tracking-wider uppercase"
          :class="getCategoryBadgeClass($frontmatter.way)"
        >
          {{ getCategoryLabel($frontmatter.way) }}
        </span>
        <span
          v-if="$frontmatter.skill"
          class="text-xs font-mono font-medium px-2 py-0.5 rounded bg-gray-800 text-gray-300 border border-gray-700"
        >
          {{ $frontmatter.skill }}
        </span>
        <h2 class="text-xl font-bold text-gray-100 tracking-wide m-0">
          {{ $frontmatter.title || 'Skill Architecture' }}
        </h2>
      </div>

      <div v-if="$frontmatter.step" class="text-xs text-gray-400 font-medium tracking-wide">
        {{ $frontmatter.step }}
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
function getCategoryLabel(way: string | number): string {
  const str = String(way).toLowerCase()
  if (str.includes('1') || str.includes('library')) return 'Way 1 · Library Review'
  if (str.includes('2') || str.includes('dfu') || str.includes('operational')) return 'Way 2 · DFU Operational'
  if (str.includes('3') || str.includes('hardware') || str.includes('discovery')) return 'Way 3 · Hardware Discovery'
  if (str.includes('mashup') || str.includes('usb')) return 'The Mashup Skill'
  return `Way ${way}`
}

function getCategoryBadgeClass(way: string | number): string {
  const str = String(way).toLowerCase()
  if (str.includes('1') || str.includes('library')) return 'badge-way1'
  if (str.includes('2') || str.includes('dfu') || str.includes('operational')) return 'badge-way2'
  if (str.includes('3') || str.includes('hardware') || str.includes('discovery')) return 'badge-way3'
  if (str.includes('mashup') || str.includes('usb')) return 'badge-mashup'
  return 'bg-gray-800 text-gray-300 border border-gray-700'
}

function getCardBorderClass(way: string | number): string {
  const str = String(way).toLowerCase()
  if (str.includes('1') || str.includes('library')) return 'border-cyan-500/30 bg-cyan-950/10'
  if (str.includes('2') || str.includes('dfu') || str.includes('operational')) return 'border-amber-500/30 bg-amber-950/10'
  if (str.includes('3') || str.includes('hardware') || str.includes('discovery')) return 'border-emerald-500/30 bg-emerald-950/10'
  if (str.includes('mashup') || str.includes('usb')) return 'border-purple-500/30 bg-purple-950/10'
  return 'border-gray-800 bg-gray-900/40'
}
</script>
