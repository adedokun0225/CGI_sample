<template>
  <div id="welcome-div">
    <h2 id="infoh">
      You're ready to start using BLURR.
      <br />
      Do you want to enable tracking?
    </h2>
    <div id="bt-div">
      <b-button
        @click="next(false)"
        id="notrack-bt"
        variant="outline-secondary"
      >
        No, I want to enable it later manually.
      </b-button>
      <b-button @click="next(true)" id="track-bt"
        >Yes, I want to start right away.</b-button
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

#notrack-bt {
  margin-left: auto;
  margin-right: 5px;
}
</style>
