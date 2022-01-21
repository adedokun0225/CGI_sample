<template>
  <div id="app">
    <b-overlay v-if="!loggedIn" :show="!loaded">
      <LogIn :onLogin="signIn" />
    </b-overlay>
    <b-overlay v-else-if="firstStart" :show="!loaded">
      <Configure :configure="setUp" />
    </b-overlay>
    <div v-else id="settings-app">
      <LeftBar
        :selectedOption="selectedOption"
        :selectOption="selectOption"
      ></LeftBar>
      <div id="rightSide">
        <TopBar :loggedOut="loggedOut" />
        <ContentsContainer
          :selectedOption="selectedOption"
          id="contents-container"
        />
      </div>
    </div>
  </div>
</template>

<script>
  import Configure from "./components/FirstConfiguration/Configure.vue";
  import LogIn from "./components/LogIn/LogIn.vue";
  import LeftBar from "./components/LeftBar/LeftBar.vue";
  import TopBar from "./components/TopBar/TopBar.vue";
  import ContentsContainer from "./components/ContentsContainer.vue";
  import constants from "./lib/constants";
  import eelMixin from "./lib/eelMixin.vue";

  export default {
    name: "BlurrSettings",
    mixins: [eelMixin],
    components: { LeftBar, TopBar, ContentsContainer, Configure, LogIn },
    data() {
      return {
        selectedOption: constants.Screens.STATISTICS,
        firstStart: true,
        loaded: false,
        loggedIn: false,
      };
    },
    methods: {
      selectOption(option) {
        this.selectedOption = option;
      },
      methods: {
        selectOption(option) {
          this.selectedOption = option;
        },
        async setUp() {
          this.firstStart = false;
          this.firstStart = !(await this.wasSetUp());
        },
        signIn() {
          this.loggedIn = true;
        },
        loggedOut() {
          this.loggedIn = false;
        },
      },
      async created() {
        this.firstStart = !(await this.wasSetUp());
        this.loggedIn = await this.isLoggedIn();
        if (!this.loggedIn) {
          let wasAuthorized = await this.wasAuthorized();
          if (wasAuthorized) {
            this.$bvToast.toast(
              "It seems that your account no longer has a valid license. Please contact your manager.",
              {
                title: "Account expired",
                variant: "warning",
                toaster: "b-toaster-top-center",
                appendToast: true,
              }
            );
          }
        }
        this.loaded = true;
      },
      signIn() {
        this.loggedIn = true;
      },
      loggedOut() {
        this.loggedIn = false;
      },
    },
    async created() {
      this.firstStart = !(await this.wasSetUp());
      this.loggedIn = await this.isLoggedIn();
      this.loaded = true;
    },
  };
</script>

<style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    display: flex;
    flex-direction: row;
    max-height: 100vh;
  }

  #settings-app {
    display: flex;
    flex-direction: row;
    max-height: 100vh;
    flex-grow: 1;
  }

  #rightSide {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
  }

  #contents-container {
    flex-grow: 1;
    background: rgb(245, 245, 245);
  }
</style>
