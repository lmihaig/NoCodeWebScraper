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
  },
  data() {
    return {
      layout: [
        { x: 0, y: 0, w: 4, h: 4, i: '0' },
        { x: 4, y: 0, w: 4, h: 4, i: '1' },
        { x: 8, y: 0, w: 4, h: 4, i: '2' },
      ],
    };
  },
};
</script>
