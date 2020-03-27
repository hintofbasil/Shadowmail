<template>
  <div class="four columns descriptor">
    <div class="descriptor-title">{{ element.title }}</div>
    <div>
      <i class="material-icons descriptor-icon">{{ element.symbol }}</i>
    </div>
    <div class="descriptor-text" v-html="element.description" />
  </div>
</template>

<script>
export default {
  name: "DescriptorElement",
  props: {
    element: Object,
    title: String,
    symbol: String,
    description: String
  }
};
</script>

<style lang="scss" scoped>
@import "../colors";

.columns {
  margin: 0;
  padding: 0 2% 0 2%;
}

.descriptor {
  text-align: center;
  color: $text-on-background-color;
  padding-bottom: 5%;
  padding-top: 5%;
  height: 100%;

  a {
    color: $text-on-background-hyperlink;
  }
}

.descriptor-title {
  font-size: 2em;
}

.descriptor-icon {
  width: 50%;
  font-size: 4em;
}

.descriptor:not(:last-child) {
  border-bottom: 2px solid $text-on-background-color;
}

@media (min-width: 550px) {
  .descriptor:not(:last-child) {
    border-bottom: none;
  }
}
</style>
