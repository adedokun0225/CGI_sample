<template>
  <div id="faceSettings">
    <!--
    <video
      v-show="false"
      ref="camera"
      :width="450"
      :height="337.5"
      autoplay
    ></video>
    <canvas v-show="false" ref="canvas"> </canvas>
    <img ref="img" />
    <button @click="takePhoto()">Test</button>
    -->
    <b-overlay :show="loadingTable">
      <b-table :items="items" :fields="fields">
        <template #cell(actions)="row">
          <b-button
            size="sm"
            variant="success"
            @click="addAnotherEncoding(row.item.name)"
            >Add encoding</b-button
          >

          <b-button size="sm" variant="danger" @click="deleteRow(row)"
            >Delete</b-button
          >
        </template>
      </b-table>
    </b-overlay>

    <div id="btsContainer">
      <b-button
        class="facesBt"
        variant="outline-primary"
        @click="addNewMember()"
        >Add a new member</b-button
      >
      <b-button
        class="facesBt"
        v-b-modal="'info-modal'"
        variant="outline-secondary"
        >More information</b-button
      >
    </div>

    <b-modal id="info-modal">
      Here you can manage the faces that are authorized to use the computer; you
      can delete old members, add new members or add new encodings of faces for
      already existing members (for example with beard).
    </b-modal>

    <AddFaceModal
      :show="showAddModal"
      :hideModal="hideAddFaceModal"
      :name="nameToAdd"
    />
  </div>
</template>

<script>
import eelMixin from "../../lib/eelMixin.vue";
import AddFaceModal from "./AddFace/AddFaceModal.vue";

export default {
  components: { AddFaceModal },
  mixins: [eelMixin],
  data() {
    return {
      stream: null,
      items: [],
      fields: [
        { key: "name", label: "Name", sortable: true },
        { key: "count", label: "Face encodings" },
        { key: "actions", label: "" },
      ],
      showAddModal: false,
      nameToAdd: "",
      loadingTable: false,
    };
  },
  async created() {
    this.fetchTableData();
  },
  methods: {
    async fetchTableData() {
      this.loadingTable = true;
      let info = await this.getFacesInfo();
      this.items = JSON.parse(info);
      this.loadingTable = false;
    },
    async deleteRow(row) {
      this.$bvModal
        .msgBoxConfirm(
          "Are you sure you want to delete " + row.item.name + "?",
          {
            title: "Please Confirm",
            okVariant: "danger",
            okTitle: "YES",
            cancelTitle: "NO",
            footerClass: "p-2",
            hideHeaderClose: false,
            centered: true,
          }
        )
        .then(async (value) => {
          if (value) {
            console.log("Deleting ", row);
            await this.removePerson(row.item.name);
            this.fetchTableData();
          }
        })
        .catch((err) => {
          // An error occurred
          console.error(err);
        });
    },
    addAnotherEncoding(name) {
      this.nameToAdd = name;
      this.showAddModal = true;
      console.log("Opened modal for " + name);
    },
    addNewMember() {
      this.nameToAdd = "";
      this.showAddModal = true;
    },
    hideAddFaceModal() {
      this.showAddModal = false;
      console.log("Closing modal");
      this.fetchTableData();
    },
  },
};
</script>

<style>
#faceSettings {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

#btsContainer {
  display: flex;
  flex-direction: row;
  margin-top: auto;
}

.facesBt {
  flex-grow: 1;
}
</style>
