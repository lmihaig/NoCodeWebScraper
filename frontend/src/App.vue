<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <dialogModal @addWidget="addWidget" />
        <span class=".text-lg-h6 pl-3">add something</span>
      </div>
    </v-app-bar>

    <v-main>
      <WidgetsGrid :widgets="widgets" />
    </v-main>
  </v-app>
</template>

<script>
import dialogModal from './components/addModal.vue';
import WidgetsGrid from './components/WidgetsGrid.vue';

export default {
  name: 'App',

  components: {
    dialogModal,
    WidgetsGrid,
  },

  data() {
    return {
      widgets: [],
    };
  },
  methods: {
    addWidget(input) {
      this.widgets.push({
        title: input,
        subTitle: input,
        content: input,
      });
    },
  },
};
</script>
