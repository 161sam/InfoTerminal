import type { AppProps } from 'next/app';
import '@/styles/globals.css';
import 'leaflet/dist/leaflet.css';
import { ThemeProvider } from '@/lib/theme-provider';
import { ToastProvider, ToastViewport } from '@/components/ui/toast';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <ThemeProvider>
      <ToastProvider>
        <Component {...pageProps} />
        <ToastViewport />
      </ToastProvider>
    </ThemeProvider>
  );
}
