<template>
  <div>
    <div class="row">
      <div class="offset-by-two eight columns">
        <form method="POST" id="click-me-form">
          <input
            type="email"
            name="email"
            id="click-me-text-input"
            placeholder="email@shadowmail.co.uk"
            v-model="email"
          />
          <br />
          <input
            type="submit"
            id="click-me-button"
            value="Send request"
            v-on:click="submit"
          />
        </form>
      </div>
    </div>
    <DeleteFormResponse
      v-if="status"
      v-bind:status="status"
      v-bind:reason="reason"
    />
  </div>
</template>

<script>
import axios from "axios";
import DeleteFormResponse from "@/components/DeleteFormResponse.vue";

const REQUEST_DELETE_URL = "/api/request_delete";

export default {
  components: {
    DeleteFormResponse
  },
  data: () => {
    const url = new URL(document.URL);
    const email = url.searchParams.get("email");
    return {
      email: email,
      status: "",
      reason: ""
    };
  },
  methods: {
    submit: async function(event) {
      event.preventDefault();
      const data = {
        email: this.email
      };
      try {
        const response = await axios.post(REQUEST_DELETE_URL, data);
        this.status = response.data.status;
        this.reason = "Confirmation email sent";
      } catch (error) {
        const { response } = error;
        this.status = response.data.status || "ERROR";
        this.reason = response.data.reason || "An unexpected error occured";
      }
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../colors";

#click-me-button {
  max-width: 90%;
  word-wrap: break-word;
  white-space: normal;
  height: 100%;
  margin-bottom: 0;
}

#click-me-form {
  text-align: center;
  padding-top: 10%;
  padding-bottom: 10%;
  margin-bottom: 0;
}

#click-me-text-input {
  text-align: center;
  margin-bottom: 5rem;
  width: 100%;
  font-size: 1.4em;
}

@media (min-width: 550px) {
  #click-me-form {
    padding-top: 6%;
    padding-bottom: 6%;
  }

  #click-me-button {
    font-size: 1em;
  }
}
</style>
