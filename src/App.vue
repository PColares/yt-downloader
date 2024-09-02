<template>
  <div id="app">
    <h1 class="text-orange-500 mb-4">Magnífico seja!</h1>
    <p>https://www.youtube.com/watch?v=_RtbGoaeJUQ</p>
    <h1>BaixaTube</h1>
    <form @submit.prevent="downloadVideo" class="flex flex-col justify-center items-center gap-4 mt-12">
      <div class="flex gap-4">
        <input v-model="videoUrl" type="text" placeholder="Insira um link do youtube" class="h-10 rounded-md px-4"/>
        <select v-model="videoFormat" class="rounded-md pl-4 px-4">
          <option value="mp4">.mp4</option>
          <option value="mp3">.mp3</option>
        </select>
      </div>
      <button type="submit">Baixar</button>
    </form>
    <a v-if="downloadLink" :href="downloadLink" :download="downloadTitle">Clique aqui para baixar o vídeo</a>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { toast } from 'vue3-toastify';

const videoUrl = ref('');
const videoFormat = ref('mp4');
const downloadLink = ref('');
const downloadTitle = ref('');

const downloadVideo = async () => {
  try {
    const response = await axios.post('http://localhost:5000/download', {
      url: videoUrl.value,
      format: videoFormat.value
    });

    if (response.data.download_url) {
      downloadLink.value = response.data.download_url;
      downloadTitle.value = response.data.title + (videoFormat.value === 'mp3' ? '.mp3' : '.mp4');
      toast.success('Download concluído com sucesso!');
    }
  } catch (error) {
    console.error('Erro ao baixar vídeo:', error);
    toast.error('Erro ao baixar vídeo. Tente novamente.');
  }
};
</script>
