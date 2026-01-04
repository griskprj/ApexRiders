<template>
    <div v-if="isLoading" class="products-loading">
        <div class="loading-spinner-small"></div>
        <p>Загрузка объявлений...</p>
    </div>

    <template v-else-if="filteredListings && filteredListings.length > 0">
        <div class="listing-card" v-for="item in filteredListings" :key="item.id">
            <div class="listing-image">
                <img 
                    :src="getProductImage(item)" 
                    :alt="item.title"
                    @error="handleImageError"
                    loading="lazy"
                >
                <div class="listing-badge" :class="item.is_active ? 'active' : 'sold'">
                    {{ item.is_active ? 'Активно' : 'Продано' }}
                </div>
                <div class="listing-favorite" @click="toggleLike(item.id)">
                    <i class="fas fa-heart" :class="{ active: item.is_liked }"></i>
                </div>
            </div>
            
            <div class="listing-content">
                <div class="listing-category">{{ formatCategory(item.category) }}</div>
                <h3 class="listing-title">{{ item.title }}</h3>
                <p class="listing-description">{{ item.description }}</p>
                
                <div class="listing-meta">
                    <span class="location">
                        <i class="fas fa-map-marker-alt"></i> {{ item.town[0].toUpperCase() + item.town.slice(1) }}
                    </span>
                    <span class="date">
                        <i class="far fa-clock"></i> {{ formatTime(item.date_pub) }}
                    </span>
                    <span class="views">
                        <i class="fas fa-eye"></i> {{ item.watchs }}
                    </span>
                    <span class="likes">
                        <i class="fas fa-heart"></i> {{ item.likes_count }}
                    </span>
                </div>
                
                <div class="listing-footer">
                    <div class="listing-price">
                        <div class="price">{{ formatPrice(item.cost) }} ₽</div>
                        <div class="negotiable" v-if="item.is_bargain">Торг уместен</div>
                    </div>
                    <button class="btn btn-outline" @click="goToDetails(item)">
                        Подробнее
                    </button>
                </div>
            </div>
        </div>
    </template>
</template>

<script>
    export default {
        props: {
            isLoading: Boolean,
            filteredListings: Array,
            handleImageError: Function,
            toggleLike: Function,
            formatTime: Function,
            formatPrice: Function,
        },

        methods: {
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

            goToDetails(item) {
                 this.$router.push(`/market/${item.id}`);
            }
        }
    }
</script>

<style scoped>
    .listing-image {
        position: relative;
        height: 200px;
        overflow: hidden;
    }

    .listing-image img {
        width: 100%;
        height: 100%;
        object-fit: cover; 
        object-position: center; 
        display: block; 
    }

    .no-image-placeholder {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--text-secondary);
        font-size: 0.9rem;
        background: var(--dark);
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

    .listing-meta .likes {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.85rem;
        color: var(--text-secondary);
        z-index: 100;
    }
    
    .listing-meta .likes i {
        font-size: 14px;
        color: var(--primary);
    }
    
    .listing-favorite i.active {
        color: var(--primary);
        text-shadow: 0 0 10px rgba(255, 69, 0, 0.8);
    }
    
    .listing-favorite i {
        transition: all 0.3s ease;
    }
    
    .listing-favorite:hover i {
        transform: scale(1.2);
    }

    @media (max-width: 480px) {
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