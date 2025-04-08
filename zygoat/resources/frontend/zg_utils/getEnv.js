import axios from 'axios';

const headers = {
  'X-REQUESTED-WITH': 'XMLHttpRequest',
  'Content-Type': 'application/json',
};

const getEnv = (keys, url = '/api/zygoat/env/') => {
  const resolves = {};
  const env = {};
  let resolveSuccess;

  env.success = new Promise(resolve => {
    resolveSuccess = resolve;
  });

  for (const key of keys) {
    env[key] = new Promise(resolve => {
      resolves[key] = resolve;
    });
  }

  const isSsr = typeof window === 'undefined';
  if (!isSsr) {
    axios({ method: 'GET', url, headers })
      .then(response => {
        for (const [key, resolve] of Object.entries(resolves)) {
          resolve(response.data[key]);
        }
        resolveSuccess(true);
      })
      .catch(() => {
        for (const resolve of Object.values(resolves)) {
          resolve(null);
        }
        resolveSuccess(false);
      });
  } else {
    for (const resolve of Object.values(resolves)) {
      resolve(null);
    }
    resolveSuccess(true);
  }

  return env;
};

export default getEnv;
