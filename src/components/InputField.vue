<script lang="ts" setup>
import { ref } from 'vue'

const props = withDefaults(
  defineProps<{
    voiceSessionActive?: boolean
    userSpeaking?: boolean
  }>(),
  {
    voiceSessionActive: false,
    userSpeaking: false,
  },
)

const emit = defineEmits<{
  (e: 'sendMessage', text: string): void
  (e: 'toggleVoice'): void
}>()

const message = ref<string>('')

const clearInputField = () => {
  message.value = ''
}

const onInput = (e: Event) => {
  message.value = (e.target as HTMLDivElement).innerText
}

const handleKeyPress = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey && message.value?.trim()) {
    e.preventDefault()
    submitText()
  }
}

const submitText = () => {
  const t = message.value?.trim()
  if (!t) return
  emit('sendMessage', t)
  clearInputField()
  const el = document.getElementById('messageInput')
  if (el) el.innerText = ''
}

defineExpose({
  setPlaceholderFocus: () => {
    const el = document.getElementById('messageInput')
    el?.focus()
  },
})
</script>

<template>
  <footer class="input-footer">
    <div class="input-bar">
      <div class="input-shell input-box">
        <div
          id="messageInput"
          class="input-area"
          contenteditable="true"
          spellcheck="false"
          data-placeholder="输入你想说的话..."
          @input="onInput"
          @keydown="handleKeyPress"
        ></div>
      </div>

      <div class="voice-wrap">
        <button
          type="button"
          class="voice-btn"
          :class="{
            active: props.voiceSessionActive,
            speaking: props.voiceSessionActive && props.userSpeaking,
          }"
          :aria-pressed="props.voiceSessionActive"
          :aria-label="props.voiceSessionActive ? '结束语音输入' : '开始语音输入'"
          @click="emit('toggleVoice')"
        >
          <span class="ring ring-3" />
          <span class="ring ring-2" />
          <span class="ring ring-1" />
          <span class="voice-inner">
            <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round">
              <path d="M4 12v-2a2 2 0 012-2h2M4 18v2a2 2 0 002 2h2M20 12v-2a2 2 0 00-2-2h-2M20 18v2a2 2 0 01-2 2h-2" />
              <path d="M8 10v4M12 8v8M16 10v4" />
            </svg>
          </span>
        </button>
        <span class="voice-label">{{ props.voiceSessionActive ? '点击结束' : '点击说话' }}</span>
      </div>
    </div>
  </footer>
</template>

<style scoped lang="less">
.input-footer {
  position: fixed;
  left: 50%;
  bottom: 1.2rem;
  transform: translateX(-50%);
  width: min(96%, 56rem);
  z-index: 30;
  flex-shrink: 0;
  padding: 0 0.75rem;
  pointer-events: none;
}

.input-footer .input-bar {
  pointer-events: all;
}

.input-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.85rem;
  max-width: 56rem;
  margin: 0 auto;
  width: 100%;
  padding: 0.9rem 1rem calc(1rem + env(safe-area-inset-bottom, 0px));
  background: rgba(6, 10, 28, 0.7);
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 -18px 60px rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
}

.input-shell {
  flex: 1;
  display: flex;
  align-items: center;
  min-width: 0;
  padding: 0.95rem 1.1rem;
  border-radius: 999px;
}

.input-area {
  flex: 1;
  min-height: 1.35rem;
  max-height: 5rem;
  overflow-y: auto;
  outline: none;
  color: rgba(255, 255, 255, 0.92);
  font-size: 0.95rem;
  line-height: 1.45;
  scrollbar-width: none;

  &:empty::before {
    content: attr(data-placeholder);
    color: var(--text-muted);
    pointer-events: none;
  }
}

.kbd-btn {
  display: none;
}

.voice-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
  flex-shrink: 0;
  min-width: 4.15rem;
}

.voice-label {
  font-size: 0.78rem;
  color: var(--text-soft);
}

.voice-btn {
  position: relative;
  width: 4.15rem;
  height: 4.15rem;
  border: none;
  padding: 0;
  cursor: pointer;
  background: transparent;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.voice-btn.active .voice-inner {
  background: linear-gradient(145deg, #5b8dff, #7c3aed 55%, #c084fc);
  box-shadow:
    0 0 0 6px rgba(124, 156, 255, 0.08),
    0 16px 40px rgba(124, 156, 255, 0.18),
    inset 0 1px 0 rgba(255, 255, 255, 0.18);
}

.voice-btn.speaking .ring-1 {
  animation-duration: 1.1s;
  border-color: rgba(99, 102, 241, 0.55);
}

.ring {
  position: absolute;
  border-radius: 50%;
  inset: 0;
  border: 1px solid rgba(168, 85, 247, 0.35);
  pointer-events: none;
}

.ring-1 {
  animation: pulse-a 2.4s ease-out infinite;
}

.ring-2 {
  inset: -6px;
  border-color: rgba(99, 102, 241, 0.25);
  animation: pulse-b 2.4s ease-out infinite 0.4s;
}

.ring-3 {
  inset: -12px;
  border-color: rgba(59, 130, 246, 0.2);
  animation: pulse-b 2.4s ease-out infinite 0.8s;
}

.voice-inner {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--gradient-voice);
  box-shadow:
    0 8px 28px rgba(79, 70, 229, 0.45),
    inset 0 1px 0 rgba(255, 255, 255, 0.25);
  transition:
    transform 0.15s,
    background 0.25s,
    box-shadow 0.25s;

  svg {
    width: 1.45rem;
    height: 1.45rem;
  }
}

.voice-btn:hover .voice-inner {
  transform: scale(1.05);
}

.voice-btn:active .voice-inner {
  transform: scale(0.97);
}

.voice-label {
  font-size: 0.72rem;
  color: var(--text-muted);
  letter-spacing: 0.08em;
  white-space: nowrap;
}

@keyframes pulse-a {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.55;
  }
  50% {
    transform: scale(1.06);
    opacity: 0.9;
  }
}

@keyframes pulse-b {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.35;
  }
  50% {
    transform: scale(1.04);
    opacity: 0.55;
  }
}
</style>
