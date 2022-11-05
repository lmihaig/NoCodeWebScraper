<template>
  <v-dialog transition="dialog-top-transition" max-width="600">
    <template v-slot:activator="{ on, attrs }">
      <v-btn icon elevation="4" v-bind="attrs" v-on="on">
        <v-icon> mdi-plus-thick </v-icon>
      </v-btn>
    </template>
    <template v-slot:default="dialog">
      <v-card>
        <v-toolbar color="primary" dark>Add something</v-toolbar>
        <v-card-text>
          <div class="text-h2 pa-12">Hello world!</div>
          <v-text-field v-model="input" label="Add something"></v-text-field>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn
            text
            @click="
              addWidget();
              dialog.value = false;
            "
            >Add</v-btn
          >
          <v-btn text @click="dialog.value = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      input: '',
    };
  },
  methods: {
    addWidget() {
      this.$emit('addWidget', this.input);
      this.input = '';
    },
  },
};
</script>
