<template>
  <div class="footer">
    &#xa9; ShadowMail.co.uk 2017 - 2020
  </div>
</template>

<style lang="scss">
@import "../colors";

$footer-height: 2em;

.footer {
  background-color: $background-color;
  color: $text-on-background-color;
  text-align: center;
  height: $footer-height;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
}

.body {
  min-height: 100%;
  padding-bottom: $footer-height;
}

html {
  height: 100%;
}

body {
  min-height: 100%;
  position: relative;
}
</style>
