<script lang="ts" setup>
</script>

<template>
  <div class="brand">
    <div class="brand-text">
      <div class="title-row">
        <span class="star-flank" aria-hidden="true">✦</span>
        <h1 class="title">言寄星</h1>
        <span class="star-flank" aria-hidden="true">✦</span>
      </div>
      <p class="tagline">愿星光替你说话</p>
    </div>
  </div>
</template>

<style scoped lang="less">
.brand {
  display: flex;
  align-items: center;
  min-width: 0;
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 0;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.star-flank {
  font-size: 0.65rem;
  color: #fde68a;
  opacity: 0.95;
  filter: drop-shadow(0 0 8px rgba(253, 230, 138, 0.55));
  line-height: 1;
  padding-bottom: 0.1rem;
}

.title {
  margin: 0;
  font-family: 'Noto Serif SC', serif;
  font-size: 1.35rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  color: rgba(255, 255, 255, 0.96);
  line-height: 1.2;
}

.tagline {
  margin: 0;
  font-size: 0.72rem;
  font-weight: 400;
  color: var(--text-muted);
  letter-spacing: 0.06em;
}
</style>
