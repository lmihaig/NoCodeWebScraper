<template>
  <v-dialog transition="dialog-top-transition" max-width="600">
    <template v-slot:activator="{ on, attrs }">
      <v-btn icon elevation="4" v-bind="attrs" v-on="on" @click="showSources">
        <v-icon> mdi-plus-thick </v-icon>
      </v-btn>
    </template>
    <template v-slot:default="dialog">
      <v-card>
        <v-toolbar color="primary" dark>
          Add something
          <v-text-field v-model="name"></v-text-field>
        </v-toolbar>
        <v-card-text>
          <v-list dense nav>
            <v-list-item v-for="(source, index) in sources" :key="index" link @click="addWidget(source); dialog.value = false;">
              <v-list-item-content>
                <v-list-item-title>{{ source.scrapes[0] }}</v-list-item-title>
                <v-list-item-subtitle> {{ source.url }} </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions class="justify-end">
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
      sources: [],
      name: ''
    };
  },
  methods: {
    async addWidget(source) {
      const body = {
        name: this.name,
        source: source.id,
        x: 0,
        y: 0,
        width: 4,
        height: 4
      }
      const response = await fetch('/api/widget', {
        method: 'POST',
        body: JSON.stringify(body),
        headers: {
          'Content-Type': 'application/json'
        }
      });
      this.name = '';
      this.$emit('addWidget');
    },
    async showSources() {
      const data = await fetch('/api/sources').then(respone => respone.json());
      this.sources = data.sources;
      console.log(data)
    }
  },
};
</script>
