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
    push: jest.fn(() => new Promise(r => r())),
  };
  nextRouter.useRouter = () => window.mockedRouter;
});
