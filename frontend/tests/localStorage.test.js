import { saveToLocalStorage, getFromLocalStorage, removeFromLocalStorage } from '../utils/localStorage';

describe('LocalStorage Utility Functions', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test('saves and retrieves data from local storage', () => {
    saveToLocalStorage('token', 'mock-token');
    expect(getFromLocalStorage('token')).toBe('mock-token');
  });

  test('removes data from local storage', () => {
    saveToLocalStorage('token', 'mock-token');
    removeFromLocalStorage('token');
    expect(getFromLocalStorage('token')).toBeNull();
  });
});
