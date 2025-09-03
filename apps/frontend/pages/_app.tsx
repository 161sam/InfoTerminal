import type { AppProps } from 'next/app';
import '../src/styles/globals.css';
import { ThemeProvider } from '../src/lib/theme-provider';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <ThemeProvider>
      <Component {...pageProps} />
    </ThemeProvider>
  );
}
