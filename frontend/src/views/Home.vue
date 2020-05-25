<template>
  <div class="body">
    <div class="container">
      <div class="row">
        <div class="offset-by-two eight columns title">
          <img class="logo-image" src="../assets/logo.png" />
        </div>
      </div>
      <div class="row">
        <div class="offset-by-one ten columns sub-title">
          private email forwarding
        </div>
      </div>
      <EmailSubmitForm />
    </div>
    <DescriptorContainer />
    <FaqContainer />
  </div>
</template>

<script>
// @ is an alias to /src
import EmailSubmitForm from "@/components/EmailSubmitForm.vue";
import DescriptorContainer from "@/components/DescriptorContainer.vue";
import FaqContainer from "@/components/FaqContainer.vue";

export default {
  name: "Home",
  components: {
    EmailSubmitForm,
    DescriptorContainer,
    FaqContainer
  }
};
</script>

<style lang="scss" scoped>
@import "../colors";

.title {
  margin-top: 15%;
  text-align: center;
}

.sub-title {
  margin-bottom: 10%;
  text-align: center;
  color: $subtitle-text-color;
  font-weight: bold;
  font-size: 5vw;
}

@media (min-width: 550px) {
  .sub-title {
    font-size: 3vw;
  }
}

@media (min-width: 940px) {
  .sub-title {
    font-size: 28px;
  }
}

.logo-image {
  width: 100%;
  max-width: 465px;
}

.background {
  background-color: $background-color;
  padding: 5% 0 5% 0;
}
</style>
