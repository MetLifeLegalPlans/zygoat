// UNCOMMENT AFTER SETTING UP AUTH
// import tokenFetcher from '@/zg_utils/tokens';
import axios from 'axios';
import Cookies from 'js-cookie';
import { cookies } from 'next/headers';

interface CookieStore {
  get(name: string): unknown;
}

const isSSR = typeof window === 'undefined';

let baseURL = '/api/';
// Connect directly to the backend host while server-side
// as we're bypassing the reverse proxy there
if (isSSR) {
  baseURL = process.env.BACKEND_URL + baseURL;
}
const client = axios.create({
  baseURL,
  responseType: 'json',
  headers: {
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    'Content-Type': 'application/json',
  },
});
client.interceptors.request.use(async config => {
  let cookieStore = Cookies as CookieStore;
  if (isSSR) {
    cookieStore = (await cookies()) as CookieStore;
  }
  config.headers['X-CSRFToken'] = cookieStore.get('csrftoken');

  // UNCOMMENT AFTER SETTING UP AUTH
  // const accessToken = await tokenFetcher.accessToken;
  // if (accessToken) {
  //   config.headers.Authorization = `Bearer ${accessToken}`;
  // }
  return config;
});

export default client;
