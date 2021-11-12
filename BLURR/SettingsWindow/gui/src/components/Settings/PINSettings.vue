<template>
  <div id="pinCodeSettings">
    <div id="pinSettings">
      <h2 class="settingsLabel">CHANGE PIN CODE</h2>

      <div v-if="succesfullyChanged" id="successText">
        Succesfully changed the PIN code!
      </div>

      <b-form-group
        id="oldPinGroup"
        label="Old PIN code"
        label-for="oldPinInput"
        v-if="!forgotPin"
      >
        <b-form-input
          id="oldPinInput"
          type="password"
          :formatter="formatPIN"
          v-model="oldPin"
          :state="validOld"
        />
        <b-form-invalid-feedback id="old-feedback">
          Invalid PIN!
        </b-form-invalid-feedback>
      </b-form-group>

      <div v-else id="forgotText">
        Please input a new PIN code. After clicking on "Change the PIN code" you
        will be logged out from the system.
      </div>

      <b-form-group
        id="newPinGroup"
        label="New PIN code"
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

      <div id="changeBts">
        <b-button
          v-if="!forgotPin"
          id="forgotPinBt"
          class="changeBt"
          variant="outline-primary"
          v-on:click="toggleForgot()"
        >
          I forgot my PIN code
        </b-button>
        <b-button
          v-else
          id="forgotPinBt"
          class="changeBt"
          variant="outline-primary"
          v-on:click="toggleForgot()"
        >
          I remember the PIN code
        </b-button>

        <b-button
          id="changePinBt"
          class="changeBt"
          variant="primary"
          v-on:click="changePIN()"
        >
          Change the PIN code
        </b-button>
      </div>
    </div>
  </div>
</template>

<script>
import eelMixin from "./../../lib/eelMixin.vue";

export default {
  mixins: [eelMixin],
  data() {
    return {
      forgotPin: false,
      succesfullyChanged: false,
      oldPin: "",
      newPin: "",
      repeatPin: "",
      validOld: null,
      pwdMatch: null,
      pwdShort: null,
    };
  },
  methods: {
    formatPIN(pin) {
      this.pwdMatch = null;
      this.validOld = null;
      this.pwdShort = null;
      return String(pin)
        .replace(/\D/g, "")
        .substring(0, 4);
    },
    toggleForgot() {
      this.forgotPin = !this.forgotPin;
    },
    async changePIN() {
      if (this.newPin !== this.repeatPin) {
        console.log("NO MATCH");
        this.pwdMatch = false;
        return;
      }
      if (this.newPin.length != 4) {
        console.log("TOO SHORT");
        this.pwdShort = false;
        return;
      }
      let result = false;
      if (this.forgotPin) {
        result = this.eelResetPin(this.newPin);
      } else {
        result = await this.eelChangePin(this.oldPin, this.newPin);
      }

      if (result) {
        this.newPin = this.oldPin = this.repeatPin = "";
        this.succesfullyChanged = true;
      } else {
        this.validOld = false;
      }
    },
  },
};
</script>

<style>
#pinCodeSettings {
  display: flex;
  flex-direction: column;
  padding: 10px;
  text-align: left;
}

#successText {
  margin: 10px 0;
  color: green;
}

.settingsLabel {
  font-family: Helvetica;
  font-weight: 600;
  font-size: 15px;
}

#forgotText {
  margin-bottom: 10px;
}

#changeBts {
  display: flex;
  flex-direction: row;
}

.changeBt {
  flex-grow: 1;
}
</style>
