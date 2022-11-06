<template>
  <div class="grid-widget">
    <smart-widget-grid :layout="layout">
      <smart-widget
        v-for="(widget, index) in widgets"
        :slot="index"
        :title="widget.title"
        :sub-title="widget.subTitle"
        :key="index"
      >
        <template #toolbar>
          <v-btn icon class="pa-2" @click="removeWidget(index)">
            <v-icon> mdi-close </v-icon>
          </v-btn>
        </template>
        <div class="layout-center">
          <h3>{{ widget.content }}</h3>
        </div>
        <Chart :config="widget.config" :index="index" />
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
  },
};
</script>
