import { GetServerSideProps } from 'next';

// Redirect from old verification/media-forensics route to new media-forensics route
export const getServerSideProps: GetServerSideProps = async () => {
  return {
    redirect: {
      destination: '/media-forensics',
      permanent: true, // 301 redirect for SEO
    },
  };
};

// This component will never render due to the redirect
export default function MediaForensicsRedirect() {
  return null;
}
