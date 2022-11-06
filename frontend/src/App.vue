<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <dialogModal @addWidget="addWidget" />
        <span class=".text-lg-h6 pl-3">add something</span>
      </div>
    </v-app-bar>

    <v-main>
      <WidgetsGrid
        v-if="widgets.length"
        :layout="layout"
        :widgets="widgets"
        @removeWidget="removeWidget"
      />
      <h2 v-else>no widgets :(</h2>
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
      layout: [],
    };
  },
  async mounted() {
    await fetch('http://192.168.22.158:8069/api/widget', {
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    })
      .then((response) => response.json())
      .then((data) => console.log(data));
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

      this.layout.push({
        x: 0,
        y: 0,
        w: 4,
        h: 4,
        i: this.widgets.length,
      });
      this.widgets.push({
        title: input,
        subTitle: input,
        content: input,
        config,
      });
    },
    removeWidget(index) {
      this.widgets.splice(index, 1);
      this.layout.splice(index, 1);
      for (let l of this.layout) {
        if (l.i > index) {
          l.i -= 1;
        }
      }
      console.log(this.widgets);
      console.log(this.layout);
    },
  },
};
</script>
