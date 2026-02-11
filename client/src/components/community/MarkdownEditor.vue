<template>
  <div class="markdown-editor">
    <div class="mobile-toolbar-overlay" v-if="showMobileToolbar" @click="showMobileToolbar = false">
      <div class="mobile-toolbar" @click.stop>
        <div class="mobile-toolbar-header">
          <h3>Форматирование</h3>
          <button @click="showMobileToolbar = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="mobile-toolbar-grid">
          <button type="button" @click="formatText('bold')" title="Жирный">
            <i class="fas fa-bold"></i>
            <span>Жирный</span>
          </button>
          <button type="button" @click="formatText('italic')" title="Курсив">
            <i class="fas fa-italic"></i>
            <span>Курсив</span>
          </button>
          <button type="button" @click="formatText('header')" title="Заголовок">
            <i class="fas fa-heading"></i>
            <span>Заголовок</span>
          </button>
          <button type="button" @click="formatText('link')" title="Ссылка">
            <i class="fas fa-link"></i>
            <span>Ссылка</span>
          </button>
          <button type="button" @click="formatText('image')" title="Изображение">
            <i class="fas fa-image"></i>
            <span>Изображение</span>
          </button>
          <button type="button" @click="formatText('list-ul')" title="Список">
            <i class="fas fa-list-ul"></i>
            <span>Список</span>
          </button>
          <button type="button" @click="formatText('code')" title="Код">
            <i class="fas fa-code"></i>
            <span>Код</span>
          </button>
          <button type="button" @click="formatText('quote')" title="Цитата">
            <i class="fas fa-quote-right"></i>
            <span>Цитата</span>
          </button>
        </div>
      </div>
    </div>

    <div class="editor-toolbar">
      <div class="toolbar-group left-group">
        <!-- Мобильная кнопка меню -->
        <button 
          type="button" 
          class="mobile-menu-btn"
          @click="showMobileToolbar = true"
          title="Меню форматирования"
          v-if="isMobile"
        >
          <i class="fas fa-bars"></i>
          <span>Формат</span>
        </button>

        <template v-if="!isMobile">
          <button type="button" @click="formatText('bold')" title="Жирный">
            <i class="fas fa-bold"></i>
          </button>
          <button type="button" @click="formatText('italic')" title="Курсив">
            <i class="fas fa-italic"></i>
          </button>
          <button type="button" @click="formatText('header')" title="Заголовок">
            <i class="fas fa-heading"></i>
          </button>
          <div class="divider"></div>
          <button type="button" @click="formatText('link')" title="Ссылка">
            <i class="fas fa-link"></i>
          </button>
          <button type="button" @click="formatText('image')" title="Изображение">
            <i class="fas fa-image"></i>
          </button>
          <div class="divider"></div>
          <button type="button" @click="formatText('list-ul')" title="Маркированный список">
            <i class="fas fa-list-ul"></i>
          </button>
          <button type="button" @click="formatText('list-ol')" title="Нумерованный список">
            <i class="fas fa-list-ol"></i>
          </button>
          <button type="button" @click="formatText('code')" title="Код">
            <i class="fas fa-code"></i>
          </button>
          <button type="button" @click="formatText('quote')" title="Цитата">
            <i class="fas fa-quote-right"></i>
          </button>
        </template>
        
        <button 
          type="button" 
          class="keyboard-toggle"
          @click="toggleKeyboard"
          title="Скрыть клавиатуру"
          v-if="isMobile"
        >
          <i class="fas fa-keyboard"></i>
        </button>
      </div>
      
      <div class="toolbar-group">
        <button 
          type="button" 
          @click="togglePreview" 
          :class="{ active: showPreview }"
          title="Предпросмотр"
        >
          <i class="fas fa-eye"></i>
          <span v-if="!isMobile"></span>
        </button>
      </div>
    </div>
    
    <div class="editor-container">
      <div 
        v-show="!showPreview" 
        class="editor-area"
        :class="{ 'full-width': !splitView, 'mobile-editor': isMobile }"
      >
        <textarea
          ref="textarea"
          v-model="internalValue"
          :placeholder="placeholder"
          @input="updateContent"
          @keydown.tab.prevent="handleTab"
          @focus="onTextareaFocus"
          @blur="onTextareaBlur"
          class="markdown-textarea"
          :rows="mobileRows"
          :style="{ 'font-size': mobileFontSize }"
        ></textarea>
        
        <div class="editor-hints" :class="{ 'mobile-hints': isMobile }">
          <span><strong>Markdown подсказки:</strong></span>
          <span>**жирный**</span>
          <span>*курсив*</span>
          <span># Заголовок</span>
          <span>- список</span>
          <span>`код`</span>
          <span>[ссылка](url)</span>
        </div>
      </div>
      
      <div 
        v-show="showPreview" 
        class="preview-area"
        :class="{ 'full-width': !splitView, 'mobile-preview': isMobile }"
      >
        <div 
          class="markdown-preview"
          v-html="renderedHtml"
        ></div>
      </div>
      
      <div v-if="splitView && !showPreview" class="split-preview">
        <div class="split-divider"></div>
        <div class="preview-area split">
          <div 
            class="markdown-preview"
            v-html="renderedHtml"
          ></div>
        </div>
      </div>
    </div>
    
    <div class="editor-mode" :class="{ 'mobile-mode': isMobile }">
      <button
        v-for="mode in editorModes"
        :key="mode.id"
        :class="{ active: editorMode === mode.id }"
        @click="setEditorMode(mode.id)"
        type="button"
      >
        <i :class="mode.icon"></i>
        <span v-if="!isMobile">{{ mode.label }}</span>
      </button>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked';
import DOMPurify from 'dompurify';

export default {
  name: 'MarkdownEditor',
  
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: 'Начните вводить текст...'
    },
    rows: {
      type: Number,
      default: 10
    }
  },
  
  emits: ['update:modelValue'],
  
  data() {
    return {
      internalValue: this.modelValue,
      showPreview: false,
      splitView: false,
      editorMode: 'edit',
      showMobileToolbar: false,
      showContextMenu: false,
      isMobile: false,
      mobileRows: this.rows,
      mobileFontSize: '16px',
      
      editorModes: [
        { id: 'edit', label: 'Редактирование', icon: 'fas fa-edit' },
        { id: 'split', label: 'Раздельно', icon: 'fas fa-columns' },
        { id: 'preview', label: 'Просмотр', icon: 'fas fa-eye' }
      ]
    };
  },
  
  computed: {
    renderedHtml() {
      if (!this.internalValue.trim()) {
        return '<div class="empty-preview">Текст будет отображен здесь...</div>';
      }
      
      try {
        const html = marked(this.internalValue, {
          breaks: true,
          gfm: true
        });
        
        return DOMPurify.sanitize(html);
      } catch (error) {
        console.error('Ошибка рендеринга Markdown:', error);
        return '<div class="error-preview">Ошибка форматирования текста</div>';
      }
    }
  },
  
  watch: {
    modelValue(newVal) {
      if (newVal !== this.internalValue) {
        this.internalValue = newVal;
      }
    },
    
    internalValue(newVal) {
      this.$emit('update:modelValue', newVal);
    }
  },
  
  mounted() {
    this.checkMobile();
    window.addEventListener('resize', this.checkMobile);
    
    // Настройка marked
    marked.setOptions({
      breaks: true,
      gfm: true,
      headerIds: false
    });
  },
  
  beforeUnmount() {
    window.removeEventListener('resize', this.checkMobile);
  },
  
  methods: {
    updateContent() {
      this.$emit('update:modelValue', this.internalValue);
    },
    
    formatText(type) {
      const textarea = this.$refs.textarea;
      if (!textarea) return;
      
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const selectedText = this.internalValue.substring(start, end);
      
      let formattedText = '';
      let cursorOffset = 0;
      
      switch(type) {
        case 'bold':
          formattedText = `**${selectedText}**`;
          cursorOffset = 2;
          break;
        case 'italic':
          formattedText = `*${selectedText}*`;
          cursorOffset = 1;
          break;
        case 'header':
          formattedText = `# ${selectedText}`;
          cursorOffset = 2;
          break;
        case 'link':
          formattedText = `[${selectedText}](https://example.com)`;
          cursorOffset = selectedText.length + 3;
          break;
        case 'image':
          formattedText = `![${selectedText}](https://example.com/image.jpg)`;
          cursorOffset = selectedText.length + 4;
          break;
        case 'list-ul':
          formattedText = selectedText.split('\n').map(line => `- ${line}`).join('\n');
          break;
        case 'list-ol':
          formattedText = selectedText.split('\n').map((line, i) => `${i + 1}. ${line}`).join('\n');
          break;
        case 'code':
          formattedText = selectedText.includes('\n') 
            ? `\`\`\`\n${selectedText}\n\`\`\`` 
            : `\`${selectedText}\``;
          cursorOffset = selectedText.includes('\n') ? 4 : 1;
          break;
        case 'quote':
          formattedText = selectedText.split('\n').map(line => `> ${line}`).join('\n');
          break;
      }
      
      const newValue = this.internalValue.substring(0, start) + 
                       formattedText + 
                       this.internalValue.substring(end);
      
      this.internalValue = newValue;
      
      // Восстанавливаем позицию курсора
      this.$nextTick(() => {
        textarea.focus();
        const newCursorPos = start + (selectedText ? formattedText.length : cursorOffset);
        textarea.setSelectionRange(newCursorPos, newCursorPos);
      });
      
      this.showMobileToolbar = false;
    },
    
    handleTab(event) {
      event.preventDefault();
      const textarea = this.$refs.textarea;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      
      const newValue = this.internalValue.substring(0, start) + 
                       '    ' + 
                       this.internalValue.substring(end);
      
      this.internalValue = newValue;
      
      this.$nextTick(() => {
        textarea.focus();
        const newCursorPos = start + 4;
        textarea.setSelectionRange(newCursorPos, newCursorPos);
      });
    },
    
    togglePreview() {
      this.showPreview = !this.showPreview;
    },
    
    setEditorMode(mode) {
      this.editorMode = mode;
      
      switch(mode) {
        case 'edit':
          this.showPreview = false;
          this.splitView = false;
          break;
        case 'split':
          this.showPreview = false;
          this.splitView = true;
          break;
        case 'preview':
          this.showPreview = true;
          this.splitView = false;
          break;
      }
    },
    
    checkMobile() {
      this.isMobile = window.innerWidth <= 768;
      this.mobileRows = this.isMobile ? 6 : this.rows;
      this.mobileFontSize = this.isMobile ? '16px' : '14px';
    },
    
    toggleKeyboard() {
      const textarea = this.$refs.textarea;
      textarea.blur();
    },
    
    onTextareaFocus() {
      if (this.isMobile) {
        setTimeout(() => {
          this.showContextMenu = true;
        }, 300);
      }
    },
    
    onTextareaBlur() {
      if (this.isMobile) {
        setTimeout(() => {
          this.showContextMenu = false;
        }, 200);
      }
    },
    
    copySelectedText() {
      const textarea = this.$refs.textarea;
      const selectedText = this.internalValue.substring(
        textarea.selectionStart,
        textarea.selectionEnd
      );
      
      if (selectedText) {
        navigator.clipboard.writeText(selectedText)
          .then(() => {
            console.log('Текст скопирован');
          })
          .catch(err => {
            console.error('Ошибка копирования:', err);
          });
      }
    },
    
    cutSelectedText() {
      const textarea = this.$refs.textarea;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const selectedText = this.internalValue.substring(start, end);
      
      if (selectedText) {
        navigator.clipboard.writeText(selectedText)
          .then(() => {
            const newValue = this.internalValue.substring(0, start) + 
                           this.internalValue.substring(end);
            this.internalValue = newValue;
            
            this.$nextTick(() => {
              textarea.focus();
              textarea.setSelectionRange(start, start);
            });
          })
          .catch(err => {
            console.error('Ошибка вырезания:', err);
          });
      }
    },
    
    async pasteText() {
      try {
        const text = await navigator.clipboard.readText();
        const textarea = this.$refs.textarea;
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        
        const newValue = this.internalValue.substring(0, start) + 
                         text + 
                         this.internalValue.substring(end);
        
        this.internalValue = newValue;
        
        this.$nextTick(() => {
          textarea.focus();
          const newCursorPos = start + text.length;
          textarea.setSelectionRange(newCursorPos, newCursorPos);
        });
      } catch (err) {
        console.error('Ошибка вставки:', err);
      }
    },
    
    selectAllText() {
      const textarea = this.$refs.textarea;
      textarea.focus();
      textarea.setSelectionRange(0, this.internalValue.length);
    }
  }
};
</script>

<style scoped>
.markdown-editor {
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  background: var(--dark-light);
  overflow: hidden;
}

/* Мобильное меню форматирования */
.mobile-toolbar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.mobile-toolbar {
  background: var(--dark-light);
  border-radius: 20px;
  width: 100%;
  max-width: 400px;
  max-height: 80vh;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
}

.mobile-toolbar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.mobile-toolbar-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.mobile-toolbar-header button {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 1.2rem;
  cursor: pointer;
}

.mobile-toolbar-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  padding: 20px;
}

.mobile-toolbar-grid button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 20px 15px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.mobile-toolbar-grid button:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text);
  border-color: var(--primary);
}

.mobile-toolbar-grid button i {
  font-size: 1.5rem;
}

.mobile-toolbar-grid button span {
  font-size: 0.9rem;
}

/* Основной тулбар */
.editor-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background: rgba(0, 0, 0, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.toolbar-group {
  display: flex;
  align-items: center;
  gap: 5px;
}

.editor-toolbar button {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 5px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.editor-toolbar button:not(.mobile-menu-btn):not(.keyboard-toggle) {
  width: 36px;
  height: 36px;
}

.mobile-menu-btn {
  padding: 8px 15px;
  height: 36px;
  gap: 8px;
}

.keyboard-toggle {
  width: 36px;
  height: 36px;
}

.editor-toolbar button:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text);
  border-color: var(--primary);
}

.editor-toolbar button.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}

.editor-toolbar .divider {
  width: 1px;
  height: 24px;
  background: rgba(255, 255, 255, 0.1);
  margin: 0 5px;
}

/* Контейнер редактора */
.editor-container {
  position: relative;
  display: flex;
  min-height: 300px;
}

.editor-area,
.preview-area {
  flex: 1;
  padding: 15px;
}

.editor-area.full-width,
.preview-area.full-width {
  width: 100%;
}

.editor-area.mobile-editor {
  padding: 10px;
}

/* Текстовое поле */
.markdown-textarea {
  width: 100%;
  height: 460px;
  min-height: 250px;
  background: transparent;
  border: none;
  color: var(--text);
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  line-height: 1.6;
  resize: vertical;
  outline: none;
}

.markdown-textarea::placeholder {
  color: var(--text-secondary);
  opacity: 0.7;
}

/* Предпросмотр */
.markdown-preview {
  height: 100%;
  overflow-y: auto;
  line-height: 1.7;
  color: var(--text);
}

.markdown-preview >>> * {
  margin-top: 0;
  margin-bottom: 1em;
}

.markdown-preview >>> h1,
.markdown-preview >>> h2,
.markdown-preview >>> h3,
.markdown-preview >>> h4 {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  color: var(--text);
  font-weight: 600;
}

.markdown-preview >>> h1 { font-size: 1.8em; border-bottom: 2px solid var(--primary); padding-bottom: 0.3em; }
.markdown-preview >>> h2 { font-size: 1.5em; }
.markdown-preview >>> h3 { font-size: 1.3em; }
.markdown-preview >>> h4 { font-size: 1.1em; }

.markdown-preview >>> strong { color: var(--text); font-weight: 700; }
.markdown-preview >>> em { color: var(--text); font-style: italic; }

.markdown-preview >>> ul,
.markdown-preview >>> ol {
  padding-left: 2em;
  margin-bottom: 1em;
}

.markdown-preview >>> blockquote {
  border-left: 4px solid var(--primary);
  padding-left: 1em;
  margin-left: 0;
  color: var(--text-secondary);
  background: rgba(255, 69, 0, 0.05);
  border-radius: 0 5px 5px 0;
}

.markdown-preview >>> code {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 0.9em;
  color: var(--accent);
}

.markdown-preview >>> pre {
  background: rgba(0, 0, 0, 0.3);
  padding: 1em;
  border-radius: 5px;
  overflow-x: auto;
  margin-bottom: 1em;
}

.markdown-preview >>> pre code {
  background: none;
  padding: 0;
  color: inherit;
}

.markdown-preview >>> a {
  color: var(--accent);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
}

.markdown-preview >>> a:hover {
  border-bottom-color: var(--accent);
}

.markdown-preview >>> img {
  max-width: 100%;
  height: auto;
  border-radius: 5px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.markdown-preview >>> table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1em;
}

.markdown-preview >>> th,
.markdown-preview >>> td {
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0.5em 1em;
  text-align: left;
}

.markdown-preview >>> th {
  background: rgba(255, 255, 255, 0.05);
  font-weight: 600;
}

.markdown-preview >>> hr {
  border: none;
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 2em 0;
}

.empty-preview {
  color: var(--text-secondary);
  font-style: italic;
  text-align: center;
  padding: 3em;
  opacity: 0.7;
}

/* Подсказки */
.editor-hints {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 0.8em;
  color: var(--text-secondary);
  padding: 10px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.editor-hints.mobile-hints {
  display: none; /* Скрываем на мобильных для экономии места */
}

.editor-hints span {
  padding: 2px 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

/* Раздельный режим */
.split-preview {
  display: flex;
  width: 100%;
}

.split-divider {
  width: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 0 10px;
}

.preview-area.split {
  flex: 1;
  border-left: 1px solid rgba(255, 255, 255, 0.1);
}

/* Режимы редактора */
.editor-mode {
  display: flex;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(0, 0, 0, 0.1);
}

.editor-mode.mobile-mode button {
  flex-direction: column;
  gap: 5px;
  font-size: 0.8rem;
}

.editor-mode button {
  flex: 1;
  padding: 10px;
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.editor-mode button:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text);
}

.editor-mode button.active {
  background: var(--primary);
  color: white;
}

/* Адаптивность */
@media (max-width: 768px) {
  .editor-toolbar .left-group > button:not(.mobile-menu-btn):not(.keyboard-toggle) {
    display: none;
  }
  
  .editor-toolbar .divider {
    display: none;
  }
  
  .editor-container {
    min-height: 200px;
  }
  
  .editor-area, .preview-area {
    padding: 10px;
  }
  
  .markdown-textarea {
    font-size: 16px !important;
    min-height: 200px;
  }
  
  .editor-hints {
    display: none;
  }
  
  .split-preview {
    display: none;
  }
  
  .preview-area.mobile-preview {
    padding: 15px;
  }
  
  .editor-mode {
    flex-wrap: wrap;
  }
  
  .editor-mode button {
    min-width: 33.33%;
    padding: 12px 5px;
  }
}

@media (max-width: 480px) {
  .mobile-toolbar-grid {
    grid-template-columns: 1fr;
  }
  
  .editor-mode button {
    min-width: 50%;
    font-size: 0.75rem;
  }
}

/* Предотвращение zoom на iOS */
@media (max-device-width: 768px) {
  .markdown-textarea {
    font-size: 16px !important;
  }
  
  input, select, textarea {
    font-size: 16px !important;
  }
}
</style>