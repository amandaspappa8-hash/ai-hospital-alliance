import { useTranslation } from "react-i18next";
export function useAppLanguage() {
    const { t, i18n } = useTranslation();
    function setLanguage(lang) {
        localStorage.setItem("aiha_language", lang);
        i18n.changeLanguage(lang);
    }
    return {
        t,
        language: i18n.language,
        setLanguage,
    };
}
