import { createStore } from 'vuex'

export default createStore({
  namespaced: true,
  modules: {
  },
  state: {
    darkMode: false
  },
  mutations: {
    toggleDarkMode (state) {
      state.darkMode = !state.darkMode
    }
  },
  actions: {
    toggleDarkMode ({ commit }) {
      commit('toggleDarkMode')
    }
  },
  getters: {
    darkMode: state => {
      return state.darkMode
    }
  }
})
