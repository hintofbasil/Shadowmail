import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import RequestDelete from "../views/RequestDelete.vue";
import Delete from "../views/Delete.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/request_delete",
    name: "Request delete",
    component: RequestDelete
  },
  {
    path: "/delete",
    name: "Delete",
    component: Delete
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
