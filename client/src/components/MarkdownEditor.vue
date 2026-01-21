<template>
  <div class="markdown-editor">
    <div class="editor-toolbar">
      <div class="toolbar-group">
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
      </div>
      
      <div class="toolbar-group">
        <button 
          type="button" 
          @click="togglePreview" 
          :class="{ active: showPreview }"
          title="Предпросмотр"
        >
          <i class="fas fa-eye"></i>
        </button>
      </div>
    </div>
    
    <div class="editor-container">
      <div 
        v-show="!showPreview" 
        class="editor-area"
        :class="{ 'full-width': !splitView }"
      >
        <textarea
          ref="textarea"
          v-model="internalValue"
          :placeholder="placeholder"
          @input="updateContent"
          @keydown.tab.prevent="handleTab"
          class="markdown-textarea"
          :rows="rows"
        ></textarea>
        
        <div class="editor-hints">
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
        :class="{ 'full-width': !splitView }"
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
    
    <div class="editor-mode">
      <button
        v-for="mode in editorModes"
        :key="mode.id"
        :class="{ active: editorMode === mode.id }"
        @click="setEditorMode(mode.id)"
        type="button"
      >
        <i :class="mode.icon"></i>
        {{ mode.label }}
      </button>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'
import DOMPurify from 'dompurify'

export default {
  name: 'MarkdownEditor',
  
  props: {
    value: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: 'Напишите ваш пост используя Markdown...'
    },
    rows: {
      type: Number,
      default: 10
    },
    autoPreview: {
      type: Boolean,
      default: false
    }
  },
  
  data() {
    return {
      internalValue: this.value || '',
      showPreview: this.autoPreview,
      splitView: false,
      editorMode: 'edit',
      editorModes: [
        { id: 'edit', label: 'Редактор', icon: 'fas fa-edit' },
        { id: 'preview', label: 'Просмотр', icon: 'fas fa-eye' },
        { id: 'split', label: 'Раздельно', icon: 'fas fa-columns' }
      ]
    }
  },
  
  computed: {
    renderedHtml() {
      if (!this.internalValue || !this.internalValue.trim()) {
        return '<p class="empty-preview">Текст пока не написан...</p>'
      }
      
      marked.setOptions({
        breaks: true,
        gfm: true,
        highlight: function(code, lang) {
          if (typeof window.hljs === 'undefined') {
            return code
          }
          const hljs = window.hljs
          if (lang && hljs.getLanguage(lang)) {
            return hljs.highlight(code, { language: lang }).value
          }
          return hljs.highlightAuto(code).value
        }
      })
      
      try {
        const html = marked(this.internalValue)
        return DOMPurify.sanitize(html)
      } catch (error) {
        console.error('Error rendering markdown:', error)
        return '<p class="error">Ошибка при обработке Markdown</p>'
      }
    }
  },
  
  watch: {
    value(newVal) {
        const newValStr = String(newVal || '')
    if (newValStr !== this.internalValue) {
        this.internalValue = newValStr
    }
    },
        
    internalValue(newVal) {
        this.$emit('update:model-value', newVal)
        this.$emit('change', newVal)
    }
  },
  
  methods: {
    setEditorMode(mode) {
      this.editorMode = mode
      if (mode === 'edit') {
        this.showPreview = false
        this.splitView = false
      } else if (mode === 'preview') {
        this.showPreview = true
        this.splitView = false
      } else if (mode === 'split') {
        this.showPreview = false
        this.splitView = true
      }
    },
    
    
    togglePreview() {
      this.showPreview = !this.showPreview
      if (this.showPreview) {
        this.editorMode = 'preview'
      } else {
        this.editorMode = 'edit'
      }
    },
    
    handleTab(event) {
      const textarea = event.target
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      
      const spaces = '  '

      const newValue = this.internalValue.substring(0, start) + spaces + this.internalValue.substring(end)
      
      this.internalValue = newValue
      
      this.$nextTick(() => {
        textarea.selectionStart = textarea.selectionEnd = start + spaces.length
      })
    },
    
    formatText(type) {
      const textarea = this.$refs.textarea
      if (!textarea) return
      
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      const selectedText = this.internalValue.substring(start, end)
      
      let formattedText = ''
      let newCursorPos = start
      
      switch(type) {
        case 'bold':
          formattedText = `**${selectedText}**`
          newCursorPos = start + 2
          break
        case 'italic':
          formattedText = `*${selectedText}*`
          newCursorPos = start + 1
          break
        case 'header':
          formattedText = `# ${selectedText}`
          newCursorPos = start + 2
          break
        case 'link':
          formattedText = `[${selectedText || 'текст ссылки'}](https://example.com)`
          newCursorPos = start + 1
          break
        case 'image':
          formattedText = `![${selectedText || 'alt текст'}](${selectedText || 'https://example.com/image.jpg'})`
          newCursorPos = start + 2
          break
        case 'list-ul':
          formattedText = selectedText ? `- ${selectedText.replace(/\n/g, '\n- ')}` : '- '
          break
        case 'list-ol':
          formattedText = selectedText ? `1. ${selectedText.replace(/\n/g, '\n1. ')}` : '1. '
          break
        case 'code':
          if (selectedText.includes('\n')) {
            formattedText = '```\n' + selectedText + '\n```'
            newCursorPos = start + 4
          } else {
            formattedText = `\`${selectedText}\``
            newCursorPos = start + 1
          }
          break
        case 'quote':
          formattedText = selectedText ? `> ${selectedText.replace(/\n/g, '\n> ')}` : '> '
          break
      }
      
      this.internalValue = this.internalValue.substring(0, start) + formattedText + this.internalValue.substring(end)
      
      this.$nextTick(() => {
        textarea.focus()
        if (selectedText) {
          textarea.selectionStart = newCursorPos
          textarea.selectionEnd = newCursorPos + selectedText.length
        } else {
          textarea.selectionStart = textarea.selectionEnd = newCursorPos
        }
      })
    },
    
    insertImage(url, alt = '') {
      const textarea = this.$refs.textarea
      const start = textarea.selectionStart
      const markdownImage = `![${alt}](${url})`
      
      this.internalValue = this.internalValue.substring(0, start) + markdownImage + this.internalValue.substring(start)
      
      this.$nextTick(() => {
        textarea.focus()
        textarea.selectionStart = textarea.selectionEnd = start + markdownImage.length
      })
    },
    
    focus() {
      this.$refs.textarea?.focus()
    }
  },
  
  mounted() {
    this.internalValue = String(this.value || '')
  }
}
</script>

<style scoped>
.markdown-editor {
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  background: var(--dark-light);
  overflow: hidden;
}

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
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
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

.markdown-textarea {
  width: 100%;
  height: 100%;
  min-height: 250px;
  background: transparent;
  border: none;
  color: var(--text);
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
  resize: vertical;
  outline: none;
}

.markdown-textarea::placeholder {
  color: var(--text-secondary);
  opacity: 0.7;
}

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

.editor-hints {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 0.8em;
  color: var(--text-secondary);
  padding: 10px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.editor-hints span {
  padding: 2px 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

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

.editor-mode {
  display: flex;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(0, 0, 0, 0.1);
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

@media (max-width: 768px) {
  .editor-toolbar {
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .editor-mode {
    flex-direction: column;
  }
}
</style>