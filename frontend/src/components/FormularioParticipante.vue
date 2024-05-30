<template>
  <div>
    <form @submit.prevent="submitForm">
      <input v-model="nombre" placeholder="Nombre" required />
      <input v-model="edad" type="number" placeholder="Edad" required />
      <input v-model="nacionalidad" placeholder="Nacionalidad" required />
      <input v-model="genero" placeholder="Género" required />
      <button type="submit">Participa</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const nombre = ref('');
const edad = ref(0);
const nacionalidad = ref('');
const genero = ref('');

const submitForm = async () => {
  const participante = {
    Nombre: nombre.value, // Usar mayúscula para coincidir con el backend
    Edad: edad.value,
    Nacionalidad: nacionalidad.value,
    Genero: genero.value,
  };

  try {
    const response = await axios.post('http://127.0.0.1:5000/participantes', participante, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    console.log('Participante creado:', response.data);
  } catch (error) {
    console.error('Error:', error);
  }
};
</script>

<style scoped>
div {
  margin: 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
  text-decoration: none;
}
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background-color: ;
}
</style>
