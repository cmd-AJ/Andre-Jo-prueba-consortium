
<template>
  <Header></Header>

  <div class="containerforms">
    <div class="listnotifs">
      <div class="subtitle">CENTRO DE NOTIFICACIONES</div>

      <!-- Button to show form and generate new notification -->
      <button @click="newsubmit" class="buttoncheck">GENERAR NUEVA NOTIFICACIÓN</button>

      <!-- Notifications List -->
      <div v-for="(item, index) in notifications" :key="index" @click="showNotificationDetails(item)"
        style="cursor: pointer; background-color: white; border-top: 3px solid black; border-bottom: 3px solid black;"
        class="notification-box">
        <p><strong>Número de expediente:</strong> {{ item.case_number }}</p>
        <p><strong>Destinatario:</strong> {{ item.recipient }}</p>
      </div>
    </div>

    <!-- Form for new notification, shown when !submitted -->
    <form v-if="!submitted && !activeNotification" @submit.prevent="handleSubmit" 
      style="background-color: white; margin: 2%; border-radius: 15px; width: 52%;" 
      class="max-w-xl mx-auto p-4 bg-white rounded-xl shadow space-y-4">

      <div style="height: 4vh"></div>

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
        <input type="text" v-model="form.case_number" placeholder="Número Cédula/Expediente" class="entity" />
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
        <label for="collaborators" style="margin-left: 4px;">Colaborador interno</label>
        <select id="collaborators" class="input-box" v-model="form.internal_collaborator[0]">
          <option disabled value="">Seleccione una opción</option>
          <option v-for="(user, index) in userlist" :key="index" :value="user.username">
            {{ user.first_name }} {{ user.last_name }}
          </option>
        </select>
      </div>

      <br>
      <div class="button-wrapper">
        <button type="submit" class="guardar">
          <b>Enviar Notificación</b>
        </button>
      </div>
    </form>

    <!-- Display notification details when a notification is selected -->
    <div v-if="activeNotification" style="background: #f9f9f9; padding: 20px; margin: 2%; border-radius: 15px; width: 52%; text-align: center;" class="max-w-xl mx-auto shadow">
      <h2 style="font-weight: bold;">Notificación Seleccionada</h2>
      <p><strong>Fecha:</strong> {{ activeNotification.received_date }}</p>
      <p><strong>Hora:</strong> {{ activeNotification.received_time }}</p>
      <p><strong>Entidad Emisora:</strong> {{ activeNotification.issuing_entity }}</p>
      <p><strong>Número de Expediente:</strong> {{ activeNotification.case_number }}</p>
      <p><strong>Destinatario:</strong> {{ activeNotification.recipient }}</p>
      <p><strong>Recepcionista:</strong> {{ activeNotification.receptionist }}</p>
      <p><strong>Colaborador Interno:</strong> {{ activeNotification.internal_collaborator  }}</p>
    </div>
  </div>
</template>


<script setup>
import Header from './Header.vue'
import { reactive, ref, onMounted } from 'vue'

const userlist = ref([])
const notifications = ref([])

const today = new Date();
const date = today.getFullYear() + '-' +
             String(today.getMonth() + 1).padStart(2, '0') + '-' +
             String(today.getDate()).padStart(2, '0');
const time = String(today.getHours()).padStart(2, '0') + ":" + 
             String(today.getMinutes()).padStart(2, '0');

const submitted = ref(false)
const activeNotification = ref(null); // Active notification when clicked

// Form reactive state
const form = reactive({
  received_date: date,
  received_time: time,
  issuing_entity: '',
  case_number: '',
  recipient: '',
  receptionist: 'Amanda González',
  internal_delivery_time: '10:15',
  internal_collaborator: ['Carlos Méndez'],
  final_delivery_datetime: time
})

// Fetch user data
async function fetchData() {
  try {
    const response = await fetch("http://3.147.6.53:8000/api/users/") // adjust this to your actual endpoint
    if (!response.ok) {
      throw new Error('Error fetching data')
    }

    const data = await response.json()
    userlist.value = data
  } catch (error) {
    console.error("Error fetching data:", error)
  }
}

// Fetch notifications data
async function fetchNotifications() {
  try {
    const response = await fetch('http://3.147.6.53:8000/api/getnotification/') // Change to your endpoint
    if (!response.ok) throw new Error('Failed to fetch notifications')
    const data = await response.json()
    notifications.value = data
  } catch (error) {
    console.error('Fetch error:', error)
  }
}


//sends mail need also database insertion
async function sendmail() {
  try {
    const response = await fetch('http://3.147.6.53:8000/api/sendmail/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form), // Send the form data as the request body
    })
    
    if (!response.ok) throw new Error('Failed to send email')

    const data = await response.json()
    notifications.value = data // Assuming the response contains updated notifications

    console.log('Correo enviado exitosamente:', data)
  } catch (error) {
    console.error('Error al enviar el correo:', error)
  }
}

//sends mail need also database insertion
async function send_to_db() {
  try {
    const response = await fetch('http://3.147.6.53:8000/api/send_notif/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form), // Send the form data as the request body
    })
    
    if (!response.ok) throw new Error('Failed to send email')

    const data = await response.json()
    notifications.value = data // Assuming the response contains updated notifications

    console.log('Correo enviado exitosamente:', data)
  } catch (error) {
    console.error('Error al enviar el correo:', error)
  }
}



// Handle form submission 
async function handleSubmit() {
  console.log('Formulario enviado:', form)
  
  await send_to_db()
  
  await sendmail()

  await fetchNotifications()
  

  // Set submitted to true to show success message
  submitted.value = true
}


// Show selected notification details
function showNotificationDetails(item) {
  activeNotification.value = item
  submitted.value = false; // Hide form when a notification is selected
}

// Reset the form
function newsubmit() {
  console.log('Formulario creado:', form)
  submitted.value = false
  activeNotification.value = null
  form.received_date = date
  form.received_time = time
  form.issuing_entity = ''
  form.case_number = ''
  form.recipient = ''
  form.receptionist = 'Amanda González'
  form.internal_collaborator = ['Carlos Méndez']
  form.final_delivery_datetime = ['2025-04-07T10:30:00']
}

onMounted(() => {
  fetchData()
  fetchNotifications()
})
</script>

<style scoped>
.input {
  width: 50%;
}
</style>