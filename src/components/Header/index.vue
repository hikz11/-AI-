<script setup lang="ts">
import ConnectionStatus from './ConnectionStatus.vue'
import Title from './Title.vue'
import SettingButton from '../Setting/SettingButton.vue'
import { ref } from 'vue'

const props = defineProps<{
  connectionStatus: 'connected' | 'disconnected' | 'error'
  nightDim: boolean
}>()

const emit = defineEmits<{
  (e: 'toggle-night'): void
}>()

const musicOn = ref(false)

const onMoon = () => {
  emit('toggle-night')
}

const onMusic = () => {
  musicOn.value = !musicOn.value
}
</script>

<template>
  <header class="app-header">
    <Title />
    <div class="header-right">
      <ConnectionStatus :connection-status="props.connectionStatus" />
      <button
        type="button"
        class="icon-btn"
        :class="{ active: props.nightDim }"
        aria-label="切换夜间柔和"
        title="夜间柔和"
        @click="onMoon"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"
          />
        </svg>
      </button>
      <button
        type="button"
        class="icon-btn"
        :class="{ active: musicOn }"
        aria-label="背景音乐"
        title="背景音乐"
        @click="onMusic"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M9 18V5l12-2v13M9 9l12-2"
          />
          <circle cx="6" cy="18" r="3" />
          <circle cx="18" cy="16" r="3" />
        </svg>
      </button>
      <SettingButton />
    </div>
  </header>
</template>

<style scoped lang="less">
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.25rem 0.75rem;
  flex-shrink: 0;
  position: relative;
  z-index: 2;
  background: linear-gradient(180deg, rgba(6, 10, 28, 0.75) 0%, rgba(6, 10, 28, 0.2) 100%);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  color: rgba(255, 255, 255, 0.85);
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(10px);
  transition:
    background 0.2s,
    box-shadow 0.2s,
    transform 0.15s;

  svg {
    width: 1.15rem;
    height: 1.15rem;
  }

  &:hover {
    background: rgba(255, 255, 255, 0.14);
    transform: scale(1.04);
  }

  &.active {
    color: #fde68a;
    border-color: rgba(253, 230, 138, 0.35);
    box-shadow: 0 0 20px rgba(253, 230, 138, 0.2);
  }
}
</style>
