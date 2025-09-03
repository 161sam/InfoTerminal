import type { AppProps } from 'next/app';
import '@/styles/globals.css';
import { ThemeProvider } from '@/lib/theme-provider';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <ThemeProvider>
      <Component {...pageProps} />
    </ThemeProvider>
  );
}
