import { useEffect } from 'react';
import PropTypes from 'prop-types';
import Head from 'next/head';
import ReactDOM from 'react-dom';
import AxeCore from 'axe-core';
import CssBaseline from '@material-ui/core/CssBaseline';

const isSsr = typeof window === 'undefined';

/**
 * Accessibility tool - outputs to devtools console on dev only and client-side only.
 * @see https://github.com/dequelabs/react-axe
 * For full list of a11y rules:
 * @see https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md
 */
if (process.env.NODE_ENV !== 'production' && !isSsr) {
  import('react-axe').then(axe => {
    const config = {
      rules: AxeCore.getRules(['wcag21aa', 'wcag2aa', 'wcag2a']).map(rule => ({
        ...rule,
        id: rule.ruleId,
        enabled: true,
      })),
      disableOtherRules: true,
    };

    axe.default(React, ReactDOM, 1000, config);
  });
}

const App = ({ Component, pageProps }) => {
  useEffect(() => {
    // Remove the server-side injected CSS.
    const jssStyles = document.querySelector('#jss-server-side');
    if (jssStyles) {
      jssStyles.parentElement.removeChild(jssStyles);
    }
  });

  return (
    <>
      <Head>
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0"
        />

        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
        />
      </Head>

      <CssBaseline />
      <Component {...pageProps} />
    </>
  );
};

App.propTypes = {
  Component: PropTypes.elementType.isRequired,
  pageProps: PropTypes.object,
};

App.defaultProps = {
  pageProps: {},
};

export default App;
