export const saveToLocalStorage = (key, value) => {
  try {
    localStorage.setItem(key, value);
  } catch (e) {
    console.error('Error saving to localStorage', e);
  }
};

export const getFromLocalStorage = (key) => {
  try {
    return localStorage.getItem(key);
  } catch (e) {
    console.error('Error retrieving from localStorage', e);
    return null;
  }
};

export const removeFromLocalStorage = (key) => {
  try {
    localStorage.removeItem(key);
  } catch (e) {
    console.error('Error removing from localStorage', e);
  }
};
