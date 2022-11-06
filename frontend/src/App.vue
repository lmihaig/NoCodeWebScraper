<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <dialogModal @addWidget="addWidget" />
        <span class=".text-lg-h6 pl-3">add something</span>
      </div>
    </v-app-bar>

    <v-main>
      <WidgetsGrid v-if="widgets.length" :widgets="widgets" />
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
      const labels = ['January', 'February', 'March', 'April', 'May', 'June'];

      const data = {
        labels: labels,
        datasets: [
          {
            label: 'My First dataset',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [0, 10, 5, 2, 20, 30, 45],
          },
        ],
      };

      const config = {
        type: 'line',
        data: data,
        options: {},
      };

      this.widgets.push({
        title: input,
        subTitle: input,
        content: input,
        config,
      });
    },
  },
};
</script>
