<template>
  <div class="grid-widget">
    <smart-widget-grid :layout="layout" @layout-updated="resize">
      <smart-widget v-for="(widget, index) in widgets" :slot="index" :title="widget.title" :sub-title="widget.subTitle"
        :key="index">

        <template #toolbar>
          <v-btn icon class="pa-2" @click="removeWidget(index)">
            <v-icon> mdi-close </v-icon>
          </v-btn>
        </template>
        <!-- {{ Object.keys(widget.content) }}
        {{ widget.content[Object.keys(widget.content)[0]][0].val.length }} -->
        <!-- <div class="layout-center"> -->
        <div v-for="i in (widget.content[Object.keys(widget.content)[0]][0].val.length)">
          <div v-for="name in Object.keys(widget.content)">
            <!-- {{ widget.content[name][0].val }} -->
            <h5>{{ widget.content[name][0].val[i - 1] }}</h5>
          </div>
          <v-divider></v-divider>
        </div>
        <!-- </div> -->
      </smart-widget>
    </smart-widget-grid>
  </div>
</template>

<script>
import Chart from './chart.vue';
export default {
  name: 'GridWidget',
  components: {
    Chart,
  },
  props: {
    widgets: {
      type: Array,
    },
    layout: {
      type: Array,
    },
  },
  data() {
    return {};
  },
  methods: {
    removeWidget(index) {
      this.$emit('removeWidget', index);
    },
    async resize() {
      const body = [];
      for (let entry of this.layout) {
        body.push({
          x: entry.x,
          y: entry.y,
          width: entry.w,
          height: entry.h
        });
      }
      await fetch('/api/dashboard/reorder', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      })
    }
  },
};
</script>
