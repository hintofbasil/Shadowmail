<template>
  <div class="background">
    <div class="container">
      <div class="row descriptor-container">
        <DescriptorElement
          v-for="element of content"
          :element="element"
          :key="element.title"
        />
      </div>
    </div>
  </div>
</template>

<script>
const CONTENT = [
  {
    title: "Simple",
    symbol: "done",
    description: `
      <span>
        ShadowMail is simple to use.
        Simply enter your email address and start using your
        private, virtual email address immediately.
      </span>
    `
  },
  {
    title: "Secure",
    symbol: "lock",
    description: `
      <span>
        ShadowMails is 100%
        <a href="https://github.com/hintofbasil/ShadowMail"
          target="_blank"
          rel="noopener noreferrer"
        >
          open source
        </a>.
        You can audit our code yourself to ensure you&apos;re comfortable with our practises.
      </span>
    `
  },
  {
    title: "Private",
    symbol: "fingerprint",
    description: `
      <span>
        We care about privacy as much as you do.  As such we never save, read or otherwise
        monitor your emails.
      </span>
    `
  }
];

import DescriptorElement from "@/components/DescriptorElement.vue";

export default {
  computed: {
    content: () => CONTENT
  },
  components: {
    DescriptorElement
  }
};
</script>
