<template>
  <div>
    <h5 v-if="selectedOption === constants.Screens.STATISTICS" id="statistics">
      Statistics will be added later
    </h5>

    <GeneralSettings
      v-if="selectedOption === constants.Screens.GENERAL_SETTINGS"
    />

    <PINSettings v-if="selectedOption === constants.Screens.PIN_SETTINGS" />

    <FacesSettings v-if="selectedOption === constants.Screens.FACE_SETTINGS" />
  </div>
</template>

<script>
import GeneralSettings from "./Settings/GeneralSettings.vue";
import PINSettings from "./Settings/PINSettings.vue";
import FacesSettings from "./Settings/FacesSettings.vue";
import constants from "./../lib/constants";
export default {
  components: { GeneralSettings, PINSettings, FacesSettings },
  props: {
    selectedOption: String,
  },
  data() {
    return {
      constants,
    };
  },
};
</script>

<style>
#statistics {
  padding: 10px;
}
</style>
