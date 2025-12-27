<template>
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
</template>

<script>
    export default {
        props: {
            categories: {
                type: Object,
                required: true,
                default: () => ({
                    motorcycles: false,
                    engines: false,
                    frames: false,
                    electronics: false,
                    helmets: false,
                    clothing: false,
                    accessories: false
                })
            },
            addTag: Function,
            handleCityChange: Function,
            formatPrice: Function,
            updatePriceRange: Function
        },
        data() {
            return {
                selectedCity: '',
                priceRange: [0, 1000000]
            }
        }
    }
</script>

<style scoped>
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

    @media (max-width: 1200px) {
        .sidebar {
            position: static;
            margin-bottom: 30px;
        }
    }
</style>