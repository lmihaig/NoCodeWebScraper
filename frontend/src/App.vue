<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <dialogModal @addWidget="addWidget" />
        <span class=".text-lg-h6 pl-3">add something</span>
      </div>
    </v-app-bar>

    <v-main>
      <WidgetsGrid v-if="widgets.length" :layout="layout" :widgets="widgets" @removeWidget="removeWidget" />
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
    const data = await fetch('/api/widget').then((response) => response.json());
    console.log(data);
    for (let entry of data) {
      this.layout.push({
        x: entry.x,
        y: entry.y,
        w: entry.width,
        h: entry.height,
        i: this.widgets.length
      });
      const data1 = await fetch('/api/source/' + entry.source).then((response) => response.json());
      console.log(data1)
      this.widgets.push({
        title: entry.name,
        content: data1
      })
    }
    
  },
  methods: {
    async addWidget() {
      const data = await fetch('/api/widget').then((response) => response.json());
      this.widgets = [];
      this.layout = [];
      for (let entry of data) {
        this.layout.push({
          x: entry.x,
          y: entry.y,
          w: entry.width,
          h: entry.height,
          i: this.widgets.length
        });
        const data1 = await fetch('/api/source/' + entry.source).then((response) => response.json());
        console.log(data1)
        this.widgets.push({
          title: entry.name,
          content: data1
        })
      }
    },
    async removeWidget(index) {
      await fetch('/api/widget/' + index, {
        method: 'DELETE'
      });
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
