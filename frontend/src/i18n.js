import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import translationEN from "./locales/en.json";
import translationHI from "./locales/hi.json";
import translationMR from "./locales/mr.json";
import translationGU from "./locales/gu.json";

// Fetch stored language preference, default to English
const savedLanguage = localStorage.getItem("language") || "en";

const resources = {
  en: {
    translation: translationEN
  },
  hi: {
    translation: translationHI
  },
  mr: {
    translation: translationMR
  },
  gu: {
    translation: translationGU
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: savedLanguage,
    fallbackLng: "en",
    interpolation: {
      escapeValue: false // react already protects from xss
    }
  });

export default i18n;
