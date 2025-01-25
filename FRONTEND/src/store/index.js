import { createStore } from "vuex";
import { user_auth } from "./modules/user_auth";

export default createStore({
    modules:{
      user_auth,
    },
});