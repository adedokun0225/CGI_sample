<template>
  <div id="encodingScreen">
    <h2 id="info-h">
      Please add an encoding of your face so that Blurr can recognize you
    </h2>
    <div v-if="selectName" id="name-select">
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
      <div id="imageDiv">
        <img
          ref="img"
          id="cameraImage"
          v-bind:src="'data:image/png;base64,' + frameSrc"
        />
      </div>
    </div>

    <div id="bt-div">
      <b-button
        class="bottom-bt"
        id="back-bt"
        @click="goBack()"
        variant="outline-secondary"
      >
        Back
      </b-button>

      <b-overlay
        class="bottom-bt"
        id="bt-overlay"
        :show="isLoading"
        rounded="sm"
      >
        <b-button class="overlay-bt" @click="proceedToFace()" v-if="selectName">
          Select name
        </b-button>
        <b-button class="overlay-bt" v-else @click="addEncoding()">
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
        let res = await this.addFaceEncoding(this.nameToAdd);
        this.isLoading = false;
        if (res.successful) {
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

<style>
  .overlay-bt {
    width: 100%;
  }

  #encodingScreen {
    max-width: 100vw;
    max-height: 100vh;
    min-width: 100vw;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    padding: 15px;
  }

  #cameraDiv {
    display: flex;
    flex-direction: column;
    align-self: center;
  }

  #imageDiv {
    display: flex;
    flex-direction: row;
    padding: 20px;
    align-self: center;
  }

  #cameraImage {
    height: 80vmin;
    width: 80vmin;
    object-fit: contain;
    align-self: center;
  }

  #bt-div {
    margin-top: auto;
    display: flex;
    flex-direction: row;
  }

  .bottom-bt {
    min-width: 20%;
  }

  #back-bt {
    margin-left: auto;
    margin-right: 5px;
  }

  #name-select {
    margin-top: auto;
    margin-bottom: auto;
  }
</style>
