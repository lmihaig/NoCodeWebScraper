<template>
  <div>
    <canvas :id="'myChart' + index"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';
export default {
  props: {
    config: {
      type: Object,
    },
    index: {
      type: Number,
    },
  },
  mounted() {
    new Chart(document.getElementById('myChart' + this.index), this.config);
  },
};
</script>
