<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import 'asciinema-player/dist/bundle/asciinema-player.css'

export interface AsciinemaPlayerProps {
  /**
   * Path to .cast file (e.g. '/casts/demo.cast'), Data URL, or remote URL
   */
  src: string
  /**
   * Terminal columns override (defaults to recording header)
   */
  cols?: number
  /**
   * Terminal rows override (defaults to recording header)
   */
  rows?: number
  /**
   * Automatically start playback on slide entry
   */
  autoPlay?: boolean
  /**
   * Preload cast file before playback starts
   */
  preload?: boolean
  /**
   * Loop playback: true for infinite, or a number for fixed repetitions
   */
  loop?: boolean | number
  /**
   * Playback speed multiplier (e.g. 1.0, 1.5, 2.0)
   */
  speed?: number
  /**
   * Skip to timestamp in seconds or NPT string ("0:15")
   */
  startAt?: number | string
  /**
   * Maximum idle time between terminal events in seconds
   */
  idleTimeLimit?: number
  /**
   * Color theme: 'asciinema' | 'dracula' | 'monokai' | 'nord' | 'solarized-dark' |
   * 'solarized-light' | 'gruvbox-dark' | 'tango' | 'github-dark' | 'github-light'
   */
  theme?: string
  /**
   * Scaling mode: 'width' | 'height' | 'both' | 'none'
   */
  fit?: 'width' | 'height' | 'both' | 'none'
  /**
   * Player control bar: true | false | 'auto' (show on hover)
   */
  controls?: boolean | 'auto'
  /**
   * Terminal font size: 'small' | 'medium' | 'big' or custom CSS size (e.g. '14px')
   */
  terminalFontSize?: string
  /**
   * Custom CSS font family string
   */
  terminalFontFamily?: string
  /**
   * Terminal line height multiplier
   */
  terminalLineHeight?: number
  /**
   * Poster frame preview timestamp (e.g. 'npt:0:05')
   */
  poster?: string
  /**
   * Chapter markers: [timestamp, label][] or [timestamp][]
   */
  markers?: Array<number | [number, string]>
  /**
   * Pause automatically on hitting chapter markers
   */
  pauseOnMarkers?: boolean
}

const props = withDefaults(defineProps<AsciinemaPlayerProps>(), {
  cols: undefined,
  rows: undefined,
  autoPlay: false,
  preload: false,
  loop: false,
  speed: 1.0,
  startAt: 0,
  idleTimeLimit: 2.0,
  theme: 'dracula',
  fit: 'width',
  controls: 'auto',
  terminalFontSize: 'small',
  terminalFontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace",
  terminalLineHeight: 1.3333,
  poster: undefined,
  markers: () => [],
  pauseOnMarkers: false,
})

const containerRef = ref<HTMLDivElement | null>(null)
let playerInstance: any = null
let resizeObserver: ResizeObserver | null = null

/**
 * Normalizes asset paths against Vite's base URL for GitHub Pages compatibility
 */
function resolveUrl(rawSrc: string): string {
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
  const cleanPath = rawSrc.startsWith('/') ? rawSrc.slice(1) : rawSrc
  return `${normalizedBase}${cleanPath}`
}

/**
 * Cleanly initializes the player on the client DOM
 */
async function initPlayer() {
  if (typeof window === 'undefined' || !containerRef.value) return

  // Dispose previous instance if re-initializing
  teardownPlayer()

  try {
    // Dynamic import guarantees no SSR execution for player JS
    const AsciinemaPlayer = await import('asciinema-player')

    const resolvedSrc = resolveUrl(props.src)

    const playerOptions: Record<string, any> = {
      cols: props.cols,
      rows: props.rows,
      autoPlay: props.autoPlay,
      preload: props.preload,
      loop: props.loop,
      speed: props.speed,
      startAt: props.startAt,
      idleTimeLimit: props.idleTimeLimit,
      theme: props.theme,
      fit: props.fit,
      controls: props.controls,
      terminalFontSize: props.terminalFontSize,
      terminalFontFamily: props.terminalFontFamily,
      terminalLineHeight: props.terminalLineHeight,
      poster: props.poster,
      markers: props.markers.length > 0 ? props.markers : undefined,
      pauseOnMarkers: props.pauseOnMarkers,
    }

    // Strip undefined keys
    Object.keys(playerOptions).forEach((key) => {
      if (playerOptions[key] === undefined) delete playerOptions[key]
    })

    playerInstance = AsciinemaPlayer.create(resolvedSrc, containerRef.value, playerOptions)

    // Setup ResizeObserver to adjust on Slidev view transitions
    if (typeof ResizeObserver !== 'undefined' && containerRef.value) {
      resizeObserver = new ResizeObserver(() => {
        if (playerInstance && typeof playerInstance.render === 'function') {
          playerInstance.render()
        }
      })
      resizeObserver.observe(containerRef.value)
    }
  } catch (err) {
    console.error('[AsciinemaPlayer] Failed to instantiate asciinema-player:', err)
  }
}

function teardownPlayer() {
  if (resizeObserver) {
    resizeObserver.disconnect()
    resizeObserver = null
  }
  if (playerInstance) {
    if (typeof playerInstance.dispose === 'function') {
      playerInstance.dispose()
    }
    playerInstance = null
  }
  if (containerRef.value) {
    containerRef.value.innerHTML = ''
  }
}

onMounted(() => {
  nextTick(() => {
    initPlayer()
  })
})

onUnmounted(() => {
  teardownPlayer()
})

// Reinitialize when source or theme changes reactively
watch(
  () => [props.src, props.theme, props.fit],
  () => {
    initPlayer()
  }
)
</script>

<template>
  <div class="asciinema-player-wrapper">
    <div ref="containerRef" class="asciinema-player-element" />
  </div>
</template>

<style scoped>
.asciinema-player-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
}

.asciinema-player-element {
  width: 100%;
  height: 100%;
}

/* Ensure player terminal controls match slide styling */
:deep(.asciinema-player-wrapper .ap-player) {
  border-radius: 8px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
</style>
