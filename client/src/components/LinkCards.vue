<template>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />

    <div class="cards-wrapper">
        <router-link to="/">
            <div class="link-card">
                <p class="link-title">Apex Wrench</p>
                <span class="material-symbols-outlined card-icon">construction</span>
            </div>
        </router-link>
        <router-link to="/">
            <div class="link-card">
                <p class="link-title">Apex Pitstop</p>
                <span class="material-symbols-outlined card-icon">store</span>
            </div>
        </router-link>
        <router-link to="/">
            <div class="link-card">
                <p class="link-title">Apex Trackpad</p>
                <span class="material-symbols-outlined card-icon">school</span>
            </div>
        </router-link>
    </div>
</template>

<script>
export default {
    name: 'StatsCards'
}
</script>

<style scoped>
a {
    text-decoration: none;
}

.cards-wrapper {
    display: flex;
    flex-direction: row;
    gap: 15px;
}

.link-card {
    width: 200px;
    height: 100px;

    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(7.5px);
    border-radius: 25px;
    color: #FFFFFF;

    display: flex;
    flex-direction: column;
    align-items: center;

    transition: all;
    transition-duration: 500ms; 
}

.link-title {
    margin-top: 10px;
    font-size: 24px;
    font-weight: 400;

    transition: all;
    transition-duration: 500ms;
}

.card-icon {
    font-size: 37px;

    transition: all;
    transition-duration: 500ms;
}

.link-card:hover {
    background: rgba(16, 26, 213, 0.08);
    border: 1px solid #353B8B;
    backdrop-filter: blur(7.5px);
    filter: drop-shadow(0px 0px 16px #353B8B);
    border-radius: 25px;
    color: #92A4FF;

    transition: all;
    transition-duration: 500ms;
}
</style>