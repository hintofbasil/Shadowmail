<template>
  <div class="offset-by-two eight columns faq-question">
    <details>
      <summary>{{ element.summary }}</summary>
      <p>{{ element.content }}</p>
    </details>
  </div>
</template>

<script>
export default {
  props: {
    element: Object
  }
};
</script>

<style lang="scss" scoped>
@import "../colors";

.faq-question {
  margin-top: 2%;
  margin-bottom: 2%;

  summary {
    display: list-item;
    font-size: 1.1em;
  }
}
</style>
