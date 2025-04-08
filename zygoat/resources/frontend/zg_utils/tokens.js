import axios from 'axios';

const TOKEN_REFRESH_INTERVAL = 4 * 60 * 1000; // 4 min in ms

// eslint-disable-next-line default-param-last
export const withReturn = (url, includePath = true, home) => {
  if (typeof window === 'undefined') {
    // server side rendering, so we don't know where to return to
    return url;
  }
  const next = includePath ? window.location.href : window.location.origin;
  const params = new URLSearchParams();
  params.append('next', next);
  params.append('home', home || window.location.origin);
  return `${url}?${params.toString()}`;
};

class TokenFetcher {
  constructor() {
    this.portunusUrl = '';
    this.fetchFunction = this.defaultFetch;
    this.onError = this.defaultOnError;
    this.onSuccess = this.defaultOnSuccess;
    this.currentToken = '';
    this.timerId = null;
    this.tokenCallbacks = [];
    this.lastFetchedAt = Date.now();
  }

  get isLastFetchExpired() {
    return Date.now() - this.lastFetchedAt > TOKEN_REFRESH_INTERVAL;
  }

  get loginUrl() {
    return withReturn(this.portunusUrl, false);
  }

  defaultFetch() {
    return axios({
      method: 'post',
      url: `${this.portunusUrl}/api/auth/token/refresh/`,
      withCredentials: true,
    });
  }

  defaultOnError() {
    window.location.replace(this.loginUrl);
  }

  // eslint-disable-next-line class-methods-use-this
  defaultOnSuccess = () => null;

  get accessToken() {
    return new Promise(resolve => {
      if (this.currentToken) {
        if (this.isLastFetchExpired) {
          this.startAutoFetch().then(() => resolve(this.currentToken));
        } else {
          resolve(this.currentToken);
        }
      } else {
        this.tokenCallbacks.push(resolve);
      }
    });
  }

  fetchToken = async () => {
    try {
      this.currentToken = '';
      const response = await this.fetchFunction();
      this.currentToken = response.data.access;
      this.lastFetchedAt = Date.now();
      this.onSuccess(this.currentToken);
      this.clearCallbacks();
      return true;
    } catch (error) {
      if (error.response) {
        if (error.response.status === 401) {
          this.clearToken();
        }
      }
      this.onError(error);
    }
    return false;
  };

  clearToken() {
    this.currentToken = '';
    clearInterval(this.timerId);
    this.timerId = null;
    this.clearCallbacks();
  }

  startAutoFetch() {
    if (this.timerId) {
      clearInterval(this.timerId);
    }
    this.timerId = setInterval(this.fetchToken, TOKEN_REFRESH_INTERVAL);
    return this.fetchToken();
  }

  clearCallbacks() {
    this.tokenCallbacks.forEach(cb => cb(this.currentToken));
    this.tokenCallbacks = [];
  }

  start(portunusUrl, fetchFn, onSuccess, onError) {
    this.portunusUrl = portunusUrl || this.portunusUrl;
    this.fetchFunction = fetchFn || this.defaultFetch;
    this.onSuccess = onSuccess || this.defaultOnSuccess;
    this.onError = onError || this.defaultOnError;
    if (!this.timerId) {
      this.startAutoFetch();
    }
  }
}

const tokenFetcher = new TokenFetcher();

export default tokenFetcher;
