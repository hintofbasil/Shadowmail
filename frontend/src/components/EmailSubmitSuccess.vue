<template>
  <div v-if="email">
    <div class="new-email-success-response">
      <i class="material-icons descriptor-icon descriptor-icon-mail">
        mail_outline
      </i>
      <br />
    </div>
    <div class="input-then-button-layout">
      <button
        type="submit"
        value="content_copy"
        title="Copy to clipboard"
        id="email-copy-button"
        v-on:click="copy"
      >
        <i class="material-icons descriptor-icon submit-material-icon">
          content_copy
        </i>
        <br />
      </button>
      <span class="submit-span">
        <input
          type="email"
          id="new-email-success-text"
          v-model="email"
          readOnly
        />
      </span>
      <div id="copy-status">
        {{ copyStatus }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: () => {
    return {
      copyStatus: null
    };
  },
  methods: {
    copy: function(event) {
      event.preventDefault();
      const emailInput = document.getElementById("new-email-success-text");
      emailInput.select();
      const success = document.execCommand("copy");
      this.copyStatus = success ? "Copied!" : "Unable to copy";
    }
  },
  props: ["email"]
};
</script>

<style lang="scss" scoped>
@import "../colors";

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

.new-email-success-response {
  text-align: center;
  color: $success-text-color;
}

.submit-material-icon {
  font-size: 20px;
  line-height: 38px;
}

#new-email-success {
  margin-bottom: 5%;
}

#new-email-error {
  margin-bottom: 5%;
}

#copy-status {
  text-align: center;
}

.descriptor-icon-mail {
  width: 50%;
  font-size: 4em;
}
</style>
