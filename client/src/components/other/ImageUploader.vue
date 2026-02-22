<template>
  <div class="image-uploader">
    <input 
      type="file" 
      multiple 
      accept="image/*"
      @change="handleFileUpload"
      ref="fileInput"
    >
    <div v-if="isCompressing" class="compressing">
      Сжатие изображений... {{ compressionProgress }}%
    </div>
    <div class="preview-images">
      <div v-for="(image, index) in compressedImages" :key="index" class="preview-item">
        <img :src="image.preview" :alt="image.name">
        <span class="file-size">{{ formatSize(image.size) }}</span>
        <button @click="removeImage(index)">×</button>
      </div>
    </div>
  </div>
</template>

<script>
import imageCompression from 'browser-image-compression';

export default {
    name: 'ImageUploader',
    props: {
        maxImages: {
            type: Number,
            default: 5
        },
        maxSizeMB: {
            type: Number,
            default: 5
        },
        maxWifthOrHeight: {
            type: Number,
            default: 1200
        }
    },
    data() {
        return {
            compressedImages: [],
            isCompressing: false,
            compressionProgress: 0
        };
    },
    methods: {
        async handleFileUpload(event) {
            const files = Array.from(event.target.files);

            if (this.compressedImages.length + files.length > this.maxImages) {
                alert(`Можно загрузить не более ${this.maxImages} изображений`);
                return;
            }

            this.isCompressing = true;

            for (const file of files) {
                try {
                    const options = {
                        maxSizeMB: this.maxSizeMB,
                        maxWifthOrHeight: this.maxWifthOrHeight,
                        useWebWorker: true,
                        onProgress: (progress) => {
                            this.compressionProgress = Math.round(progress);
                        },
                        fileType: file.type,
                        initialQuality: 0.85
                    };

                    const compressedFile = await imageCompression(file, options);

                    const preview = await imageCompression.getDataUrlFromFile(compressedFile);

                    this.compressedImages.push({
                        file: compressedFile,
                        preview: preview,
                        name: compressedFile.name,
                        size: compressedFile.size,
                        originalSize: file.size
                    });
                } catch (error) {
                    console.error('Ошибка при сжатии: ', error);
                    const preview = await imageCompression.getDataUrlFromFile(file);
                    this.compressedImages.push({
                        file: file,
                        preview: preview,
                        name: file.name,
                        size: file.size
                    });
                }
            }

            this.isCompressing = false;
            this.compressionProgress = 0;
            this.$refs.fileInput.value = '';

            this.$emit('images-updated', this.compressedImages.map(img => img.file));
        },

        removeImage(index) {
            this.compressedImages.splice(index, 1);
            this.$emit('images-updated', this.compressedImages.map(img => img.file));
        },

        formatSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        },

        getFormData() {
            const formData = new FormData();
            this.compressedImages.forEach((img, index) => {
                formData.append('images', img.file)
            });
            return formData;
        },

        clear() {
            this.compressedImages = [];
        }
    }
};
</script>

<style scoped>
.image-uploader {
  width: 100%;
}

.preview-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
  margin-top: 10px;
}

.preview-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.1);
}

.preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-item .file-size {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0,0,0,0.7);
  color: white;
  font-size: 10px;
  padding: 2px 4px;
  text-align: center;
}

.preview-item button {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(255,0,0,0.7);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.compressing {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: var(--dark-light);
  padding: 20px;
  border-radius: 10px;
  z-index: 1000;
}
</style>