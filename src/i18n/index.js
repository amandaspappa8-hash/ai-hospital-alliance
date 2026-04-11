import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import ar from "./locales/ar/common.json";
import en from "./locales/en/common.json";
import fr from "./locales/fr/common.json";
import it from "./locales/it/common.json";
import tzm from "./locales/tzm/common.json";
const savedLanguage = localStorage.getItem("aiha_language") || "en";
i18n.use(initReactI18next).init({
    resources: {
        ar: { translation: ar },
        en: { translation: en },
        fr: { translation: fr },
        it: { translation: it },
        tzm: { translation: tzm }
    },
    lng: savedLanguage,
    fallbackLng: "en",
    interpolation: {
        escapeValue: false
    }
});
export default i18n;
