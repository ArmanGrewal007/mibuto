import { createStore } from "vuex";
import { user_auth } from "./modules/user_auth";
import { subjects } from "./modules/subjects";

export default createStore({
    modules:{
      user_auth, subjects
    },
});