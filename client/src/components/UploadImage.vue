<template>
  <div class="image-upload">
    <input
      type="file"
      ref="fileInput"
      @change="handleFileSelect"
      accept="image/*"
      style="display: none"
    />
    
    <button 
      type="button" 
      class="btn btn-outline"
      @click="$refs.fileInput.click()"
    >
      <i class="fas fa-upload"></i>
      Загрузить изображение
    </button>
    
    <div v-if="uploading" class="upload-progress">
      <div class="progress-bar">
        <div 
          class="progress-fill" 
          :style="{ width: uploadProgress + '%' }"
        ></div>
      </div>
      <span>{{ uploadProgress }}%</span>
    </div>
    
    <div v-if="error" class="upload-error">
      {{ error }}
    </div>
  </div>
</template>

<script>
export default {
    props: {
        endpoint: {
            type: String,
            default: '/api/upload'
        }
    },

    data() {
        return {
            uploading: false,
            uploadProgress: 0,
            error: null
        }
    },

    methods: {
        async handleFileSelect(event) {
            const file = event.target.files[0]
            if (!file) return

            if (!file.type.startWith('image/')) {
                this.error = 'Пожалйуста, выберите файл изображения'
                return
            }

            if (file.size > 5 * 1024 * 1024) {
                this.error = 'Файл слишком большой (макс. 5MB)'
                return
            }

            await this.uploadFile(file)
        },

        async uploadFile(file) {
            this.uploading = true
            this.error = null
            this.uploadProgress = 0

            const formData = new FormData()
            formData.append('image', file)

            try {
                const token = localStorage.getItem('authToken')
                const response = await fetch(this.endpoint, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    body: formData
                })

                if (!response.ok) {
                    throw new Error('Ошибка загрузки')
                }

                const data = await response.json()
                this.$emit('uploaded', data.url)
            } catch (error) {
                this.error = 'Не удалось загрузить изображение'
            } finally {
                this.uploading = false
                this.uploadProgress = 100
            }
        }
    }
}
</script>