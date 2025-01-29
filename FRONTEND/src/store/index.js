import { createStore } from "vuex";
import { user_auth } from "./modules/user_auth";
import { subjects } from "./modules/subjects";
import { chapters } from "./modules/chapters";

export default createStore({
  modules: {
    user_auth, subjects, chapters
  },
});