import { useEffect } from "react";
import PropTypes from "prop-types";
import Head from "next/head";
import CssBaseline from "@mui/material/CssBaseline";
import { configure } from "mobx";
import { observer, enableStaticRendering } from "mobx-react";

import { ThemeProvider } from "@mui/material/styles";
import { CacheProvider } from "@emotion/react";
import createCache from "@emotion/cache";

import Nav from "components/Nav";
import GlobalContextProvider from "global-context";
import AuthWatcher from "components/AuthWatcher";

import { theme } from "@bequestinc/wui";

import "global.css";

configure({ enforceActions: "never" });
enableStaticRendering(typeof window === "undefined");

const muiCache = createCache({
  key: "mui",
  prepend: true,
});

const App = ({ Component, pageProps }) => {
  useEffect(() => {
    // Remove the server-side injected CSS.
    const jssStyles = document.querySelector("#jss-server-side");
    if (jssStyles) {
      jssStyles.parentElement.removeChild(jssStyles);
    }
  });

  return (
    <CacheProvider value={muiCache}>
      <GlobalContextProvider>
        <Head>
          <title>Online Wills &amp; Estate Planning</title>
          <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0"
          />
        </Head>

        <CssBaseline />

        <ThemeProvider theme={theme}>
          <Nav />
          <AuthWatcher disabled={Component.public}>
            <Component {...pageProps} />
          </AuthWatcher>
        </ThemeProvider>
      </GlobalContextProvider>
    </CacheProvider>
  );
};

App.propTypes = {
  Component: PropTypes.elementType.isRequired,
  pageProps: PropTypes.object,
};

App.defaultProps = {
  pageProps: {},
};

export default observer(App);
