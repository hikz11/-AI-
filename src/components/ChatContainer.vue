<script setup lang="ts">
import { ref, nextTick, computed } from 'vue'
import type { Message } from '@/types/message'

const messages = ref<Message[]>([])

const emit = defineEmits<{
  (e: 'quick-send', text: string): void
  (e: 'open-voice'): void
}>()

const hasMessages = computed(() => messages.value.length > 0)

const processText = (text: string): string => {
  return text.replace(/[，。]$/, '')
}

const appendMessage = (type: 'user' | 'ai', text: string) => {
  const now = new Date()
  messages.value.push({
    type,
    content: processText(text),
    time: now.toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit',
    }),
  })
  nextTick(() => {
    const container = document.querySelector('.chat-scroll')
    if (container) {
      container.scrollTop = container.scrollHeight
    }
  })
}

const featureCards = [
  {
    key: 'daily',
    icon: 'bubble',
    title: '和我聊聊今天',
    desc: '分享你的日常',
    prompt: '今天我想和你聊聊我的一天。',
    color: '#c084fc',
  },
  {
    key: 'mood',
    icon: 'heart',
    title: '帮我整理情绪',
    desc: '理清你的心情',
    prompt: '我最近心情有点复杂，想请你陪我梳理一下。',
    color: '#f472b6',
  },
  {
    key: 'warm',
    icon: 'star',
    title: '给我一点鼓励',
    desc: '温暖你的心',
    prompt: '可以给我一点鼓励吗？',
    color: '#fcd34d',
  },
  {
    key: 'voice',
    icon: 'wave',
    title: '想听你的声音',
    desc: '语音陪你聊聊',
    prompt: '',
    color: '#a78bfa',
    action: 'voice' as const,
  },
]

const onCardClick = (card: (typeof featureCards)[0]) => {
  if (card.action === 'voice') {
    emit('open-voice')
    return
  }
  if (card.prompt) {
    emit('quick-send', card.prompt)
  }
}

defineExpose({
  appendMessage,
})
</script>

<template>
  <div class="chat-root">
    <div v-if="!hasMessages" class="hero">
      <div class="hero-inner">
        <h2 class="greeting">
          你好，我是言寄星
          <span class="spark" aria-hidden="true">✦</span>
        </h2>
        <p class="sub">今晚想聊些什么？</p>

        <div class="cards">
          <button
            v-for="card in featureCards"
            :key="card.key"
            type="button"
            class="feature-card"
            @click="onCardClick(card)"
          >
            <span class="card-icon" :style="{ color: card.color }">
              <template v-if="card.icon === 'bubble'">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M4 5a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2H9l-4 4v-4H6a2 2 0 01-2-2V5z"
                  />
                </svg>
              </template>
              <template v-else-if="card.icon === 'heart'">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
                  />
                </svg>
              </template>
              <template v-else-if="card.icon === 'star'">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M12 2l2.4 7.4h7.6l-6 4.6 2.3 7L12 16.9 5.7 21l2.3-7-6-4.6h7.6z"
                  />
                </svg>
              </template>
              <template v-else>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 12v-2a2 2 0 012-2h2M4 18v2a2 2 0 002 2h2M20 12v-2a2 2 0 00-2-2h-2M20 18v2a2 2 0 01-2 2h-2" />
                  <path d="M8 10v4M12 8v8M16 10v4" />
                </svg>
              </template>
            </span>
            <span class="card-text">
              <span class="card-title">{{ card.title }}</span>
              <span class="card-desc">{{ card.desc }}</span>
            </span>
          </button>
        </div>
      </div>
    </div>

    <div v-else class="chat-scroll">
      <div class="chat-messages">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.type]"
        >
          <div class="message-content" v-html="msg.content" />
          <div class="message-time">{{ msg.time }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.chat-root {
  flex: 1 1 0;
  min-height: 0;
  height: 100%;
  width: 100%;
  max-width: 56rem;
  margin: 0 auto;
  padding: 0 0.75rem 7.5rem;
  display: flex;
  flex-direction: column;
  position: relative;
  align-self: stretch;
  justify-content: flex-start;
}

.hero {
  flex: 1 1 0;
  min-height: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 1.4rem 0 1.4rem;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.hero-inner {
  width: 100%;
  max-width: 58rem;
  text-align: center;
  padding: 2rem;
  border-radius: 36px;
  background: rgba(7, 12, 28, 0.58);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 32px 90px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
}

.greeting {
  margin: 0;
  font-family: 'Noto Serif SC', serif;
  font-size: clamp(1.5rem, 4vw, 2rem);
  font-weight: 600;
  color: rgba(255, 255, 255, 0.96);
  letter-spacing: 0.04em;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  flex-wrap: wrap;
}

.spark {
  color: #fde68a;
  font-size: 0.85em;
  filter: drop-shadow(0 0 8px rgba(253, 230, 138, 0.6));
}

.sub {
  margin: 0.75rem 0 1.75rem;
  font-size: 0.95rem;
  color: var(--text-soft);
  letter-spacing: 0.06em;
}

.cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;

  @media (max-width: 900px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 420px) {
    grid-template-columns: 1fr;
  }
}

.feature-card {
  display: flex;
  flex-direction: row;
  align-items: center;
  text-align: left;
  gap: 0.85rem;
  padding: 1rem 1rem;
  border-radius: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.16);
  cursor: pointer;
  transition:
    transform 0.2s,
    border-color 0.2s,
    background 0.2s,
    box-shadow 0.2s;
  color: inherit;

  &:hover {
    transform: translateY(-3px);
    border-color: rgba(255, 255, 255, 0.22);
    background: rgba(255, 255, 255, 0.12);
    box-shadow: 0 24px 64px rgba(0, 0, 0, 0.18);
  }
}

.card-icon {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 2.8rem;
  height: 2.8rem;
  border-radius: 0.95rem;
  background: rgba(255, 255, 255, 0.1);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.08);

  svg {
    width: 1.3rem;
    height: 1.3rem;
  }
}

.card-text {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 0;
  flex: 1;
  text-align: left;
}

.card-title {
  font-size: 0.88rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.92);
  line-height: 1.35;
}

.card-desc {
  font-size: 0.75rem;
  color: var(--text-muted);
  line-height: 1.4;
}

.chat-scroll {
  flex: 1 1 0;
  min-height: 0;
  display: flex;
  flex-direction: column;
  padding: 0.75rem;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(6, 10, 28, 0.45);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.chat-scroll::after {
  content: '';
  display: block;
  height: 6rem;
}

.chat-messages {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-top: auto;
  min-height: min-content;
  width: 100%;
}

.message.ai,
.message.user {
  .message-content {
    width: max-content;
    max-width: 89%;
    padding: 0.55rem 1rem;
    white-space: pre-line;
    overflow-wrap: break-word;
    word-break: break-word;
  }

  .message-time {
    color: var(--text-muted);
    font-size: 0.72rem;
    margin-top: 0.25rem;
  }
}

.message.ai {
  margin: 0.5rem 0;

  .message-content {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    border-radius: 1rem 1rem 1rem 6px;
    color: var(--text-color);
  }
}

.message.user {
  margin: 0.5rem 0;
  display: flex;
  flex-direction: column;
  align-items: flex-end;

  .message-content {
    background: var(--gradient-primary);
    border-radius: 1rem 1rem 6px 1rem;
    color: white;
    margin-left: auto;
    box-shadow: var(--shadow-soft);
  }

  .message-time {
    text-align: right;
  }
}
</style>
