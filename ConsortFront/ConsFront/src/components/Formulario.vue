
<template>
  <Header></Header>
  
  <div class="containerforms">
  <div class="listnotifs">

    <div class="subtitle">CENTRO DE NOTIFICACIONES</div>
    
    <div >
      <button @click="newsubmit" class="buttoncheck">GENERAR NUEVA NOTIFIACACIÓN</button>
    </div>

  </div >
  <form v-if="!submitted" @submit.prevent="handleSubmit" style="background-color: white; margin: 2%; border-radius: 15px; width: 52%  ;" class="max-w-xl mx-auto p-4 bg-white rounded-xl shadow space-y-4">

    <div style="height: 4vh " ></div>

    <div class="fecharecept">
    <label for="received_date" class="input-label">Fecha de recepción</label>
    <input type="date" v-model="form.received_date" id="received_date" class="input-field" />
    <label class="input-label">Hora de recepción</label>
    <input type="time" v-model="form.received_time" class="input-field" />
    </div>


    <div>
      <input type="text" v-model="form.issuing_entity" placeholder="Entidad Emisora" class="entity" />
    </div>
    <br>
    <div>
      <input type="text" v-model="form.case_number"  placeholder="Número Cédula/Expediente" class="entity" />
    </div>
    <br>
    <div>
      <input type="text" v-model="form.recipient" placeholder="Dirigido a" class="entity" />
    </div>
    <br>
    <div class="fecharecept">
      <label for="received_date" class="input-label">Recepcionista</label>
      <select id="receptionist" name="receptionist" class="input-box" v-model="form.receptionist">
        <option disabled value="">Seleccione una opción</option>
        <option value="Amanda González">Amanda González</option>
        <option value="Wanda Pastor">Wanda Pastor</option>
      </select>
    </div>

    <div>
      <select id="collaborators" name="collaborators" class="input-box" v-model="form.internal_collaborator[0]">
        <option disabled value="">Seleccione una opción</option>
        <option value="Amanda González">Amanda </option>
        <option value="Wanda Pastor">Wanda Pastor</option>
      </select> 
    </div>


    <br>
    <div class="button-wrapper">
      <button type="submit" class="guardar">
        <b>Enviar Notificación</b>
      </button>
    </div>

  </form>
</div>
</template>

<script setup>
import Header from './Header.vue'
import { reactive, ref } from 'vue'

const today = new Date();
const date = today.getFullYear() + '-' +
             String(today.getMonth() + 1).padStart(2, '0') + '-' +
             String(today.getDate()).padStart(2, '0');
             const time = String(today.getHours()).padStart(2, '0') + ":" + 
             String(today.getMinutes()).padStart(2, '0');


const submitted = ref(false)

function handleSubmit() {
  console.log('Formulario enviado:', form)
  submitted.value = true
}

function newsubmit() {
  console.log('Formulario creado:', form)
  submitted.value = false
}


const form = reactive({
  received_date: date,
  received_time: time,
  issuing_entity: '',
  case_number: '',
  recipient: '',
  receptionist: 'Amanda González',
  internal_delivery_time: '10:15',
  internal_collaborator: ['Carlos Méndez'],
  final_delivery_datetime: ['2025-04-07T10:30:00']
})



</script>

<style scoped>
.input {
  width: 50%;
}
</style>
