import { fetchTrafficData } from '../utils/api';

describe('API Utility Functions', () => {
  test('fetchTrafficData returns data when API call is successful', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve([{ source: '192.168.1.1', destination: '192.168.1.2' }]),
      })
    );

    const data = await fetchTrafficData();
    expect(data).toEqual([{ source: '192.168.1.1', destination: '192.168.1.2' }]);
  });

  test('fetchTrafficData returns empty array when API call fails', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: false,
      })
    );

    const data = await fetchTrafficData();
    expect(data).toEqual([]);
  });
});
