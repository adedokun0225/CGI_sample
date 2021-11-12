<template>
  <div id="leftBar">
    <div id="logoContainer">
      <img src="../../assets/BLURR.png" id="blurrLogo" />
    </div>

    <div id="leftBtContainer">
      <div id="statisticsLabel" class="btLabel">
        USAGE STATISTICS
      </div>

      <div
        id="statisticsBt"
        class="leftBt"
        v-on:click="select(screens.STATISTICS)"
        v-bind:class="{ leftBtClicked: selectedOption === screens.STATISTICS }"
      >
        <b-icon icon="graph-up" />
        Statistics
      </div>

      <div id="settingsLabel" class="btLabel">
        SETTINGS
      </div>

      <div
        id="generalSettingsBt"
        class="leftBt"
        v-on:click="select(screens.GENERAL_SETTINGS)"
        v-bind:class="{
          leftBtClicked: selectedOption === screens.GENERAL_SETTINGS,
        }"
      >
        <b-icon icon="gear" />
        General settings
      </div>

      <div
        id="facesSettingsBt"
        class="leftBt"
        v-on:click="select(screens.FACE_SETTINGS)"
        v-bind:class="{
          leftBtClicked: selectedOption === screens.FACE_SETTINGS,
        }"
      >
        <b-icon icon="person-bounding-box" />
        Authorized faces
      </div>

      <div
        id="pinSettingsBt"
        class="leftBt"
        v-on:click="select(screens.PIN_SETTINGS)"
        v-bind:class="{
          leftBtClicked: selectedOption === screens.PIN_SETTINGS,
        }"
      >
        <b-icon icon="key" />
        Change PIN Code
      </div>
    </div>
    <h5 id="version-text">v0.0.2Alpha - For testing only</h5>
  </div>
</template>

<script>
import constants from "../../lib/constants";
export default {
  props: {
    selectOption: Function,
    selectedOption: String,
  },
  methods: {
    select(option) {
      this.selectOption(option);
    },
  },
  data() {
    return {
      screens: constants.Screens,
    };
  },
};
</script>

<style>
#leftBar {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  border-right: 1px lightgray solid;
}

#blurrLogo {
  height: 15px;
}

#logoContainer {
  padding: 20px 40px;
  border-bottom: 1px lightgray solid;
}

.btLabel {
  font-family: Helvetica;
  font-weight: 500;
  font-size: 14px;
  padding: 5px 20px;
  margin-top: 10px;
  text-align: left;
  color: #797799;
}

.leftBt {
  text-align: left;
  padding-left: 30px;
  padding-top: 5px;
  padding-bottom: 5px;
}

.leftBt:hover {
  background-color: rgb(240, 240, 240);
  cursor: pointer;
}

.leftBtClicked {
  background: lightgray !important;
}

#version-text {
  margin-top: auto;
  margin-right: 10px;
  text-align: right;
  font-size: small;
}
</style>
