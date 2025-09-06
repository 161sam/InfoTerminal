import type { AppProps } from 'next/app';
import '@/styles/globals.css';
import { ThemeProvider } from '@/lib/theme-provider';
import { ToastViewport } from '@/components/ui/Toast';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <ThemeProvider>
      <ToastViewport />
      <Component {...pageProps} />
    </ThemeProvider>
  );
}
