<template>
  <div class="card card-body m-4">
    <h3>{{ response.hello }}</h3>
    <h5 class="text-center">{{ counter }} x 2 = {{ times2 }}</h5>
    <button class="btn btn-primary" @click="inc">Increment</button>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapState } from 'vuex'
import axios from 'axios'

export default {
  name: 'HelloWorld',
  data() {
    {
      return { response: "" }
    }
  },

  computed: {
    ...mapState(['counter']),
    ...mapGetters(['times2'])
  },
  methods: {
    ...mapMutations(['setCounter']),
    inc() {
      this.setCounter(this.counter + 1)
    },

    getResponse() {
      axios.get("/api/hello")
        .then((res) => {
          this.response = res.data
        })
        .catch((err) => {
          console.error(err)
        })
    }
  },
  created() {
    this.getResponse();
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
