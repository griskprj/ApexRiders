<template>
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
</template>

<script>
    export default {
        props: {
            activeListings: Number,
            userActiveListings: Number
        }
    }
</script>

<style scoped>
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
</style>