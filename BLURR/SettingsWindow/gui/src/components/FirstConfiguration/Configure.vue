<template>
  <div id="configure-container">
    <WelcomeScreen :next="next" v-if="state === 0" />
    <PINSetup :next="setUpPin" v-if="state === 1" />
    <EnableFace :next="useFace" v-if="state === 2" />
    <AddEncoding v-if="state === 3" :next="next" :prev="prev" />
    <StartTracking v-if="state === 4" :next="start" />
  </div>
</template>

<script>
  import WelcomeScreen from "./WelcomeScreen.vue";
  import PINSetup from "./PINSetup.vue";
  import EnableFace from "./EnableFace.vue";
  import AddEncoding from "./AddEncoding.vue";
  import StartTracking from "./StartTracking.vue";
  import eelMixin from "../../lib/eelMixin.vue";

  export default {
    mixins: [eelMixin],
    components: {
      WelcomeScreen,
      PINSetup,
      EnableFace,
      AddEncoding,
      StartTracking,
    },
    props: {
      configure: Function,
    },
    data() {
      return {
        state: 0,
        pinCode: "",
        useFaceRecognition: false,
        faceModels: false,
      };
    },
    methods: {
      next() {
        this.state++;
      },
      prev() {
        this.state--;
      },
      setUpPin(pin) {
        this.pinCode = pin;
        this.state++;
      },
      useFace(useFace) {
        this.useFaceRecognition = useFace;
        if (useFace && !this.faceModels) {
          this.state++;
        } else {
          this.state += 2;
        }
      },
      start(tracking) {
        let settings = {
          tracking: tracking,
          faceRecognition: this.faceRecognition,
          unlockPin: this.pinCode,
        };
        this.setUp(settings);
        this.configure();
      },
    },
    async created() {
      let settings = await this.getGeneralSettings();
      this.faceModels = settings["faceEncodings"];
    },
  };
</script>

<style>
  #configure-container {
    min-width: 100vw;
    min-height: 100vh;
  }
</style>
