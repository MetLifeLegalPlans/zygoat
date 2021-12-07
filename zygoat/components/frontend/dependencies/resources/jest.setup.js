import '@testing-library/jest-dom/extend-expect';
import mediaQuery from 'css-mediaquery';
import * as nextRouter from 'next/router';

function createMatchMedia(width) {
  return query => ({
    matches: mediaQuery.match(query, { width }),
    addListener: () => {},
    removeListener: () => {},
  });
}

beforeEach(() => {
  window.matchMedia = createMatchMedia(window.innerWidth);
  global.document.createRange = () => ({
    setStart: () => {},
    setEnd: () => {},
    commonAncestorContainer: {
      nodeName: 'BODY',
      ownerDocument: document,
    },
  });

  window.mockedRouter = {
    route: '',
    pathname: '',
    query: '',
    asPath: '',
    // eslint-disable-next-line no-promise-executor-return
    push: jest.fn(() => new Promise(r => r())),
  };

  // eslint-disable-next-line no-import-assign
  nextRouter.useRouter = () => window.mockedRouter;
});
