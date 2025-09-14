import type { AppProps } from 'next/app';
import '@/styles/globals.css';
import 'leaflet/dist/leaflet.css';
import { ThemeProvider } from '@/lib/theme-provider';
import { ToastProvider, ToastViewport } from '@/components/ui/toast';
import { AuthProvider } from '@/components/auth/AuthProvider';
import { NotificationProvider } from '@/lib/notifications';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <NotificationProvider>
      <AuthProvider>
        <ThemeProvider>
          <ToastProvider>
            <Component {...pageProps} />
            <ToastViewport />
          </ToastProvider>
        </ThemeProvider>
      </AuthProvider>
    </NotificationProvider>
  );
}
