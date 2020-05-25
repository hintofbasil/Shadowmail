<template>
  <Layout>
    <div class="body">
      <div class="request-delete-email" />
      <div class="container">
        <DeleteForm />
      </div>
    </div>
  </Layout>
</template>

<script>
import DeleteForm from "@/components/DeleteForm.vue";

export default {
  components: {
    DeleteForm
  }
};
</script>

<style lang="scss" scoped>
@import "../colors";

.request-delete-email {
  text-align: center;
  padding: 15%;
  background-color: $background-color;
  color: $text-on-background-color;
  word-wrap: break-word;
  font-weight: bold;
}

@media (min-width: 550px) {
  .request-delete-email {
    font-size: 2em;
    padding: 5%;
  }
}
</style>
