<template>
  <b-modal v-model="showModal">
    <div slot="modal-title">
      {{ modalTitle + nameTitle }}
    </div>

    <div slot="modal-footer" id="modal-footer">
      <b-button @click="hide()"> Cancel </b-button>
      <b-overlay :show="isLoading" rounded="sm">
        <b-button @click="proceedToFace()" variant="primary" v-if="selectName">
          Select name
        </b-button>
        <b-button variant="primary" v-else @click="addEncoding()">
          Add encoding
        </b-button>
      </b-overlay>
    </div>

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
  </b-modal>
</template>

<script>
  import eelMixin from "../../../lib/eelMixin.vue";
  export default {
    mixins: [eelMixin],
    props: {
      show: Boolean,
      hideModal: Function,
      name: String,
    },
    data() {
      return {
        frameSrc: "",
        isOpen: true,
        modalTitle: "Add face encoding",
        showModal: false,
        selectName: false,
        addingError: false,
        addingErrorMsg: "",
        nameToAdd: "",
        proceedButtonText: "",
        nameError: "",
        nameState: null,
        isLoading: false,
      };
    },
    methods: {
      async grabFrame() {
        let src = await this.getFrame();
        this.frameSrc = src.substring(2, src.length - 1);
        if (!this.showModal) return;
        this.grabFrame();
      },
      async addEncoding() {
        this.isLoading = true;
        let res = await this.addFaceEncoding(this.nameToAdd);
        this.isLoading = false;
        if (res.successful) {
          this.encodingAdded();
          this.hide();
        } else {
          this.addingError = true;
          this.addingErrorMsg = res.error;
        }
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
      openModal() {
        this.isLoading = false;
        this.showModal = true;
        if (this.name && this.name.length > 0) {
          //Adding an encoding for an existing member
          console.log("Name is here! in modal");
          this.nameToAdd = this.name;
          this.selectName = false;
          this.grabFrame();
        } else {
          this.nameToAdd = "";
          this.selectName = true;
        }
      },
      hide() {
        this.showModal = false;
      },
      encodingAdded() {
        this.$bvToast.toast("Succesfully added the encoding!", {
          title: "Success",
          variant: "success",
          toaster: "b-toaster-top-center",
          appendToast: true,
        });
      },
    },
    computed: {
      nameTitle() {
        if (!this.selectName) {
          return " for " + this.nameToAdd;
        }
        return "";
      },
    },
    beforeDestroy() {
      this.isOpen = false;
    },
    watch: {
      nameToAdd() {
        this.nameState = null;
      },
      show() {
        if (this.show) {
          this.openModal();
        } else {
          if (!this.showModal) this.showModal = false;
        }
      },
      showModal() {
        if (!this.showModal && this.show) {
          this.hideModal();
        }
      },
    },
  };
</script>

<style>
  #cameraDiv {
    display: flex;
    flex-direction: column;
    text-align: center;
  }

  #modal-footer {
    display: flex;
    flex-direction: row;
  }
</style>
