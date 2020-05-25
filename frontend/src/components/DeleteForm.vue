<template>
  <div>
    <div class="row">
      <div class="offset-by-two eight columns">
        <div class="warning1">
          Warning!
        </div>
      </div>
    </div>
    <div class="row">
      <div class="offset-by-two eight columns">
        <div class="warning2">
          This operation is not reversible.
        </div>
      </div>
    </div>
    <div class="row">
      <div class="offset-by-two eight columns">
        <form method="POST" id="click-me-form">
          <input
            type="email"
            name="email"
            id="click-me-text-input"
            placeholder="you@shadowmail.co.uk"
            v-model="email"
          />
          <br />
          <input
            type="submit"
            id="click-me-button"
            value="Confirm delete"
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
import DeleteFormResponse from "./DeleteFormResponse.vue";

const DELETE_URL = "/api/delete";

export default {
  components: {
    DeleteFormResponse
  },
  data: () => {
    const url = new URL(document.URL);
    const email = url.searchParams.get("email");
    const timestamp = url.searchParams.get("timestamp");
    const token = url.searchParams.get("token");

    return {
      email: email,
      timestamp: timestamp,
      token: token,
      status: "",
      reason: ""
    };
  },
  methods: {
    submit: async function(event) {
      event.preventDefault();
      const data = {
        email: this.email,
        timestamp: this.timestamp,
        token: this.token
      };
      try {
        const response = await axios.post(DELETE_URL, data);
        this.status = response.data.status;
        this.reason = "Email deleted";
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

.warning1,
.warning2 {
  text-align: center;
  color: $warning-text;
  font-weight: bold;
}

.warning1 {
  padding-top: 10%;
  font-size: 1.75em;
}

.warning2 {
  font-size: 1.5em;
}

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

  .request-delete-email {
    font-size: 2em;
    padding: 5%;
  }

  .warning1 {
    padding-top: 6%;
    font-size: 2.5em;
  }

  .warning2 {
    font-size: 2em;
  }
}
</style>
