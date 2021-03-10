import {createRouter, createWebHistory} from "vue-router"

// 基本路由
const constantRoutes = [{
    path: "/login",
    name: "login",
    component: () => import(/* webpackChunkName: "CommonLogin" */ "../views/login/common-login.vue")
},{
    path: "/superlogin",
    component: () => import(/* webpackChunkName: "SuperLogin" */ "../views/login/super-login.vue")
},{
    path: "/admin",
    component: () => import(/* webpackChunkName: "admin" */ "../layout/index.vue"),
    redirect: "/admin/index",
    children: [{
        path: "index",
        component: () => import(/* webpackChunkName: "admin" */ "../views/admin/statistics.vue"),
        meta: {scopes: ["user", "administrator", "supervisor"]},
    },{
        path: "cvadmin",
        component: () => import(/* webpackChunkName: "admin" */ "../views/admin/cv-admin.vue"),
        meta: {scopes: ["user", "administrator", "supervisor"]},
    },{
        path: "mailtemplate",
        component: () => import(/* webpackChunkName: "admin" */ "../views/admin/mail-template.vue"),
        meta: {scopes: ["user", "administrator", "supervisor"]},
    },{
        path: "setting",
        component: () => import(/* webpackChunkName: "admin" */ "../views/admin/setting.vue"),
        meta: {scopes: ["administrator", "supervisor"]},
    },{
        path: "record",
        component: () => import(/* webpackChunkName: "admin" */ "../views/admin/record.vue"),
        meta: {scopes: ["administrator", "supervisor"]},
    },{
        path: "document",
        component: () => import(/* webpackChunkName: "admin" */ "../views/admin/document.vue"),
        meta: {scopes: ["user", "administrator", "supervisor"]},
    }]
  },{
    path: "/:param(.*)",
    redirect: { name: "login" }
}]


const router =  createRouter({
    history: createWebHistory(),
    base: process.env.BASE_URL,
    routes: constantRoutes
})

export default router