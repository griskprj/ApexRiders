<template>
    <div class="manuals-header">
        <h1 class="manuals-title">
            <i class="fas fa-book"></i>
            <span>Мануалы по ремонту</span>
        </h1>
        <p class="manuals-subtitle">Подробные руководства по обслуживанию и ремонту мотоциклов</p>
        
        <div class="manuals-controls">
            <div class="search-box">
                <i class="fas fa-search"></i>
                <input type="text" placeholder="Поиск по марке, модели или детали..." class="search-input">
            </div>
        </div>
    </div>
</template>

<style scoped>
    .manuals-header {
        margin-bottom: 40px;
    }

    .manuals-title {
        display: flex;
        align-items: center;
        gap: 15px;
        font-size: 2.8rem;
        font-weight: 300;
        margin-bottom: 15px;
        color: var(--text);
    }

    .manuals-title i {
        color: var(--primary);
        text-shadow: 0 0 15px rgba(255, 69, 0, 0.5);
    }

    .manuals-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        margin-bottom: 30px;
        max-width: 600px;
    }

    .search-box {
        position: relative;
        max-width: 600px;
    }

    .search-box i {
        position: absolute;
        left: 20px;
        top: 50%;
        transform: translateY(-50%);
        color: var(--text-secondary);
        font-size: 1.1rem;  
        z-index: 20;
    }

    .search-input {
        width: 100%;
        padding: 18px 20px 18px 50px;
        background: var(--dark-light);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        font-size: 1rem;
        color: var(--text);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);    
    }

    .search-input:focus {
        outline: none;
        border-color: var(--primary);
        box-shadow: 0 0 20px rgba(255, 69, 0, 0.2);
    }

    .search-input::placeholder {
        color: var(--text-secondary);
    }
</style>