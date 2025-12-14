[file name]: Market.vue
<template>
    <!-- Декоративные элементы -->
    <div class="decoration decoration-1"></div>
    <div class="decoration decoration-2"></div>

    <!-- Страница маркета -->
    <section class="market">
        <!-- Заголовок и фильтры -->
        <div class="market-header">
            <div class="header-content">
                <h1 class="market-title">
                    <i class="fas fa-shopping-cart"></i>
                    <span>Маркет запчастей</span>
                </h1>
                <p class="market-subtitle">Площадка для покупки и продажи мотоциклов, запчастей и экипировки</p>
                
                <div class="market-stats">
                    <div class="stat-item">
                        <div class="stat-value">{{ activeListings }}</div>
                        <div class="stat-label">Активных объявлений</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{{ userActiveListings }}</div>
                        <div class="stat-label">Ваших <br> активных объявлений</div>
                    </div>
                </div>
            </div>
            
            <div class="market-actions">
                <button class="btn btn-primary" @click="showNewAdModal">
                    <i class="fas fa-plus"></i> Разместить объявление
                </button>
                <div class="search-box">
                    <i class="fas fa-search"></i>
                    <input 
                        type="text" 
                        placeholder="Поиск по маркету..." 
                        v-model="searchQuery"
                        @input="handleSearch"
                    >
                </div>
            </div>
        </div>

        <!-- Фильтры и категории -->
        <div class="market-filters">
            <div class="filter-tabs">
                <button 
                    class="filter-tab" 
                    :class="{ active: activeFilter === 'all' }"
                    @click="setFilter('all')"
                >
                    Все
                </button>
                <button 
                    class="filter-tab" 
                    :class="{ active: activeFilter === 'motorcycles' }"
                    @click="setFilter('motorcycles')"
                >
                    Мотоциклы
                </button>
                <button 
                    class="filter-tab" 
                    :class="{ active: activeFilter === 'parts' }"
                    @click="setFilter('parts')"
                >
                    Запчасти
                </button>
                <button 
                    class="filter-tab" 
                    :class="{ active: activeFilter === 'gear' }"
                    @click="setFilter('gear')"
                >
                    Экипировка
                </button>
                <button 
                    class="filter-tab" 
                    :class="{ active: activeFilter === 'my' && user }"
                    @click="setFilter('my')"
                    v-if="user"
                >
                    Мои объявления
                </button>
            </div>
            
            <div class="filter-sort">
                <select v-model="sortBy" @change="handleSort">
                    <option value="newest">Сначала новые</option>
                    <option value="price_low">Цена (низкая → высокая)</option>
                    <option value="price_high">Цена (высокая → низкая)</option>
                    <option value="popular">Популярные</option>
                </select>
                <div class="filter-tags">
                    <span class="tag" v-for="tag in activeTags" :key="tag">
                        {{ tag }} <i class="fas fa-times" @click="removeTag(tag)"></i>
                    </span>
                </div>
            </div>
        </div>

        <!-- Основной контент -->
        <div class="market-content">
            <!-- Боковая панель с категориями -->
            <div class="sidebar">
                <div class="sidebar-section">
                    <h3><i class="fas fa-filter"></i> Категории</h3>
                    <div class="category-list">
                        <label class="category-item">
                            <input type="checkbox" v-model="categories.motorcycles">
                            <span>Мотоциклы</span>
                            <span class="count">42</span>
                        </label>
                        <label class="category-item">
                            <input type="checkbox" v-model="categories.engines">
                            <span>Двигатели</span>
                            <span class="count">156</span>
                        </label>
                        <label class="category-item">
                            <input type="checkbox" v-model="categories.frames">
                            <span>Рамы и подвеска</span>
                            <span class="count">89</span>
                        </label>
                        <label class="category-item">
                            <input type="checkbox" v-model="categories.electronics">
                            <span>Электроника</span>
                            <span class="count">67</span>
                        </label>
                        <label class="category-item">
                            <input type="checkbox" v-model="categories.helmets">
                            <span>Шлемы</span>
                            <span class="count">124</span>
                        </label>
                        <label class="category-item">
                            <input type="checkbox" v-model="categories.clothing">
                            <span>Одежда</span>
                            <span class="count">87</span>
                        </label>
                        <label class="category-item">
                            <input type="checkbox" v-model="categories.accessories">
                            <span>Аксессуары</span>
                            <span class="count">203</span>
                        </label>
                    </div>
                </div>
                
                <div class="sidebar-section">
                    <h3><i class="fas fa-tags"></i> Популярные теги</h3>
                    <div class="tags">
                        <span class="tag" @click="addTag('Yamaha')">Yamaha</span>
                        <span class="tag" @click="addTag('Honda')">Honda</span>
                        <span class="tag" @click="addTag('Kawasaki')">Kawasaki</span>
                        <span class="tag" @click="addTag('Suzuki')">Suzuki</span>
                        <span class="tag" @click="addTag('BMW')">BMW</span>
                        <span class="tag" @click="addTag('AGV')">AGV</span>
                        <span class="tag" @click="addTag('Alpinestars')">Alpinestars</span>
                        <span class="tag" @click="addTag('Yoshimura')">Yoshimura</span>
                    </div>
                </div>
                
                <div class="sidebar-section">
                    <h3><i class="fas fa-map-marker-alt"></i> Город</h3>
                    <select v-model="selectedCity" @change="handleCityChange">
                        <option value="">Все города</option>
                        <option value="moscow">Москва</option>
                        <option value="spb">Санкт-Петербург</option>
                        <option value="ekb">Екатеринбург</option>
                        <option value="kazan">Казань</option>
                        <option value="novosibirsk">Новосибирск</option>
                    </select>
                </div>
                
                <div class="sidebar-section">
                    <h3><i class="fas fa-ruble-sign"></i> Цена</h3>
                    <div class="price-range">
                        <input type="range" min="0" max="1000000" v-model="priceRange[0]" @input="updatePriceRange">
                        <input type="range" min="0" max="1000000" v-model="priceRange[1]" @input="updatePriceRange">
                        <div class="price-values">
                            <span>{{ formatPrice(priceRange[0]) }} ₽</span>
                            <span>{{ formatPrice(priceRange[1]) }} ₽</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Список объявлений -->
            <div class="listings">
                <div class="listings-grid">
                    <div v-if="isLoading" class="products-loading">
                        <div class="lodaing-spinner-small"></div>
                        <p>Загрузка объявлений...</p>
                    </div>

                    <div v-else class="listing-card" v-for="item in filteredListings" :key="item.id">
                        <div class="listing-image">
                            <img :src="item.image" :alt="item.title" @error="handleImageError">
                            <div class="listing-badge" :class="item.status">
                                {{ item.is_active ? 'Активно' : 'Продано' }}
                            </div>
                            <div class="listing-favorite" @click="toggleFavorite(item.id)">
                                <i class="fas fa-heart" :class="{ active: item.isFavorite }"></i>
                            </div>
                        </div>
                        
                        <div class="listing-content">
                            <div class="listing-category">{{ item.category }}</div>
                            <h3 class="listing-title">{{ item.title }}</h3>
                            <p class="listing-description">{{ item.description }}</p>
                            
                            <div class="listing-meta">
                                <span class="location">
                                    <i class="fas fa-map-marker-alt"></i> {{ item.town }}
                                </span>
                                <span class="date">
                                    <i class="far fa-clock"></i> {{ item.date_pub }}
                                </span>
                                <span class="views">
                                    <i class="fas fa-eye"></i> {{ item.views }}
                                </span>
                            </div>
                            
                            <div class="listing-footer">
                                <div class="listing-price">
                                    <div class="price">{{ formatPrice(item.cost) }} ₽</div>
                                    <div class="negotiable" v-if="item.is_bargain">Торг уместен</div>
                                </div>
                                <button class="btn btn-outline" @click="showDetails(item)">
                                    Подробнее
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Пагинация -->
                <div class="pagination" v-if="filteredListings.length > 0">
                    <button class="page-btn" :disabled="currentPage === 1" @click="prevPage">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    
                    <span class="page-info">
                        Страница {{ currentPage }} из {{ totalPages }}
                    </span>
                    
                    <button class="page-btn" :disabled="currentPage === totalPages" @click="nextPage">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
                
                <!-- Сообщение если нет объявлений -->
                <div class="empty-state" v-if="filteredListings.length === 0">
                    <i class="fas fa-search"></i>
                    <h3>Объявления не найдены</h3>
                    <p>Попробуйте изменить параметры поиска или фильтры</p>
                    <button class="btn btn-primary" @click="resetFilters">
                        Сбросить фильтры
                    </button>
                </div>
            </div>
        </div>
    </section>

    <!-- Модальное окно нового объявления -->
    <div class="modal" :class="{ active: showModal }">
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-plus-circle"></i> Новое объявление</h3>
                <button class="modal-close" @click="showModal = false">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <form @submit.prevent="submitNewAd">
                    <div class="form-group">
                        <label>Заголовок объявления *</label>
                        <input type="text" v-model="newAd.title" placeholder="Например: Шлем AGV K6, размер L" required>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Категория *</label>
                            <select v-model="newAd.category" required>
                                <option value="">Выберите категорию</option>
                                <option value="motorcycles">Мотоциклы</option>
                                <option value="parts">Запчасти</option>
                                <option value="gear">Экипировка</option>
                                <option value="accessories">Аксессуары</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Цена (₽) *</label>
                            <input type="number" v-model="newAd.price" placeholder="25000" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Описание *</label>
                        <textarea v-model="newAd.description" placeholder="Подробное описание товара..." rows="4" required></textarea>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Город *</label>
                            <input type="text" v-model="newAd.city" placeholder="Москва" required>
                        </div>
                        <div class="form-group">
                            <label>Телефон для связи *</label>
                            <input type="tel" v-model="newAd.phone" placeholder="+7 (XXX) XXX-XX-XX" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Изображения (до 5 шт.)</label>
                        <div class="image-upload">
                            <div class="upload-area" @click="triggerFileInput">
                                <i class="fas fa-cloud-upload-alt"></i>
                                <p>Нажмите для загрузки изображений</p>
                            </div>
                            <input type="file" ref="fileInput" @change="handleImageUpload" multiple accept="image/*" style="display: none;">
                            <div class="image-preview" v-if="newAd.images.length > 0">
                                <div class="preview-item" v-for="(img, index) in newAd.images" :key="index">
                                    <img :src="img" alt="Preview">
                                    <button class="remove-image" @click="removeImage(index)">
                                        <i class="fas fa-times"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="form-actions">
                        <button type="button" class="btn btn-outline" @click="showModal = false">
                            Отмена
                        </button>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-paper-plane"></i> Опубликовать
                        </button>
                    </div>
                </form>
            </div>
        </div>
        <div class="modal-overlay" @click="showModal = false"></div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Market',
    data() {
        return {
            // Данные для фильтров
            activeFilter: 'all',
            searchQuery: '',
            sortBy: 'newest',
            activeTags: [],
            selectedCity: '',
            priceRange: [0, 500000],
            categories: {
                motorcycles: false,
                engines: false,
                frames: false,
                electronics: false,
                helmets: false,
                clothing: false,
                accessories: false
            },
            
            // Пагинация
            currentPage: 1,
            itemsPerPage: 12,
            
            // Модальное окно
            showModal: false,
            newAd: {
                title: '',
                category: '',
                price: '',
                description: '',
                city: '',
                phone: '',
                images: []
            },
            
            // Объявления
            listings: [],
            userListings: [],
            
            // Статистика
            activeListings: 0,
            userActiveListings: 0,
            usersOnline: 0,
            isLoading: true
        }
    },
    computed: {
        limitedProducts() {
            return this.listings.slice(0, 12)
        },

        filteredListings() {
            let filtered = [...this.listings]
            
            // Фильтрация по поисковому запросу
            if (this.searchQuery) {
                const query = this.searchQuery.toLowerCase()
                filtered = filtered.filter(item => 
                    item.title.toLowerCase().includes(query) ||
                    item.description.toLowerCase().includes(query) ||
                    item.category.toLowerCase().includes(query)
                )
            }
            
            // Фильтрация по цене
            filtered = filtered.filter(item => 
                item.cost >= this.priceRange[0] && item.cost <= this.priceRange[1]
            )
            
            // Сортировка
            filtered.sort((a, b) => {
                switch (this.sortBy) {
                    case 'price_low':
                        return a.price - b.price
                    case 'price_high':
                        return b.price - a.price
                    case 'popular':
                        return b.views - a.views
                    default: // newest
                        return new Date(b.date) - new Date(a.date)
                }
            })
            
            return filtered
        },
        totalPages() {
            return Math.ceil(this.filteredListings.length / this.itemsPerPage)
        },
        user() {
            const userData = localStorage.getItem('user')
            return userData ? JSON.parse(userData) : null
        }
    },

    mounted() {
        this.fetchProducts()
    },

    methods: {
        async fetchProducts() {
            try {
                const token = localStorage.getItem('authToken')

                const response = await axios.get('/api/products/get', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                 
                if (response.data) {
                    this.listings = response.data.all_products || []
                    this.userListings = response.data.user_products || []
                    this.activeListings = response.data.product_count || 0
                    this.userActiveListings = response.data.user_product_count || 0

                }
            } catch (error) {
                console.error('Ошибка при получении объявлений: ', error)
                this.listings = []
                this.userListings = []
            } finally {
                this.isLoading = false
            }
        },

        setFilter(filter) {
            this.activeFilter = filter
            this.currentPage = 1
        },
        handleSearch() {
            this.currentPage = 1
        },
        handleSort() {
            this.currentPage = 1
        },
        handleCityChange() {
            this.currentPage = 1
        },
        updatePriceRange() {
            this.currentPage = 1
        },
        formatPrice(price) {
            return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
        },
        showNewAdModal() {
            if (!this.user) {
                alert('Для размещения объявлений необходимо авторизоваться')
                this.$router.push('/login')
                return
            }
            this.showModal = true
        },
        triggerFileInput() {
            this.$refs.fileInput.click()
        },
        handleImageUpload(event) {
            const files = event.target.files
            for (let i = 0; i < Math.min(files.length, 5); i++) {
                const reader = new FileReader()
                reader.onload = (e) => {
                    this.newAd.images.push(e.target.result)
                }
                reader.readAsDataURL(files[i])
            }
        },
        removeImage(index) {
            this.newAd.images.splice(index, 1)
        },
        async submitNewAd() {
            console.log('Новое объявление:', this.newAd)

            const token = localStorage.getItem('authToken')
            
            const response = await fetch('/api/product/new', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(this.newAd)
            })

            if (response.ok) {
                alert('Объявление успешно размещено!')
            }

            this.showModal = false
            this.resetNewAdForm()
        },
        resetNewAdForm() {
            this.newAd = {
                title: '',
                category: '',
                price: '',
                description: '',
                city: '',
                phone: '',
                images: []
            }
        },
        toggleFavorite(id) {
            const item = this.listings.find(item => item.id === id)
            if (item) {
                item.isFavorite = !item.isFavorite
            }
        },
        showDetails(item) {
            console.log('Детали объявления:', item)
            // Здесь можно перейти на страницу детального просмотра
        },
        handleImageError(event) {
            event.target.src = 'https://via.placeholder.com/400x300/333333/ffffff?text=No+Image'
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++
            }
        },
        resetFilters() {
            this.activeFilter = 'all'
            this.searchQuery = ''
            this.sortBy = 'newest'
            this.activeTags = []
            this.selectedCity = ''
            this.priceRange = [0, 500000]
            this.categories = {
                motorcycles: false,
                engines: false,
                frames: false,
                electronics: false,
                helmets: false,
                clothing: false,
                accessories: false
            }
            this.currentPage = 1
        }
    }
}
</script>

<style scoped>
/* ===== ОСНОВНЫЕ СТИЛИ МАРКЕТА ===== */
.market {
    padding: 120px 5% 60px;
    position: relative;
    min-height: calc(100vh - 80px);
}

.market-header {
    background: var(--dark-light);
    border-radius: 20px;
    padding: 40px;
    margin-bottom: 30px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
}

.header-content {
    margin-bottom: 30px;
}

.market-title {
    display: flex;
    align-items: center;
    gap: 15px;
    font-size: 2.5rem;
    font-weight: 300;
    margin-bottom: 15px;
    color: var(--text);
}

.market-title i {
    color: var(--primary);
    text-shadow: 0 0 15px rgba(255, 69, 0, 0.5);
}

.market-subtitle {
    color: var(--text-secondary);
    font-size: 1.1rem;
    max-width: 600px;
    line-height: 1.6;
}

.market-stats {
    display: flex;
    gap: 30px;
    margin-top: 30px;
}

.market-stats .stat-item {
    text-align: center;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    min-width: 150px;
}

.market-stats .stat-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 5px;
}

.market-stats .stat-label {
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.market-actions {
    display: flex;
    gap: 20px;
    align-items: center;
}

.search-box {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px 25px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}

.search-box:focus-within {
    border-color: var(--primary);
    box-shadow: 0 0 15px rgba(255, 69, 0, 0.2);
}

.search-box i {
    color: var(--text-secondary);
    font-size: 18px;
}

.search-box input {
    flex: 1;
    background: none;
    border: none;
    outline: none;
    font-size: 1rem;
    color: var(--text);
}

.search-box input::placeholder {
    color: var(--text-secondary);
}

/* ===== ФИЛЬТРЫ ===== */
.market-filters {
    background: var(--dark-light);
    border-radius: 15px;
    padding: 25px 30px;
    margin-bottom: 30px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.filter-tabs {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}

.filter-tab {
    padding: 10px 24px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 30px;
    color: var(--text-secondary);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
}

.filter-tab:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text);
}

.filter-tab.active {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
    box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);
}

.filter-sort {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 20px;
}

.filter-sort select {
    padding: 12px 20px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    color: var(--text);
    font-size: 1rem;
    min-width: 200px;
    cursor: pointer;
    outline: none;
}

.filter-sort select:focus {
    border-color: var(--primary);
}

.filter-tags {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.filter-tags .tag {
    padding: 8px 16px;
    background: rgba(255, 69, 0, 0.15);
    border-radius: 20px;
    font-size: 0.9rem;
    color: var(--primary);
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.filter-tags .tag:hover {
    background: rgba(255, 69, 0, 0.25);
}

.filter-tags .tag i {
    font-size: 12px;
    cursor: pointer;
}

/* ===== ОСНОВНОЙ КОНТЕНТ ===== */
.market-content {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 30px;
}

/* ===== БОКОВАЯ ПАНЕЛЬ ===== */
.sidebar {
    background: var(--dark-light);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    height: fit-content;
    position: sticky;
    top: 140px;
}

.sidebar-section {
    margin-bottom: 30px;
}

.sidebar-section:last-child {
    margin-bottom: 0;
}

.sidebar-section h3 {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.2rem;
    margin-bottom: 20px;
    color: var(--text);
    font-weight: 600;
}

.sidebar-section h3 i {
    color: var(--primary);
}

.category-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.category-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 15px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.category-item:hover {
    background: rgba(255, 255, 255, 0.1);
}

.category-item input {
    margin-right: 10px;
}

.category-item span:first-of-type {
    flex: 1;
    color: var(--text);
}

.count {
    background: rgba(255, 255, 255, 0.1);
    padding: 3px 10px;
    border-radius: 10px;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.tags {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.tags .tag {
    padding: 8px 16px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    font-size: 0.9rem;
    color: var(--text);
    cursor: pointer;
    transition: all 0.3s ease;
}

.tags .tag:hover {
    background: var(--primary);
    color: white;
    transform: translateY(-2px);
}

.sidebar-section select {
    width: 100%;
    padding: 12px 20px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    color: var(--text);
    font-size: 1rem;
    cursor: pointer;
    outline: none;
}

.sidebar-section select:focus {
    border-color: var(--primary);
}

.price-range {
    padding: 20px 0;
}

.price-range input[type="range"] {
    width: 100%;
    margin: 10px 0;
    -webkit-appearance: none;
    height: 4px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
    outline: none;
}

.price-range input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 20px;
    height: 20px;
    background: var(--primary);
    border-radius: 50%;
    cursor: pointer;
}

.price-values {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
    font-size: 0.9rem;
    color: var(--text-secondary);
}

/* ===== СПИСОК ОБЪЯВЛЕНИЙ ===== */
.listings-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 25px;
    margin-bottom: 40px;
}

.listing-card {
    background: var(--dark-light);
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.listing-card:hover {
    transform: translateY(-5px);
    border-color: var(--primary-dark);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 69, 0, 0.1);
}

.listing-image {
    position: relative;
    height: 200px;
    overflow: hidden;
}

.listing-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.listing-card:hover .listing-image img {
    transform: scale(1.05);
}

.listing-badge {
    position: absolute;
    top: 15px;
    left: 15px;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    z-index: 2;
}

.listing-badge.active {
    background: rgba(0, 255, 0, 0.2);
    color: limegreen;
    border: 1px solid rgba(0, 255, 0, 0.3);
}

.listing-badge.sold {
    background: rgba(255, 0, 0, 0.2);
    color: red;
    border: 1px solid rgba(255, 0, 0, 0.3);
}

.listing-favorite {
    position: absolute;
    top: 15px;
    right: 15px;
    width: 40px;
    height: 40px;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 2;
    transition: all 0.3s ease;
}

.listing-favorite:hover {
    background: rgba(255, 69, 0, 0.8);
}

.listing-favorite i {
    color: white;
    font-size: 18px;
    transition: all 0.3s ease;
}

.listing-favorite i.active {
    color: var(--primary);
    text-shadow: 0 0 10px rgba(255, 69, 0, 0.8);
}

.listing-content {
    padding: 25px;
}

.listing-category {
    color: var(--accent);
    font-size: 0.85rem;
    margin-bottom: 10px;
    font-weight: 500;
}

.listing-title {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 12px;
    color: var(--text);
    line-height: 1.4;
}

.listing-description {
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.5;
    margin-bottom: 20px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.listing-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin-bottom: 20px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.listing-meta span {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.listing-meta i {
    font-size: 14px;
    color: var(--primary);
}

.listing-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.listing-price .price {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 5px;
}

.listing-price .negotiable {
    font-size: 0.85rem;
    color: var(--text-secondary);
}

/* ===== ПАГИНАЦИЯ ===== */
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    padding: 30px 0;
}

.page-btn {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.page-btn:hover:not(:disabled) {
    background: var(--primary);
    border-color: var(--primary);
    transform: scale(1.1);
}

.page-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.page-info {
    color: var(--text-secondary);
    font-size: 0.9rem;
}

/* ===== СОСТОЯНИЕ ПУСТО ===== */
.empty-state {
    text-align: center;
    padding: 80px 40px;
    background: var(--dark-light);
    border-radius: 20px;
    border: 2px dashed rgba(255, 255, 255, 0.1);
}

.empty-state i {
    font-size: 4rem;
    color: var(--text-secondary);
    margin-bottom: 20px;
}

.empty-state h3 {
    font-size: 1.8rem;
    margin-bottom: 15px;
    color: var(--text);
}

.empty-state p {
    color: var(--text-secondary);
    margin-bottom: 30px;
    max-width: 400px;
    margin-left: auto;
    margin-right: auto;
}

/* ===== МОДАЛЬНОЕ ОКНО ===== */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 2000;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.modal.active {
    display: flex;
}

.modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
}

.modal-content {
    position: relative;
    z-index: 2;
    background: var(--dark-light);
    border-radius: 20px;
    width: 100%;
    max-width: 700px;
    max-height: 90vh;
    overflow-y: auto;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30px 30px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text);
}

.modal-header h3 i {
    color: var(--primary);
}

.modal-close {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.modal-close:hover {
    background: var(--primary);
    border-color: var(--primary);
    transform: rotate(90deg);
}

.modal-body {
    padding: 30px;
}

.form-group {
    margin-bottom: 25px;
}

.form-group label {
    display: block;
    margin-bottom: 10px;
    font-weight: 500;
    color: var(--text);
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 15px 20px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    color: var(--text);
    font-size: 1rem;
    outline: none;
    transition: all 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    border-color: var(--primary);
    box-shadow: 0 0 15px rgba(255, 69, 0, 0.2);
}

.form-group textarea {
    resize: vertical;
    min-height: 100px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.image-upload {
    margin-top: 10px;
}

.upload-area {
    padding: 40px;
    border: 2px dashed rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-bottom: 20px;
}

.upload-area:hover {
    border-color: var(--primary);
    background: rgba(255, 69, 0, 0.05);
}

.upload-area i {
    font-size: 3rem;
    color: var(--text-secondary);
    margin-bottom: 15px;
}

.upload-area p {
    color: var(--text-secondary);
}

.image-preview {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 15px;
}

.preview-item {
    position: relative;
    aspect-ratio: 1;
    border-radius: 10px;
    overflow: hidden;
}

.preview-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.remove-image {
    position: absolute;
    top: 5px;
    right: 5px;
    width: 25px;
    height: 25px;
    background: rgba(255, 0, 0, 0.8);
    border-radius: 50%;
    border: none;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 12px;
    transition: all 0.3s ease;
}

.remove-image:hover {
    transform: scale(1.1);
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 15px;
    margin-top: 30px;
}

/* ===== ДЕКОРАТИВНЫЕ ЭЛЕМЕНТЫ ===== */
.decoration {
    position: fixed;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.15;
    z-index: -1;
}

.decoration-1 {
    background: var(--primary);
    top: 10%;
    right: 5%;
}

.decoration-2 {
    background: var(--accent);
    bottom: 10%;
    left: 5%;
}

/* ===== АДАПТИВНОСТЬ ===== */
@media (max-width: 1200px) {
    .market-content {
        grid-template-columns: 1fr;
    }
    
    .sidebar {
        position: static;
        margin-bottom: 30px;
    }
    
    .listings-grid {
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    }
}

@media (max-width: 768px) {
    .market {
        padding: 100px 5% 40px;
    }
    
    .market-title {
        font-size: 2rem;
    }
    
    .market-header {
        padding: 30px 20px;
    }
    
    .market-actions {
        flex-direction: column;
        align-items: stretch;
    }
    
    .market-stats {
        flex-direction: column;
        gap: 15px;
    }
    
    .market-stats .stat-item {
        min-width: auto;
    }
    
    .filter-tabs {
        justify-content: center;
    }
    
    .filter-sort {
        flex-direction: column;
        align-items: stretch;
    }
    
    .listings-grid {
        grid-template-columns: 1fr;
    }
    
    .form-row {
        grid-template-columns: 1fr;
        gap: 15px;
    }
    
    .modal-content {
        max-height: 95vh;
    }
}

@media (max-width: 480px) {
    .market-filters {
        padding: 20px;
    }
    
    .filter-tab {
        padding: 8px 16px;
        font-size: 0.9rem;
    }
    
    .listing-content {
        padding: 20px;
    }
    
    .listing-footer {
        flex-direction: column;
        gap: 15px;
        align-items: stretch;
    }
    
    .listing-footer .btn {
        width: 100%;
    }
}
</style>