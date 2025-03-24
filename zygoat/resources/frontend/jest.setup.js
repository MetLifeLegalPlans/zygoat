import '@testing-library/jest-dom';
import 'jest-axe/extend-expect';
import mockedRouter from 'next-router-mock';

// eslint-disable-next-line global-require
jest.mock('next/router', () => require('next-router-mock'));
// This is needed for mocking 'next/link':
// eslint-disable-next-line global-require
jest.mock('next/dist/client/router', () => require('next-router-mock'));

mockedRouter.push = jest.fn();

beforeEach(() => {
  window.mockedRouter = mockedRouter;

  // eslint-disable-next-line no-import-assign
  mockedRouter.useRouter = () => window.mockedRouter;
});

jest.mock('next/dynamic', () => func => {
  let component = null;
  func().then(module => {
    component = module.default;
  });
  const DynamicComponent = (...args) => component(...args);
  DynamicComponent.displayName = 'LoadableComponent';
  DynamicComponent.preload = jest.fn();
  return DynamicComponent;
});
