import type { GetServerSideProps } from 'next';

export default function SecurityRedirectPage() {
  return null;
}

export const getServerSideProps: GetServerSideProps = async () => ({
  redirect: {
    destination: '/settings?tab=security',
    permanent: false,
    statusCode: 307,
  },
});
