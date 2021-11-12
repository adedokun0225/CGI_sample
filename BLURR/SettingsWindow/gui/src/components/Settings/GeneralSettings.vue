<template>
  <div id="generalSettingsDiv">
    <div id="settingsDiv">
      <b-form-checkbox v-model="enableTracking" name="tracking-check" switch>
        Enable tracking
      </b-form-checkbox>

      <b-form-checkbox
        v-model="faceRecognition"
        name="recognition-check"
        switch
        :disabled="facesDisabled"
      >
        Enable face recognition
      </b-form-checkbox>
    </div>

    <div id="bt-div">
      <b-button class="settings-bt" @click="setFromSettings()">
        Cancel
      </b-button>
      <b-button
        @click="showAcceptModal = true"
        variant="success"
        :disabled="!wasChanged"
        class="settings-bt"
      >
        Save Changes
      </b-button>
    </div>

    <b-modal v-model="showAcceptModal">
      <div slot="modal-title">
        PIN input needed
      </div>
      <h3 v-show="invalidPin">Invalid PIN code!</h3>

      <div>
        You need to insert the pin code to aply the changes:
        <b-form-input
          v-model="pinCode"
          :formatter="formatPIN"
          type="password"
        />
      </div>

      <div slot="modal-footer">
        <b-overlay :show="modalLoading">
          <b-button @click="showAcceptModal = false"> Cancel </b-button>

          <b-button @click="saveChanges()" variant="primary">
            Change settings
          </b-button>
        </b-overlay>
      </div>
    </b-modal>
  </div>
</template>

<script>
import eelMixin from "../../lib/eelMixin.vue";
export default {
  mixins: [eelMixin],
  data() {
    return {
      invalidPin: false,
      enableTracking: false,
      faceRecognition: false,
      settings: {},
      pinCode: "",
      showAcceptModal: false,
      modalLoading: false,
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
    startTrack() {
      this.startTracking();
    },
    stopTrack() {
      this.stopTracking();
    },
    setFromSettings() {
      this.enableTracking = this.settings["tracking"];
      this.faceRecognition = this.settings["faceRecognition"];
    },
    async saveChanges() {
      let updated = {
        tracking: this.enableTracking,
        faceRecognition: this.faceRecognition,
        faceEncodings: this.settings.faceEncodings,
      };
      this.modalLoading = true;
      let res = await this.setGeneralSettings(this.pinCode, updated);
      this.modalLoading = false;
      if (res) {
        this.showAcceptModal = false;
        this.settings = updated;
        this.pinCode = "";
        this.setFromSettings();
      } else {
        this.invalidPin = true;
      }
    },
  },
  async created() {
    this.settings = JSON.parse(await this.getGeneralSettings());
    this.setFromSettings();
  },
  computed: {
    wasChanged() {
      return (
        this.settings["tracking"] != this.enableTracking ||
        this.settings["faceRecognition"] != this.faceRecognition
      );
    },
    facesDisabled() {
      return !this.settings["faceEncodings"];
    },
  },
};
</script>

<style scoped>
#generalSettingsDiv {
  display: flex;
  flex-direction: column;
  padding: 10px;
  text-align: left;
}

#bt-div {
  display: flex;
  flex-direction: row;
  margin-top: 20px;
}

.settings-bt {
  flex-grow: 1;
}

.settingsLabel {
  font-family: Helvetica;
  font-weight: 600;
  font-size: 15px;
}
</style>
