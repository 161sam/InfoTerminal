import { GetServerSideProps } from 'next';

// This dynamic route handles /agent/[tab] URLs
// It redirects to the main /agent page with the tab parameter

export const getServerSideProps: GetServerSideProps = async (context) => {
  const { tab } = context.params as { tab: string };
  
  // Valid tabs for Agent
  const validTabs = ['interaction', 'management'];
  
  // If tab is valid, redirect to agent with query param
  if (validTabs.includes(tab)) {
    return {
      redirect: {
        destination: `/agent?tab=${tab}`,
        permanent: false,
      },
    };
  }
  
  // If tab is invalid, redirect to default agent page
  return {
    redirect: {
      destination: '/agent',
      permanent: false,
    },
  };
};

// This component won't be rendered due to the redirect
export default function AgentTabRedirect() {
  return null;
}
