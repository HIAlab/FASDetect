<template>
  <q-page class="flex flex-center">

    <q-card flat bordered class="my-card bg-grey-1">
      <q-card-section>
          <div class="text-h6">FASDetect</div>
          <div class="text-subtitle2">Application for Screening Fetal Alcohol Syndrome Spectrum Disorder</div>
      </q-card-section>

      <q-separator inset />

      <q-card-section>
      </q-card-section>

      <div class="q-gutter-sm">
        <q-checkbox v-model="checkbox" label="Ich habe obige Informationen gelesen und verstanden..." />
      </div>
      <q-separator inset/>

      <q-card-actions align="between">
        <q-btn outline color="primary">Einführung</q-btn>
        <q-btn unelevated :disabled="!checkbox" color="primary" icon-right="fas fa-chevron-right" @click="gotoQuestionnaire">Starten</q-btn>
      </q-card-actions>
    </q-card>

  </q-page>
</template>

<style lang="sass">

.q-card
  width: 50%

</style>

<script>
export default {
  name: 'PageIndex',

  data () {
    return {
      checkbox: false
    }
  },

  methods: {

    gotoQuestionnaire () {
      this.$router.push('q')
    }

  }

}
</script>
