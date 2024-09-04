import { login, getToken, isLoggedIn, logout } from '../utils/auth';

describe('Auth Utility Functions', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test('login stores token on successful login', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ token: 'mock-token' }),
      })
    );

    const success = await login('admin', 'password');
    expect(success).toBe(true);
    expect(getToken()).toBe('mock-token');
  });

  test('login does not store token on failed login', async () => {
    global.fetch = jest.fn(() => Promise.resolve({ ok: false }));

    const success = await login('admin', 'wrong-password');
    expect(success).toBe(false);
    expect(getToken()).toBeNull();
  });

  test('isLoggedIn returns true if token is present', () => {
    localStorage.setItem('token', 'mock-token');
    expect(isLoggedIn()).toBe(true);
  });

  test('isLoggedIn returns false if token is not present', () => {
    expect(isLoggedIn()).toBe(false);
  });

  test('logout removes token', () => {
    localStorage.setItem('token', 'mock-token');
    logout();
    expect(getToken()).toBeNull();
    expect(isLoggedIn()).toBe(false);
  });
});
