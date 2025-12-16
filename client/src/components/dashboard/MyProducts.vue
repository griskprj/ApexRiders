<template>
    <div class="dashboard-card market-card">
        <div class="card-header">
            <h3><i class="fas fa-shopping-cart"></i> Мои объявления</h3>
            <a href="/market" class="card-link">В маркет →</a>
        </div>

        <div v-if="products.length === 0" class="no-products">
            <i class="fas fa-box-open"></i>
            <p>У вас пока нет объявлений</p>
        </div>

        <div v-else class="market-list">
            <div v-for="product in products" :key="product.id" class="market-item">
                <div class="market-status" :class="{
                    'active': product.is_active,
                    'inactive': !product.is_active,
                    'bargain': product.is_bargain
                }">
                    <i class="fas fa-check-circle"></i>
                    {{ getStatusText(product) }}
                </div>
                <div class="market-title">{{ product.title }}</div>
                <div class="market-price">{{ product.cost.toLocaleString('ru-RU') }} ₽</div>
                <div class="market-views">
                    <i class="fas fa-eye"></i> {{ declensionViews(product.watchs) }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        products: {
            type: Array,
            default: () => []
        },
        getStatusText: {
            type: Function,
            required: true
        }
    },
    
    methods: {
        declensionViews(count) {
            const lastDigit = count % 10;
            const lastTwoDigit = count % 100;

            if (lastTwoDigit >= 11 && lastTwoDigit <= 19) {
                return `${count} просмотров`;
            }

            switch (lastDigit) {
                case 1:
                    return `${count} просмотр`;
                    case 2:
                    case 3:
                    case 4:
                        return `${count} просмотра`;
                    default:
                        return `${count} просмотров`
            }
        }
    }
}
</script>

<style scoped>
    .dashboard-card {
        background: var(--dark-light);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }

    .dashboard-card:hover {
        transform: translateY(-5px);
        border-color: var(--primary-dark);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 69, 0, 0.1);
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .card-header h3 {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.4rem;
        font-weight: 600;
    }

    .card-header i {
        color: var(--primary);
    }

    .card-badge {
        background: var(--primary);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    .card-link {
        color: var(--primary);
        text-decoration: none;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }

    .card-link:hover {
        gap: 5px;
    }

    /* ===== МАРКЕТ ===== */
    .market-list {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .market-item {
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border-left: 4px solid var(--primary);
    }

    .market-status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 5px 12px;
        background: rgba(0, 255, 0, 0.1);
        color: limegreen;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-bottom: 10px;
    }

    .market-title {
        font-weight: 600;
        margin-bottom: 10px;
        font-size: 1.1rem;
    }

    .market-price {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 10px;
    }

    .market-views {
        font-size: 0.85rem;
        color: var(--text-secondary);
        display: flex;
        align-items: center;
        gap: 5px;
    }

    .market-loading, .no-products {
        text-align: center;
        padding: 40px 20px;
        color: var(--text-secondary);
    }

    .no-products i {
        font-size: 48px;
        color: var(--text-secondary);
        margin-bottom: 15px;
        opacity: 0.5;
    }

    .no-products p {
        margin-bottom: 20px;
    }
</style>