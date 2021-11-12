<template>
  <div id="welcome-div">
    <h2 id="infoh">
      Do you want to use face recognition to improve the security level?
    </h2>
    <div id="bt-div">
      <b-button @click="next(false)" id="noface-bt" variant="outline-secondary">
        No, I want to only use eye tracking.
      </b-button>
      <b-button @click="next(true)" id="face-bt"
        >Yes, I want to use face recognition.</b-button
      >
    </div>
  </div>
</template>

<script>
export default {
  props: {
    next: Function,
  },
};
</script>

<style>
#welcome-div {
  min-width: 100vw;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

#infoh {
  margin-top: auto;
  margin-bottom: auto;
}

#bt-div {
  display: flex;
  flex-direction: row;
}

#noface-bt {
  margin-left: auto;
  margin-right: 5px;
}
</style>
