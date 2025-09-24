import { GetServerSideProps } from "next";

// This dynamic route handles /graphx/[tab] URLs
// It redirects to the main /graphx page with the tab parameter

export const getServerSideProps: GetServerSideProps = async (context) => {
  const { tab } = context.params as { tab: string };

  // Valid tabs for GraphX
  const validTabs = ["graph", "viz3d", "ml"];

  // If tab is valid, redirect to graphx with query param
  if (validTabs.includes(tab)) {
    return {
      redirect: {
        destination: `/graphx?tab=${tab}`,
        permanent: false,
      },
    };
  }

  // If tab is invalid, redirect to default graphx page
  return {
    redirect: {
      destination: "/graphx",
      permanent: false,
    },
  };
};

// This component won't be rendered due to the redirect
export default function GraphXTabRedirect() {
  return null;
}
