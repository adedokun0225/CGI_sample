<template>
  <div class="topBar">
    <div id="leftAligned">
      <b-dropdown
        size="lg"
        variant="link"
        toggle-class="text-decoration-none"
        no-caret
        right
      >
        <template #button-content>
          <b-icon icon="person" style="{height:45px}" />
        </template>
        <b-dropdown-item-button href="#" @click="logOutClicked()">
          Log Out
        </b-dropdown-item-button>
        <b-dropdown-item-button href="#" @click="exitClicked()">
          Exit Blurr
        </b-dropdown-item-button>
      </b-dropdown>
    </div>
    <b-modal v-model="showAcceptModal">
      <div slot="modal-title">
        PIN input needed
      </div>
      <h3 v-show="invalidPin">Invalid PIN code!</h3>

      <div>
        {{ modalText }}
        <b-form-input
          v-model="pinCode"
          :formatter="formatPIN"
          type="password"
        />
      </div>

      <div slot="modal-footer">
        <b-button @click="showAcceptModal = false"> Cancel </b-button>
        <b-button @click="okClicked()" variant="primary">
          {{ okText }}
        </b-button>
      </div>
    </b-modal>
  </div>
</template>

<script>
import eelMixin from "../../lib/eelMixin.vue";

export default {
  mixins: [eelMixin],
  props: {
    loggedOut: Function,
  },
  data() {
    return {
      modalText: "",
      okText: "",
      showAcceptModal: false,
      okClicked: () => {},
      pinCode: "",
      invalidPin: false,
    };
  },
  methods: {
    logOutClicked() {
      this.modalText = "Please enter the pin code to log out.";
      this.okText = "Log Out";
      this.okClicked = this.logOutFromBlurr;
      this.showAcceptModal = true;
    },
    async logOutFromBlurr() {
      let res = await this.logOut(this.pinCode);
      if (res) {
        this.loggedOut();
        this.showAcceptModal = false;
      } else {
        this.invalidPin = true;
      }
    },
    exitClicked() {
      this.modalText = "Please enter the pin code to exit Blurr.";
      this.okText = "Exit Blurr";
      this.okClicked = this.exitBlurr;
      this.showAcceptModal = true;
    },
    async exitBlurr() {
      let res = await this.quitApp(this.pinCode);
      if (res) {
        window.close();
      } else {
        this.invalidPin = true;
      }
    },
    formatPIN(pin) {
      this.pwdMatch = null;
      this.validOld = null;
      this.pwdShort = null;
      this.invalidPin = false;
      return String(pin)
        .replace(/\D/g, "")
        .substring(0, 4);
    },
  },
};
</script>

<style>
.topBar {
  min-width: 100%;
  height: 65px;
  border-bottom: 1px lightgray solid;
  display: flex;
  flex-direction: row;
}

#leftAligned {
  margin-left: auto;
  padding: 10px;
  font-size: 30px;
}
</style>
