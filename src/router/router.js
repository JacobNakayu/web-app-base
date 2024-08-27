import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import AboutPage from '../views/AboutPage.vue';
import App from '../App.vue'

const routes = [
    {path: '/', name: 'App', component: App},
    { path: '/home', name: 'Home', component: HomePage },
    { path: '/about', name: 'About', component: AboutPage },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
