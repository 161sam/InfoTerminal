import '../styles/globals.css';
import { ToastViewport } from '../components/ui/Toast';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ToastViewport />
        {children}
      </body>
    </html>
  );
}
