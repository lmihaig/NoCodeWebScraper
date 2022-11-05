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
      </smart-widget>
    </smart-widget-grid>
  </div>
</template>

<script>
export default {
  name: 'GridWidget',
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
