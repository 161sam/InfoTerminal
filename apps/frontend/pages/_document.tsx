import Document, { Html, Head, Main, NextScript } from 'next/document';

// Pre-hydration theme init to avoid flashes
// Uses the same storage key as ThemeProvider ("theme")
const themeInit = `
(function() {
  try {
    var KEY = 'theme';
    var stored = localStorage.getItem(KEY);
    var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    var wantDark = stored === 'dark' || (stored === 'system' && prefersDark);
    if (wantDark) document.documentElement.classList.add('dark');
    else document.documentElement.classList.remove('dark');
  } catch (e) {}
})();
`;

export default class MyDocument extends Document {
  render() {
    return (
      <Html lang="de">
        <Head>
          {/* Early theme init before hydration */}
          <script dangerouslySetInnerHTML={{ __html: themeInit }} />
          <meta name="theme-color" content="#ffffff" />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}

