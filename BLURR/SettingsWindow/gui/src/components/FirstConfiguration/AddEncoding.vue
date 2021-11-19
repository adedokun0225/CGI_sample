<template>
  <div>
    <h2>Please add an encoding of your face so that Blurr can recognize you</h2>
    <div v-if="selectName">
      <b-form-label for="name-input"> Member name: </b-form-label>
      <b-form-input
        id="name-input"
        v-model="nameToAdd"
        :state="nameState"
      ></b-form-input>
      <b-form-invalid-feedback id="old-feedback">
        {{ nameError }}
      </b-form-invalid-feedback>
    </div>

    <div v-show="!selectName" id="cameraDiv">
      <h2 v-if="addingError">{{ addingErrorMsg }}</h2>
      <img ref="img" v-bind:src="'data:image/png;base64,' + frameSrc" />
    </div>

    <div id="bt-div">
      <b-button @click="goBack()"> Back </b-button>

      <b-overlay id="bt-overlay" :show="isLoading" rounded="sm">
        <b-button @click="proceedToFace()" variant="primary" v-if="selectName">
          Select name
        </b-button>
        <b-button variant="primary" v-else @click="addEncoding()">
          Add encoding
        </b-button>
      </b-overlay>
    </div>
  </div>
</template>

<script>
  import eelMixin from "../../lib/eelMixin.vue";

  export default {
    props: {
      prev: Function,
      next: Function,
    },
    mixins: [eelMixin],
    data() {
      return {
        frameSrc: "",
        active: true,
        isLoading: false,
        selectName: true,
        nameState: null,
        nameError: "",
        nameToAdd: "",
        addingError: false,
        addingErrorMsg: "",
      };
    },
    methods: {
      async grabFrame() {
        let src = await this.getFrame();
        this.frameSrc = src.substring(2, src.length - 1);
        if (!this.active) return;
        this.grabFrame();
      },
      goBack() {
        this.active = false;
        this.prev();
      },
      async proceedToFace() {
        this.isLoading = true;
        let valid = await this.checkName(this.nameToAdd.trim());
        this.isLoading = false;
        if (valid) {
          this.selectName = false;
          this.grabFrame();
        } else {
          this.nameState = false;
          this.nameError =
            this.nameToAdd.trim() == ""
              ? "Name cannot be empty!"
              : "Member already exists!";
        }
      },
      async addEncoding() {
        this.isLoading = true;
        let res = JSON.parse(await this.addFaceEncoding(this.nameToAdd));
        this.isLoading = false;
        if (res.succesful) {
          this.next();
        } else {
          this.addingError = true;
          this.addingErrorMsg = res.error;
        }
      },
    },
    created() {
      this.grabFrame();
    },
  };
</script>

<style></style>
