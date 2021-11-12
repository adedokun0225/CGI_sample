<template>
  <div id="pinSetup-div">
    <h2 id="hinfo">
      Please set up your PIN code.
      <br />
      It will be used to unlock the screen after Blurr has been activated.
    </h2>

    <b-form-group
      class="pin-group"
      id="newPinGroup"
      label="PIN code"
      label-for="newPinInput"
    >
      <b-form-input
        id="newPinInput"
        type="password"
        :formatter="formatPIN"
        v-model="newPin"
        :state="pwdShort"
      />
      <b-form-invalid-feedback id="match-feedback">
        The pin code has to be 4 digits long!
      </b-form-invalid-feedback>
    </b-form-group>

    <b-form-group
      class="pin-group"
      id="repeatPinGroup"
      label="Repeat new PIN code"
      label-for="repeatPinInput"
    >
      <b-form-input
        id="repeatPinInput"
        type="password"
        :formatter="formatPIN"
        v-model="repeatPin"
        :state="pwdMatch"
      />
      <b-form-invalid-feedback id="match-feedback">
        The 2 pin codes don't match!
      </b-form-invalid-feedback>
    </b-form-group>

    <div id="bt-div">
      <b-button id="setup-bt" variant="primary" @click="setPin()">
        Set the pin code
      </b-button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    next: Function,
  },
  data() {
    return {
      newPin: "",
      repeatPin: "",
      pwdShort: null,
      pwdMatch: null,
    };
  },
  methods: {
    formatPIN(pin) {
      this.pwdMatch = null;
      this.pwdShort = null;
      return String(pin)
        .replace(/\D/g, "")
        .substring(0, 4);
    },
    setPin() {
      if (this.newPin.length != 4) {
        this.pwdShort = false;
        return;
      }

      if (this.newPin != this.repeatPin) {
        this.pwdMatch = false;
        return;
      }

      this.next(this.newPin);
    },
  },
};
</script>

<style>
#pinSetup-div {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

#hinfo {
  margin-top: auto;
}

#bt-div {
  display: flex;
  flex-direction: row;
}

#setup-bt {
  margin-left: auto;
}
</style>
