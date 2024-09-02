<template>
  <div id="app">
    <h1 class="text-orange-500 mb-4">Magnífico seja!</h1>
    <p>https://www.youtube.com/watch?v=CCKf6O7asss</p>
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
    <!-- <a v-if="downloadLink" :href="downloadLink" :download="downloadTitle">Clique aqui para baixar o vídeo</a> -->
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { toast } from 'vue3-toastify';

const videoUrl = ref('https://www.youtube.com/watch?v=CCKf6O7asss');
const videoFormat = ref('mp4');
const downloadLink = ref('');
const downloadTitle = ref('');

const downloadVideo = async () => {
  try {
    const videoTitle = await getVideoTitle(videoUrl.value);

    const response = await axios.post('http://127.0.0.1:5000/download', {
      url: videoUrl.value,
      format: videoFormat.value
    }, { responseType: 'blob' });

    const fileURL = window.URL.createObjectURL(new Blob([response.data]));
    const fileLink = document.createElement('a');

    fileLink.href = fileURL;
    fileLink.setAttribute('download', videoTitle + (videoFormat.value === 'mp3' ? '.mp3' : '.mp4'));

    document.body.appendChild(fileLink);
    fileLink.click();
    document.body.removeChild(fileLink);

    toast.success('Download concluído com sucesso!');
  } catch (error) {
    console.error('Erro ao baixar vídeo:', error);
    toast.error('Erro ao baixar vídeo. Tente novamente.');
  }
};

const getVideoTitle = async (url) => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/video-info', {
      params: { url }
    });
    return response.data.title;
  } catch (error) {
    console.error('Erro ao obter título do vídeo:', error);
    toast.error('Erro ao obter título do vídeo. Tente novamente.');
    return 'video';
  }
};
</script>
