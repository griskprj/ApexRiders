<script setup>
import EditProductModal from './EditProductModal.vue';
</script>

<template>
    <!-- Декоративные элементы -->
    <div class="decoration decoration-1"></div>
    <div class="decoration decoration-2"></div>

    <!-- Детальная страница объявления -->
    <section class="market-detail" v-if="!isLoading && listing">
        <!-- Хлебные крошки -->
        <nav class="breadcrumbs">
            <router-link to="/market" class="breadcrumb-link">
                <i class="fas fa-arrow-left"></i> Назад к маркету
            </router-link>
            <span class="breadcrumb-separator">/</span>
            <span class="breadcrumb-current">{{ listing.title }}</span>
        </nav>

        <!-- Основной контент -->
        <div class="detail-content">
            <!-- Левая колонка - изображения -->
            <div class="detail-gallery">
                <!-- Главное изображение -->
                <div class="main-image">
                    <img 
                        :src="currentImage" 
                        :alt="listing.title"
                        @error="handleImageError"
                        class="detail-img"
                    >
                    <div class="image-badge" :class="listing.is_active ? 'active' : 'sold'">
                        {{ listing.is_active ? 'Активно' : 'Продано' }}
                    </div>
                    <div class="image-favorite" @click="toggleLike(listing.id)">
                        <i class="fas fa-heart" :class="{ active: listing.is_liked }"></i>
                    </div>
                </div>

                <!-- Миниатюры -->
                <div class="thumbnails" v-if="allImages.length > 1">
                    <div 
                        v-for="(img, index) in allImages" 
                        :key="index"
                        class="thumbnail-item"
                        :class="{ active: currentImageIndex === index }"
                        @click="changeImage(index)"
                    >
                        <img 
                            :src="img" 
                            :alt="`${listing.title} - изображение ${index + 1}`"
                            @error="handleThumbnailError"
                        >
                    </div>
                </div>
            </div>

            <!-- Правая колонка - информация -->
            <div class="detail-info">
                <!-- Заголовок и категория -->
                <div class="detail-header">
                    <div class="detail-category">{{ formatCategory(listing.category) }}</div>
                    <h1 class="detail-title">{{ listing.title }}</h1>
                    <div class="detail-meta">
                        <span class="meta-item">
                            <i class="fas fa-map-marker-alt"></i> {{ formatCity(listing.town) }}
                        </span>
                        <span class="meta-item">
                            <i class="far fa-clock"></i> {{ formatTime(listing.date_pub) }}
                        </span>
                        <span class="meta-item">
                            <i class="fas fa-eye"></i> {{ listing.watchs }} просмотров
                        </span>
                    </div>
                </div>

                <!-- Цена -->
                <div class="detail-price-section">
                    <div class="price-main">
                        <span class="price-value">{{ formatPrice(listing.cost) }} ₽</span>
                        <span class="price-bargain" v-if="listing.is_bargain">
                            <i class="fas fa-handshake"></i> Торг уместен
                        </span>
                        <span class="price-bargain" v-if="listing.status === 'reserved'">
                            <i class="fas fa-box"></i> Товар зарезервирован
                        </span>
                    </div>
                    <div class="price-actions">
                        <button class="btn btn-primary" @click="contactSeller">
                            <i class="fas fa-phone-alt"></i> Связаться с продавцом
                        </button>
                        <button class="btn btn-outline" @click="toggleLike(listing.id)">
                            <i class="fas fa-heart" :class="{ active: listing.is_liked }"></i>
                            {{ listing.is_liked ? 'В избранном' : 'В избранное' }}
                            <span class="like-count">({{ listing.likes_count }})</span>
                        </button>
                    </div>
                </div>

                <!-- Действия для владельца -->
                 <div class="owner-actions" v-if="listing.is_owner">
                    <button class="btn btn-outline" @click="deleteLising(listing.id)" :class="listing.is_active ? '' : 'sold'">
                        <i class="fas fa-trash"></i> Удалить
                    </button>
                    <div v-if="listing.is_active">
                        <button class="btn btn-outline" @click="openEditModal">
                            <i class="fas fa-arrow-up"></i> Редактировать
                        </button>
                        <button class="btn btn-outline" @click="reservedProduct(listing.id)">
                            <i class="fas fa-box"></i> {{ listing.status === 'reserved' ? 'Разрезервировать' : 'Зарезервировать' }}
                        </button>
                        <button class="btn btn-outline" @click="soldProduct(listing.id)">
                            <i class="fas fa-box-open"></i> Продать
                        </button>
                    </div>
                 </div>

                <!-- Описание -->
                <div class="detail-description">
                    <h3><i class="fas fa-align-left"></i> Описание</h3>
                    <div class="description-text">{{ listing.description || 'Описание отсутствует' }}</div>
                </div>

                <!-- Характеристики -->
                <div class="detail-specs" v-if="hasSpecs">
                    <h3><i class="fas fa-list-ul"></i> Характеристики</h3>
                    <div class="specs-grid">
                        <div class="spec-item" v-if="listing.category">
                            <span class="spec-label">Категория:</span>
                            <span class="spec-value">{{ formatCategory(listing.category) }}</span>
                        </div>
                        <div class="spec-item" v-if="listing.town">
                            <span class="spec-label">Город:</span>
                            <span class="spec-value">{{ formatCity(listing.town) }}</span>
                        </div>
                        <div class="spec-item" v-if="listing.brand">
                            <span class="spec-label">Бренд:</span>
                            <span class="spec-value">{{ listing.brand }}</span>
                        </div>
                        <div class="spec-item" v-if="listing.model">
                            <span class="spec-label">Модель:</span>
                            <span class="spec-value">{{ listing.model }}</span>
                        </div>
                        <div class="spec-item" v-if="listing.year">
                            <span class="spec-label">Год:</span>
                            <span class="spec-value">{{ listing.year }}</span>
                        </div>
                        <div class="spec-item" v-if="listing.condition">
                            <span class="spec-label">Состояние:</span>
                            <span class="spec-value">{{ formatCondition(listing.condition) }}</span>
                        </div>
                        <!-- Добавьте другие характеристики по необходимости -->
                    </div>
                </div>

                <!-- Контакты продавца -->
                <div class="detail-seller" v-if="showSellerInfo">
                    <h3><i class="fas fa-user"></i> Продавец</h3>
                    <div class="seller-info">
                        <div class="seller-avatar">
                            <i class="fas fa-user-circle"></i>
                        </div>
                        <div class="seller-details">
                            <div class="seller-name">{{ sellerName }}</div>
                            <div class="seller-rating" v-if="sellerRating">
                                <i class="fas fa-star"></i> {{ sellerRating }}
                            </div>
                            <div class="seller-joined" v-if="sellerJoined">
                                На сайте с {{ sellerJoined }}
                            </div>
                        </div>
                    </div>
                    <div class="seller-contacts">
                        <div class="contact-item" v-if="listing.phone">
                            <i class="fas fa-phone"></i>
                            <span>{{ formatPhone(listing.phone) }}</span>
                        </div>
                        <button class="btn btn-outline btn-small" @click="sendMessage">
                            <i class="fas fa-envelope"></i> Написать сообщение
                        </button>
                    </div>
                </div>

                <!-- Предупреждение для неавторизованных -->
                <div class="auth-warning" v-if="!user">
                    <i class="fas fa-exclamation-circle"></i>
                    <p>Для связи с продавцом необходимо <router-link to="/login">авторизоваться</router-link></p>
                </div>
            </div>
        </div>

        <!-- Похожие объявления -->
        <div class="similar-listings" v-if="similarListings.length > 0">
            <h3><i class="fas fa-th-large"></i> Похожие объявления</h3>
            <div class="similar-grid">
                <div 
                    class="similar-card" 
                    v-for="item in similarListings" 
                    :key="item.id"
                    @click="goToSimilar(item.id)"
                >
                    <div class="similar-image">
                        <img :src="getProductImage(item)" :alt="item.title">
                        <div class="similar-badge" :class="item.is_active ? 'active' : 'sold'">
                            {{ item.is_active ? 'Активно' : 'Продано' }}
                        </div>
                    </div>
                    <div class="similar-content">
                        <div class="similar-category">{{ formatCategory(item.category) }}</div>
                        <h4 class="similar-title">{{ item.title }}</h4>
                        <div class="similar-price">{{ formatPrice(item.cost) }} ₽</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Сообщение если объявление не найдено -->
        <div class="not-found" v-if="!isLoading && !listing">
            <div class="not-found-content">
                <i class="fas fa-search"></i>
                <h3>Объявление не найдено</h3>
                <p>Возможно, оно было удалено или скрыто продавцом</p>
                <router-link to="/market" class="btn btn-primary">
                    <i class="fas fa-arrow-left"></i> Вернуться в маркет
                </router-link>
            </div>
        </div>
    </section>

    <!-- Загрузка -->
    <div class="loading-screen" v-if="isLoading">
        <div class="loading-spinner"></div>
        <p>Загрузка объявления...</p>
    </div>

    <!-- Модальное окно контактов -->
    <div class="contact-modal" v-if="showContactModal">
        <div class="contact-modal-content">
            <div class="contact-modal-header">
                <h3><i class="fas fa-phone-alt"></i> Контакты продавца</h3>
                <button class="modal-close" @click="showContactModal = false">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="contact-modal-body">
                <div class="contact-info">
                    <div class="contact-item full">
                        <i class="fas fa-phone"></i>
                        <div>
                            <div class="contact-label">Телефон</div>
                            <div class="contact-value phone">{{ formatPhone(listing.phone_number) }}</div>
                        </div>
                    </div>
                    <button class="btn btn-primary" @click="callSeller">
                        <i class="fas fa-phone"></i> Позвонить
                    </button>
                </div>
            </div>
        </div>
        <div class="contact-modal-overlay" @click="showContactModal = false"></div>
    </div>

    <!-- Модальное окно редактирования -->
    <EditProductModal
        v-if="editingProduct"
        :showModal="showEditModal"
        :productId="editingProduct.id"
        :productData="editingProduct"
        @close="closeEditModal"
        @update-success="handleUpdateSuccess"
    />
</template>

<script>
import axios from 'axios';

export default {
    name: 'MarketDetail',
    data() {
        return {
            listing: null,
            similarListings: [],
            currentImageIndex: 0,
            isLoading: true,
            showContactModal: false,
            error: null,
            showEditModal: false,
            editingProduct: null
        }
    },
    computed: {
        allImages() {
            if (!this.listing || !this.listing.images) {
                return ['/DefaultListingPhoto.png'];
            }
            
            const images = this.listing.images.map(img => {
                if (typeof img === 'string' && img.trim()) {
                    let filename = img.trim();
                    if (filename.includes('_PNG')) {
                        filename = filename.replace('_PNG', '.png');
                    } else if (!filename.includes('.')) {
                        filename = filename + '.jpg';
                    }
                    return '/uploads/' + filename;
                }
                return '/DefaultListingPhoto.png';
            });
            
            return images.length > 0 ? images : ['/DefaultListingPhoto.png'];
        },
        currentImage() {
            return this.allImages[this.currentImageIndex];
        },
        hasSpecs() {
            return this.listing && (
                this.listing.category ||
                this.listing.brand ||
                this.listing.model ||
                this.listing.year ||
                this.listing.condition
            );
        },
        showSellerInfo() {
            return this.listing && this.listing.phone;
        },
        sellerName() {
            if (this.listing && this.listing.seller_name) {
                return this.listing.seller_name;
            }
            return 'Продавец';
        },
        sellerRating() {
            return this.listing?.seller_rating || null;
        },
        sellerJoined() {
            return this.listing?.seller_joined || null;
        },
        user() {
            const userData = localStorage.getItem('user');
            return userData ? JSON.parse(userData) : null;
        }
    },
    mounted() {
        this.fetchListingDetail();
    },
    methods: {
        async fetchListingDetail() {
            const productId = this.$route.params.id;
            if (!productId) {
                this.error = 'ID объявления не указан';
                this.isLoading = false;
                return;
            }

            try {
                const token = localStorage.getItem('authToken');
                const response = await axios.get(`/api/product/${productId}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.data && response.data.product) {
                    this.listing = response.data.product;
                    this.fetchSimilarListings();
                    this.incrementViews();
                } else {
                    this.error = 'Объявление не найдено';
                }
            } catch (error) {
                console.error('Ошибка при получении объявления:', error);
                this.error = 'Не удалось загрузить объявление';
            } finally {
                this.isLoading = false;
            }
        },

        async fetchSimilarListings() {
            if (!this.listing) return;

            try {
                const token = localStorage.getItem('authToken');
                const response = await axios.get(`/api/products/similar/${this.listing.id}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    params: {
                        category: this.listing.category,
                        limit: 4
                    }
                });

                if (response.data && response.data.products) {
                    this.similarListings = response.data.products;
                }
            } catch (error) {
                console.error('Ошибка при получении похожих объявлений:', error);
            }
        },

        async incrementViews() {
            if (!this.listing) return;

            try {
                const token = localStorage.getItem('authToken');
                await axios.post(`/api/product/${this.listing.id}/view`, {}, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
            } catch (error) {
                console.error('Ошибка при увеличении просмотров:', error);
            }
        },

        async toggleLike(productId) {
            if (!this.user) {
                alert('Для добавления в избранное необходимо авторизоваться');
                this.$router.push('/login');
                return;
            }

            try {
                const token = localStorage.getItem('authToken');
                const response = await axios.post(`/api/product/${productId}/like`, {}, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.data) {
                    this.listing.is_liked = response.data.liked;
                    this.listing.likes_count = response.data.likes_count;
                }
            } catch (error) {
                console.error('Ошибка при изменении лайка:', error);
            }
        },

        async deleteLising(productId) {
            if (!this.listing.is_owner) {
                alert('Вы не являетесь владельцем этого объявления')
                return
            }

            if (!confirm('Вы уверены, что хотите удалить это объявление?')) {
                return
            }

            try {
                const token = localStorage.getItem('authToken')
                const response = await axios.delete(`/api/product/delete/${productId}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })

                if (response.data) {
                    this.$router.replace('/market')
                }
            } catch(error) {
                console.error('Ошибка при удалении:', error)
            }
        },

        async handleUpdateSuccess(updatedData) {
            Object.assign(this.listing, updatedData.product)
            this.closeEditModal()

            alert('Объявление успешно обновлено!')
        },

        async reservedProduct(productId) {
            if (!this.listing.is_owner) {
                alert('Вы не являетесь владельцем этого объявления')
            }

            if (this.listing.status === 'sold') {
                alert('Товар продан!')
            }

            const action = this.listing.status === 'reserved' ? 'разрезервировать' : 'зарезервировать'
            if (!confirm(`Вы уверены, что хотите ${action} это объявление`)) {
                return
            }

            try {
                const token = localStorage.getItem('authToken')
                const response = await axios.put(`/api/product/${productId}/reserved`, {}, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                })

                if (response.data) {
                    this.listing.status = response.data.status
                    alert('Объявление успешно зарезервировано')
                }
            } catch (error) {
                console.error('Ошибка при резервации: ', error)
                if (error.response?.status === 401) {
                    alert('Ошибка авторизации. Пожалуйста, войдите в систему заново.');
                    this.$router.push('/login');
                } else if (error.response?.status === 403) {
                    alert('У вас нет прав для резервирования этого товара');
                } else {
                    alert('Произошла ошибка при резервировании');
                }
            }
        },

        async soldProduct(productId) {
            if (!this.listing.is_owner) {
                alert('Вы не являетесь владельцем этого объявления')
            }

            if (this.listing.status === 'sold') {
                alert('Товар продан!')
            }

            if (!confirm('Вы уверены, что хотите установить статус "продано" для этого объявления? Отменить это действие невозможно!')) {
                return
            }

            try {
                const token = localStorage.getItem('authToken')
                const response = await axios.put(`/api/product/${productId}/sold`, {}, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                })

                if (response.data) {
                    this.listing.is_active = response.data.is_active
                    this.listing.status = response.data.status
                    alert('Для объявления установлен статус "продано"!')
                }
            } catch (error) {
                console.error('Error in sold: ', error)
            }
        },

        changeImage(index) {
            this.currentImageIndex = index;
        },

        handleImageError(event) {
            event.target.src = '/DefaultListingPhoto.png';
            event.target.onerror = null;
        },

        handleThumbnailError(event) {
            event.target.src = '/DefaultListingPhoto.png';
            event.target.onerror = null;
        },

        getProductImage(item) {
            if (!item.images || item.images.length === 0) {
                return '/DefaultListingPhoto.png';
            }

            const firstImage = item.images[0];
            if (typeof firstImage === 'string' && firstImage.trim()) {
                let filename = firstImage.trim();
                if (filename.includes('_PNG')) {
                    filename = filename.replace('_PNG', '.png');
                } else if (!filename.includes('.')) {
                    filename = filename + '.jpg';
                }
                return '/uploads/' + filename;
            }
            
            return '/DefaultListingPhoto.png';
        },

        formatCategory(category) {
            const categoriesMap = {
                'motorcycles': 'Мотоциклы',
                'engines': 'Двигатели',
                'frames': 'Рамы и подвеска',
                'electronics': 'Электроника',
                'helmets': 'Шлемы',
                'clothing': 'Одежда',
                'accessories': 'Аксессуары',
                'parts': 'Запчасти',
                'gear': 'Экипировка'
            };
            return categoriesMap[category] || category;
        },

        formatCity(city) {
            if (!city) return 'Не указан';
            return city.charAt(0).toUpperCase() + city.slice(1);
        },

        formatTime(timeString) {
            if (!timeString) return '';
            const date = new Date(timeString);
            const now = new Date();
            const diff = now - date;
            
            const minutes = Math.floor(diff / 60000);
            const hours = Math.floor(minutes / 60);
            const days = Math.floor(hours / 24);
            
            if (minutes < 60) return `${minutes} мин назад`;
            if (hours < 24) return `${hours} час назад`;
            if (days < 7) return `${days} дн назад`;
            return date.toLocaleDateString('ru-RU');
        },

        formatPrice(price) {
            if (!price) return '0';
            return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
        },

        formatPhone(phone) {
            if (!phone) return 'Не указан';
            // Форматирование телефонного номера
            const cleaned = phone.replace(/\D/g, '');
            if (cleaned.length === 11) {
                return `+${cleaned[0]} (${cleaned.slice(1, 4)}) ${cleaned.slice(4, 7)}-${cleaned.slice(7, 9)}-${cleaned.slice(9)}`;
            }
            return phone;
        },

        formatCondition(condition) {
            const conditions = {
                'new': 'Новое',
                'used': 'Б/у',
                'broken': 'Требует ремонта'
            };
            return conditions[condition] || condition;
        },

        contactSeller() {
            if (!this.user) {
                alert('Для связи с продавцом необходимо авторизоваться');
                this.$router.push('/login');
                return;
            }

            this.showContactModal = true;
        },

        callSeller() {
            if (this.listing.phone) {
                const phoneNumber = this.listing.phone.replace(/\D/g, '');
                window.open(`tel:${phoneNumber}`);
                this.showContactModal = false;
            }
        },

        sendMessage() {
            if (!this.user) {
                alert('Для отправки сообщения необходимо авторизоваться');
                this.$router.push('/login');
                return;
            }

            alert('Функция отправки сообщения будет реализована в будущем');
        },

        goToSimilar(productId) {
            this.$router.push(`/market/${productId}`);
            setTimeout(() => {
                window.location.reload();
            }, 100);
        },

        openEditModal() {
            this.editingProduct = { ...this.listing }
            this.showEditModal = true
        },

        closeEditModal() {
            this.showEditModal = false
            this.editingProduct = null
        },
    }
}
</script>

<style scoped>
/* ===== ОСНОВНЫЕ СТИЛИ ===== */
.market-detail {
    padding: 120px 5% 60px;
    position: relative;
    min-height: calc(100vh - 80px);
}

/* Хлебные крошки */
.breadcrumbs {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 30px;
    padding: 15px 20px;
    background: var(--dark-light);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.breadcrumb-link {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--primary);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
}

.breadcrumb-link:hover {
    color: var(--primary-light);
    transform: translateX(-3px);
}

.breadcrumb-separator {
    color: var(--text-secondary);
}

.breadcrumb-current {
    color: var(--text);
    font-weight: 500;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* Основной контент */
.detail-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    margin-bottom: 60px;
}

/* Галерея изображений */
.detail-gallery {
    position: sticky;
    top: 140px;
    height: fit-content;
}

.main-image {
    position: relative;
    background: var(--dark-light);
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 20px;
    aspect-ratio: 4/3;
}

.detail-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.main-image:hover .detail-img {
    transform: scale(1.02);
}

.image-badge {
    position: absolute;
    top: 20px;
    left: 20px;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 500;
    z-index: 2;
}

.image-badge.active {
    background: rgba(0, 255, 0, 0.2);
    color: limegreen;
    border: 1px solid rgba(0, 255, 0, 0.3);
}

.image-badge.sold {
    background: rgba(255, 0, 0, 0.2);
    color: red;
    border: 1px solid rgba(255, 0, 0, 0.3);
}

.image-favorite {
    position: absolute;
    top: 20px;
    right: 20px;
    width: 48px;
    height: 48px;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 2;
    transition: all 0.3s ease;
}

.image-favorite:hover {
    background: rgba(255, 69, 0, 0.8);
    transform: scale(1.1);
}

.image-favorite i {
    color: white;
    font-size: 20px;
    transition: all 0.3s ease;
}

.image-favorite i.active {
    color: var(--primary);
    text-shadow: 0 0 15px rgba(255, 69, 0, 0.8);
}

/* Миниатюры */
.thumbnails {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
    gap: 10px;
}

.thumbnail-item {
    aspect-ratio: 1;
    border-radius: 10px;
    overflow: hidden;
    cursor: pointer;
    border: 2px solid transparent;
    transition: all 0.3s ease;
    position: relative;
}

.thumbnail-item.active {
    border-color: var(--primary);
    box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);
}

.thumbnail-item:hover {
    transform: translateY(-3px);
}

.thumbnail-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* Информация об объявлении */
.detail-info {
    background: var(--dark-light);
    border-radius: 20px;
    padding: 40px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.detail-header {
    margin-bottom: 30px;
    padding-bottom: 25px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.detail-category {
    color: var(--accent);
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 10px;
    display: inline-block;
    padding: 6px 12px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
}

.detail-title {
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 15px;
    color: var(--text);
    line-height: 1.3;
}

.detail-meta {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.meta-item i {
    color: var(--primary);
    font-size: 14px;
}

/* Цена */
.detail-price-section {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 30px;
}

.price-main {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
}

.price-value {
    font-size: 2.8rem;
    font-weight: 800;
    color: var(--primary);
    text-shadow: 0 0 20px rgba(255, 69, 0, 0.3);
}

.price-bargain {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: rgba(255, 69, 0, 0.1);
    border-radius: 20px;
    color: var(--primary);
    font-size: 0.9rem;
}

.price-actions {
    display: flex;
    gap: 15px;
}

.price-actions .btn {
    flex: 1;
}

/* Действия для владельца */
.owner-actions {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    padding: 25px;

    display: flex;
    flex-direction: row;
    gap: 15px;
    justify-content: center;
    margin-bottom: 30px;
}

.owner-actions .sold {
    width: 100%;
}

/* Описание */
.detail-description {
    margin-bottom: 30px;
    padding-bottom: 30px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.detail-description h3 {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.3rem;
    margin-bottom: 20px;
    color: var(--text);
    font-weight: 600;
}

.detail-description h3 i {
    color: var(--primary);
}

.description-text {
    color: var(--text);
    line-height: 1.6;
    font-size: 1.1rem;
    white-space: pre-line;
}

/* Характеристики */
.detail-specs {
    margin-bottom: 30px;
    padding-bottom: 30px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.detail-specs h3 {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.3rem;
    margin-bottom: 20px;
    color: var(--text);
    font-weight: 600;
}

.detail-specs h3 i {
    color: var(--primary);
}

.specs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 15px;
}

.spec-item {
    display: flex;
    justify-content: space-between;
    padding: 12px 15px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
}

.spec-label {
    color: var(--text-secondary);
    font-weight: 500;
}

.spec-value {
    color: var(--text);
    font-weight: 600;
}

/* Продавец */
.detail-seller {
    margin-bottom: 30px;
}

.detail-seller h3 {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.3rem;
    margin-bottom: 20px;
    color: var(--text);
    font-weight: 600;
}

.detail-seller h3 i {
    color: var(--primary);
}

.seller-info {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 25px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
}

.seller-avatar {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background: var(--dark);
    display: flex;
    align-items: center;
    justify-content: center;
}

.seller-avatar i {
    font-size: 3rem;
    color: var(--text-secondary);
}

.seller-details {
    flex: 1;
}

.seller-name {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 5px;
}

.seller-rating {
    display: flex;
    align-items: center;
    gap: 5px;
    color: #FFD700;
    font-weight: 500;
    margin-bottom: 5px;
}

.seller-joined {
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.seller-contacts {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.contact-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    color: var(--text);
}

.contact-item i {
    color: var(--primary);
    font-size: 1.2rem;
    width: 24px;
}

/* Предупреждение о авторизации */
.auth-warning {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 20px;
    background: rgba(255, 69, 0, 0.1);
    border: 1px solid rgba(255, 69, 0, 0.2);
    border-radius: 15px;
    margin-top: 30px;
}

.auth-warning i {
    color: var(--primary);
    font-size: 1.5rem;
}

.auth-warning p {
    color: var(--text);
    margin: 0;
}

.auth-warning a {
    color: var(--primary);
    text-decoration: none;
    font-weight: 600;
}

.auth-warning a:hover {
    text-decoration: underline;
}

/* Похожие объявления */
.similar-listings {
    background: var(--dark-light);
    border-radius: 20px;
    padding: 40px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.similar-listings h3 {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.5rem;
    margin-bottom: 30px;
    color: var(--text);
    font-weight: 600;
}

.similar-listings h3 i {
    color: var(--primary);
}

.similar-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 25px;
}

.similar-card {
    background: var(--dark);
    border-radius: 15px;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.similar-card:hover {
    transform: translateY(-5px);
    border-color: var(--primary-dark);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 69, 0, 0.1);
}

.similar-image {
    position: relative;
    height: 150px;
    overflow: hidden;
}

.similar-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.similar-card:hover .similar-image img {
    transform: scale(1.05);
}

.similar-badge {
    position: absolute;
    top: 10px;
    left: 10px;
    padding: 4px 10px;
    border-radius: 15px;
    font-size: 0.75rem;
    font-weight: 500;
    z-index: 2;
}

.similar-badge.active {
    background: rgba(0, 255, 0, 0.2);
    color: limegreen;
    border: 1px solid rgba(0, 255, 0, 0.3);
}

.similar-badge.sold {
    background: rgba(255, 0, 0, 0.2);
    color: red;
    border: 1px solid rgba(255, 0, 0, 0.3);
}

.similar-content {
    padding: 20px;
}

.similar-category {
    color: var(--accent);
    font-size: 0.8rem;
    margin-bottom: 8px;
    font-weight: 500;
}

.similar-title {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 10px;
    color: var(--text);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    line-height: 1.3;
}

.similar-price {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--primary);
}

/* Страница не найдена */
.not-found {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 60vh;
    text-align: center;
}

.not-found-content {
    background: var(--dark-light);
    border-radius: 20px;
    padding: 60px 40px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    max-width: 500px;
}

.not-found-content i {
    font-size: 4rem;
    color: var(--text-secondary);
    margin-bottom: 20px;
}

.not-found-content h3 {
    font-size: 1.8rem;
    margin-bottom: 15px;
    color: var(--text);
}

.not-found-content p {
    color: var(--text-secondary);
    margin-bottom: 30px;
}

/* Экран загрузки */
.loading-screen {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 70vh;
    gap: 20px;
}

.loading-spinner {
    width: 60px;
    height: 60px;
    border: 4px solid rgba(255, 255, 255, 0.1);
    border-top: 4px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-screen p {
    color: var(--text-secondary);
    font-size: 1.1rem;
}

/* Модальное окно контактов */
.contact-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 2000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.contact-modal-content {
    position: relative;
    z-index: 2;
    background: var(--dark-light);
    border-radius: 20px;
    width: 100%;
    max-width: 500px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.contact-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 25px 30px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.contact-modal-header h3 {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--text);
}

.contact-modal-header h3 i {
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

.contact-modal-body {
    padding: 30px;
}

.contact-info {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.contact-item.full {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
}

.contact-label {
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-bottom: 5px;
}

.contact-value.phone {
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--text);
}

.contact-modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
}

/* Декоративные элементы */
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

/* Адаптивность */
@media (max-width: 1024px) {
    .detail-content {
        grid-template-columns: 1fr;
        gap: 30px;
    }
    
    .detail-gallery {
        position: static;
    }
    
    .detail-title {
        font-size: 1.8rem;
    }
    
    .price-value {
        font-size: 2.2rem;
    }

    .owner-actions {
        flex-direction: column;
    }
}

@media (max-width: 768px) {
    .market-detail {
        padding: 100px 5% 40px;
    }
    
    .detail-info {
        padding: 30px 25px;
    }
    
    .price-actions {
        flex-direction: column;
    }
    
    .specs-grid {
        grid-template-columns: 1fr;
    }
    
    .similar-grid {
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    }
}

@media (max-width: 480px) {
    .detail-title {
        font-size: 1.5rem;
    }
    
    .price-value {
        font-size: 1.8rem;
    }
    
    .price-main {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }
    
    .detail-meta {
        flex-direction: column;
        gap: 10px;
    }
    
    .seller-info {
        flex-direction: column;
        text-align: center;
        gap: 15px;
    }
    
    .similar-grid {
        grid-template-columns: 1fr;
    }
    
    .contact-modal-content {
        max-width: 100%;
    }
}
</style>