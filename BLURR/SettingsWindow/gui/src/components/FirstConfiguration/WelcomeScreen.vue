<template>
  <div id="welcome-div">
    <h1 id="welcomeh">Welcome to BLURR!</h1>
    <h2 id="infoh">You need to set up some things before you start.</h2>
    <div id="bt-div">
      <b-button @click="proceed()" id="proceed-bt" variant="primary"
        >Proceed</b-button
      >
    </div>
  </div>
</template>

<script>
export default {
  props: {
    next: Function,
  },
  methods: {
    proceed() {
      console.log("Wow");
      this.next();
    },
  },
};
</script>

<style>
#welcome-div {
  display: flex;
  flex-direction: column;
  min-width: 100vw;
  min-height: 100vh;
  padding: 20px;
}

#proceed-bt {
  margin-left: auto;
}

#bt-div {
  margin-top: auto;
  display: flex;
  flex-direction: row;
}

#welcomeh {
  margin-top: auto;
}

#infoh {
  margin-bottom: auto;
}
</style>
