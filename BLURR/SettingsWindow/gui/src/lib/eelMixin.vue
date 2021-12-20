<script>
  export default {
    methods: {
      async eelResetPin(newPin) {
        return await eel.resetPIN(newPin)();
      },
      async eelChangePin(oldPin, newPin) {
        return await eel.changePIN(oldPin, newPin)();
      },
      async getFacesInfo() {
        return await eel.getFacesInfo()();
      },
      async getFrame() {
        return await eel.getFrame()();
      },
      async addFaceEncoding(name) {
        return await eel.addFaceEncoding(name)();
      },
      async checkName(name) {
        return await eel.checkName(name)();
      },
      async removePerson(name) {
        return await eel.deletePerson(name)();
      },
      async startTracking() {
        return await eel.startTracking()();
      },
      async stopTracking() {
        return await eel.stopTracking()();
      },
      async getGeneralSettings() {
        return await eel.getGeneralSettings()();
      },
      async setGeneralSettings(pinCode, settings) {
        return await eel.setGeneralSettings(pinCode, settings)();
      },
      async wasSetUp() {
        return await eel.wasSetUp()();
      },
      async setUp(settings) {
        return await eel.setUp(settings)();
      },
      async isLoggedIn() {
        return await eel.isLoggedIn()();
      },
      async getEmail() {
        return await eel.getEmail()();
      },
      async logIn(username, password) {
        return await eel.logIn(username, password)();
      },
      async signUp(email) {
        return await eel.signUp(email)();
      },
      async logOut(pin) {
        return await eel.logOut(pin)();
      },
      async quitApp(pin) {
        return await eel.quitApp(pin)();
      },
      async wasAuthorized() {
        return await eel.wasAuthorized()();
      },
    },
  };
</script>
