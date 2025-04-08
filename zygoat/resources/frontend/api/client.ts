import axios from 'axios';
import Cookies from 'js-cookie';
import { cookies } from 'next/headers';
import tokenFetcher from 'zg_utils/tokens';

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
  let cookieStore = Cookies;
  if (isSSR) {
    cookieStore = await cookies();
  }
  config.headers['X-CSRFToken'] = cookieStore.get('csrftoken');

  const accessToken = await tokenFetcher.accessToken;
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

export default client;
