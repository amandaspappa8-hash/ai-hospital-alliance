let memoryFallback = {};

function tryLocalStorage() {
  try {
    const test = "__test__";
    window.localStorage.setItem(test, test);
    window.localStorage.removeItem(test);
    return true;
  } catch {
    return false;
  }
}

const useLocal = typeof window !== "undefined" && tryLocalStorage();

export const safeStorage = {
  get(key) {
    try {
      return useLocal ? window.localStorage.getItem(key) : (memoryFallback[key] ?? null);
    } catch {
      return memoryFallback[key] ?? null;
    }
  },
  set(key, value) {
    try {
      if (useLocal) window.localStorage.setItem(key, value);
      else memoryFallback[key] = value;
    } catch {
      memoryFallback[key] = value;
    }
  },
  remove(key) {
    try {
      if (useLocal) window.localStorage.removeItem(key);
      else delete memoryFallback[key];
    } catch {
      delete memoryFallback[key];
    }
  },
}
