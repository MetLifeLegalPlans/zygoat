import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: 'REPLACEME',
  // Note: if you want to override the automatic release value, do not set a
  // `release` value here - use the environment variable `SENTRY_RELEASE`, so
  // that it will also get attached to your source maps
});

export const onRouterTransitionStart = Sentry.captureRouterTransitionStart;
