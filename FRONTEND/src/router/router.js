import { createRouter, createWebHistory } from "vue-router";
import UserLogin from "@/views/user/UserLogin.vue";
import UserSignUp from "@/views/user/UserSignUp.vue";
import AdminLogin from "@/views/user/AdminLogin.vue";
import HomePage from "@/views/HomePage.vue";
import AdminDashboard from "@/views/AdminDashboard.vue";

const routes = [
  { path: "/", redirect: "/home" },
  { path: "/user-login", name: "user-login", component: UserLogin },
  { path: "/user-signup", name: "user-signup", component: UserSignUp },
  { path: "/admin-login", name: "admin-login", component: AdminLogin },
  { path: "/home", name: "home", component: HomePage },
  { path: "/admin-dashboard", name: "admin-dashboard", component: AdminDashboard },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
