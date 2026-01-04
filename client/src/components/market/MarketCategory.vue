<template>
    <div class="sidebar">
        <div class="sidebar-section">
            <h3><i class="fas fa-filter"></i> Категории</h3>
            <div class="category-list">
                <label class="category-item">
                    <input 
                        type="checkbox"
                        :checked="categories.motorcycles"
                        @change="updateCategory('motorcycles', $event.target.checked)"    
                    >
                    <span>Мотоциклы</span>
                    <span class="count">{{ getCategoryCount('motorcycles') }}</span>
                </label>
                <label class="category-item">
                    <input 
                        type="checkbox"
                        :checked="categories.engines"
                        @change="updateCategory('engines', $event.target.checked)"    
                    >
                    <span>Двигатели</span>
                    <span class="count">{{ getCategoryCount('engines') }}</span>
                </label>
                <label class="category-item">
                    <input 
                        type="checkbox"
                        :checked="categories.frames"
                        @change="updateCategory('frames', $event.target.checked)"    
                    >
                    <span>Рамы и подвеска</span>
                    <span class="count">{{ getCategoryCount('frames') }}</span>
                </label>
                <label class="category-item">
                    <input 
                        type="checkbox"
                        :checked="categories.electronics"
                        @change="updateCategory('electronics', $event.target.checked)"    
                    >
                    <span>Электроника</span>
                    <span class="count">{{ getCategoryCount('electronics') }}</span>
                </label>
                <label class="category-item">
                    <input 
                        type="checkbox"
                        :checked="categories.helmets"
                        @change="updateCategory('helmets', $event.target.checked)"    
                    >
                    <span>Шлемы</span>
                    <span class="count">{{ getCategoryCount('helmets') }}</span>
                </label>
                <label class="category-item">
                    <input 
                        type="checkbox"
                        :checked="categories.clothing"
                        @change="updateCategory('clothing', $event.target.checked)"    
                    >
                    <span>Одежда</span>
                    <span class="count">{{ getCategoryCount('clothing') }}</span>
                </label>
                <label class="category-item">
                    <input 
                        type="checkbox"
                        :checked="categories.accessories"
                        @change="updateCategory('accessories', $event.target.checked)"    
                    >
                    <span>Аксессуары</span>
                    <span class="count">{{ getCategoryCount('accessories') }}</span>
                </label>
            </div>
        </div>
        
        <div class="sidebar-section">
            <h3><i class="fas fa-map-marker-alt"></i> Город</h3>
            <select v-model="localCity" @change="handleCityChange">
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
                <div class="price-inputs">
                    <input
                        type="number"
                        v-model="localMinPrice"
                        @input="updatePrice"
                        placeholder="Мин"
                    >
                    <span>-</span>
                    <input
                        type="number"
                        v-model="localMaxPrice"
                        @input="updatePrice"
                        placeholder="Макс"
                    >
                </div>
                <input
                    type="range"
                    min="0"
                    max="5000000"
                    v-model="localMinPrice"
                    @input="updatePrice"
                >
                <input
                    type="range"
                    min="0"
                    max="5000000"
                    v-model="localMaxPrice"
                    @input="updatePrice"
                >
                <div class="price-values">
                    <span>{{ formatPrice(localMinPrice) }} ₽</span>
                    <span>{{ formatPrice(localMaxPrice) }} ₽</span>
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
            },
            formatPrice: Function,
            listings: Array
        },
        data() {
            return {
                localCity: '',
                localMinPrice: 0,
                localMaxPrice: 5000000
            }
        },
        methods: {
            updateCategory(category, checked) {
                this.$emit('category-change', { [category]: checked })
                this.$emit('reset-active-filter')
            },

            handleCityChange() {
                this.$emit('city-change', this.localCity)
            },

            updatePrice() {
                if (this.localMinPrice > this.localMaxPrice) {
                    this.localMinPrice = this.localMaxPrice
                }
                this.$emit('price-change', [this.localMinPrice, this.localMaxPrice])
            },

            getCategoryCount(category) {
                if (!this.listings) return 0

                const categoryMapping = {
                    motorcycles: 'motorcycles',
                    engines: 'engines',
                    frames: 'frames',
                    electronics: 'electronics',
                    helmets: 'helmets',
                    clothing: 'clothing',
                    accessories: 'accessories'
                }

                const categoryValue = categoryMapping[category]
                return this.listings.filter(item => item.category === categoryValue).length
            }
        },
        emits: ['category-change', 'city-change', 'price-change', 'reset-active-filter']
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

    .price-inputs {
        display: flex;
        gap: 10px;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .price-inputs input {
        width: 100px;
        padding: 8px 12px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 6px;
        color: var(--text);
        text-align: center;
    }
    
    .price-inputs span {
        color: var(--text-secondary);
    }

    @media (max-width: 1200px) {
        .sidebar {
            position: static;
            margin-bottom: 30px;
        }
    }
</style>