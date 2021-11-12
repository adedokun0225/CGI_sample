<template>
  <div id="login-container">
    <div id="logo-container">
      <img src="../../assets/BLURR.png" id="blurr-logo" />
    </div>
    <div id="middle-container">
      <h3>{{ signText }}</h3>

      <b-form-group
        id="email-group"
        label="Email adress"
        label-for="email-input"
        :invalid-feedback="emailFeedback"
      >
        <b-form-input
          id="email-input"
          v-model="email"
          state="User with this email adress already exists!"
          :formatter="onChange"
          trim
          type="email"
        />
      </b-form-group>

      <b-form-group
        v-if="hasAccount"
        id="password-group"
        label="Password"
        label-for="password-input"
        invalid-feedback="Invalid email and/or password!"
      >
        <b-form-input
          id="password-input"
          v-model="password"
          :state="isPasswordValid"
          :formatter="onChange"
          trim
          type="password"
        />
      </b-form-group>

      <div id="buttons-container">
        <b-button
          id="toggle-button"
          class="bottom-button"
          @click="toggleMethod()"
        >
          {{ toggleText }}
        </b-button>
        <b-button id="sign-button" class="bottom-button" @click="sign()">
          {{ signText }}
        </b-button>
      </div>
    </div>
  </div>
</template>

<script>
const SIGN_UP_SUCCESS =
  "Succesfully submitted a request. You will receive an email with a password after the admistrator has accepted your registration.";

import eelMixin from "../../lib/eelMixin.vue";

export default {
  mixins: [eelMixin],
  props: {
    onLogin: Function,
  },
  data() {
    return {
      email: "",
      isEmailValid: null,
      password: "",
      isPasswordValid: null,
      hasAccount: true,
    };
  },
  methods: {
    toggleMethod() {
      this.hasAccount = !this.hasAccount;
    },
    onChange(str) {
      this.isEmailValid = null;
      this.isPasswordValid = null;
      return str.trim();
    },
    sign() {
      if (this.hasAccount) this.signIn();
      else this.register();
    },
    async signIn() {
      let success = await this.logIn(this.email, this.password);
      console.log("Tried to login, result=" + success);
      if (success) {
        this.onLogin();
      } else {
        this.isPasswordValid = false;
      }
    },
    async register() {
      let res = JSON.parse(await this.signUp(this.email));

      if (res.successful) {
        this.$bvToast.toast(SIGN_UP_SUCCESS, {
          title: "Submitted your request",
          variant: "success",
          toaster: "b-toaster-top-center",
          appendToast: true,
        });
        this.password = "";
        this.toggleMethod();
      } else {
        this.$bvToast.toast(res.message, {
          title: "Error",
          variant: "warning",
          toaster: "b-toaster-top-center",
          appendToast: true,
        });
      }
    },
  },
  computed: {
    toggleText() {
      return this.hasAccount
        ? "Create a new account"
        : "I already have an account";
    },
    signText() {
      return this.hasAccount ? "Sign In" : "Sign Up";
    },
  },
  async created() {
    this.email = await this.getEmail();
  },
};
</script>

<style scoped>
#login-container {
  min-width: 100vw;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  text-align: center;
}

#blurr-logo {
  height: 15px;
}

#logo-container {
  padding: 20px 40px;
  margin-bottom: -50px;
  text-align: left;
}

#middle-container {
  margin: auto;
  display: flex;
  flex-direction: 1;
  min-width: 40%;
  flex-direction: column;
}

#buttons-container {
  display: flex;
  flex-direction: row;
}

.bottom-button {
  flex-grow: 1;
  width: 50%;
}
</style>
