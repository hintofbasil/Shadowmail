<template>
  <div class="row">
    <div :class="this.get_class_name()">
      <i
        class="material-icons descriptor-icon"
        v-text="this.get_material_icon()"
      >
      </i>
      <br />
      <span :class="this.get_class_name()">{{ this.reason }}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    status: String,
    reason: String
  },
  methods: {
    get_class_name: function() {
      return this.status === "OK"
        ? "offset-by-two eight columns success-response"
        : "offset-by-two eight columns error-response";
    },
    get_material_icon: function() {
      return this.status === "OK" ? "mail_outline" : "error";
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../colors";

.descriptor-icon {
  font-size: 2em;
}

.success-response {
  text-align: center;
  color: $success-text-color;
  font-size: 1.5em;
}

.error-response,
.error-response-small {
  text-align: center;
  color: $error-text-color;
  font-size: 1.5em;
}
</style>
