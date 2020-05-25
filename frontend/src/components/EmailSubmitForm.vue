<template>
  <div>
    <div class="row">
      <div class="offset-by-two eight columns">
        <form
          method="POST"
          id="new-email-form"
          class="input-then-button-layout"
        >
          <input type="submit" value="↩" v-on:click="submit" />
          <span class="submit-span">
            <input
              v-model="email"
              type="email"
              name="email"
              class="email-input"
              id="new-email-input"
              placeholder="you@domain.com"
            />
          </span>
        </form>
      </div>
    </div>
    <div class="row">
      <div class="offset-by-two eight columns">
        <EmailSubmitSuccess v-if="new_email" v-bind:email="new_email" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import EmailSubmitSuccess from "@/components/EmailSubmitSuccess.vue";

const NEW_EMAIL_URL = "/api/new";

export default {
  components: {
    EmailSubmitSuccess
  },
  data: () => {
    return {
      email: "",
      new_email: ""
    };
  },
  methods: {
    submit: async function(event) {
      event.preventDefault();
      const submitData = {
        email: this.email
      };
      const response = await axios.post(NEW_EMAIL_URL, submitData);
      this.new_email = response.data.email;
    }
  }
};
</script>

<style lang="scss" scoped>
.input-then-button-layout {
  margin-bottom: 2rem;

  > :first-child {
    float: right;
    padding: 0;
    width: 38px; // Height is set in Skeleton
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
  }

  span {
    display: block;
    overflow: hidden;

    > :first-child {
      width: 100%;
      border-top-right-radius: 0;
      border-bottom-right-radius: 0;
      border-right: none;
    }
  }
}
</style>
