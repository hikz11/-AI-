<script lang="ts" setup>
import { computed } from 'vue'
import { useSettingStore } from '@/stores/setting'

const settingStore = useSettingStore()

const connectionStatusClass = computed(() => props.connectionStatus)
const connectionStatusText = computed(() => {
  const texts = {
    connected: '在线',
    disconnected: '离线',
    error: '异常',
  }
  return texts[props.connectionStatus]
})

const props = defineProps<{
  connectionStatus: 'connected' | 'disconnected' | 'error'
}>()
</script>

<template>
  <div class="status-wrap">
    <div :class="['pill', connectionStatusClass]" :title="'连接：' + connectionStatusText">
      <span class="dot" />
      {{ connectionStatusText }}
    </div>
    <span class="device" :title="settingStore.deviceId">设备 · {{ settingStore.deviceId || '—' }}</span>
  </div>
</template>

<style scoped lang="less">
.status-wrap {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  max-width: 11rem;
  min-width: 0;

  @media (max-width: 640px) {
    .device {
      display: none;
    }
    max-width: none;
  }
}

.pill {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.25rem 0.6rem;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.02em;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(10px);
  color: var(--text-soft);
  white-space: nowrap;

  .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  &.connected .dot {
    background: #4ade80;
    box-shadow: 0 0 8px rgba(74, 222, 128, 0.7);
  }

  &.disconnected .dot {
    background: rgba(255, 255, 255, 0.35);
  }

  &.error .dot {
    background: #f87171;
    box-shadow: 0 0 8px rgba(248, 113, 113, 0.6);
  }
}

.device {
  font-size: 0.68rem;
  color: var(--text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 6rem;
}
</style>
