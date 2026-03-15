import { computed, ref } from 'vue'
import { messages } from './messages'

const STORAGE_KEY = 'mirofish_locale'
const DEFAULT_LOCALE = 'en'
const SUPPORTED_LOCALES = ['en', 'zh']

const savedLocale =
  typeof window !== 'undefined' ? window.localStorage.getItem(STORAGE_KEY) : null

export const locale = ref(
  SUPPORTED_LOCALES.includes(savedLocale) ? savedLocale : DEFAULT_LOCALE
)

function resolvePath(target, path) {
  return path.split('.').reduce((acc, part) => (acc ? acc[part] : undefined), target)
}

export function setLocale(nextLocale) {
  if (!SUPPORTED_LOCALES.includes(nextLocale)) return
  locale.value = nextLocale
  if (typeof window !== 'undefined') {
    window.localStorage.setItem(STORAGE_KEY, nextLocale)
  }
}

export function t(path, params = {}) {
  const activeMessages = messages[locale.value] || messages[DEFAULT_LOCALE]
  const fallbackMessages = messages[DEFAULT_LOCALE]
  const raw =
    resolvePath(activeMessages, path) ?? resolvePath(fallbackMessages, path) ?? path

  if (typeof raw !== 'string') {
    return raw
  }

  return raw.replace(/\{(\w+)\}/g, (_, key) => `${params[key] ?? `{${key}}`}`)
}

export function tm(path) {
  const activeMessages = messages[locale.value] || messages[DEFAULT_LOCALE]
  return resolvePath(activeMessages, path) ?? resolvePath(messages[DEFAULT_LOCALE], path)
}

export function useI18n() {
  return {
    locale: computed(() => locale.value),
    setLocale,
    t,
    tm
  }
}

