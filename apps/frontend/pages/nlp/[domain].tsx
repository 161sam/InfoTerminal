import { GetServerSideProps } from "next";

// This dynamic route handles /nlp/[domain] URLs
// It redirects to the main /nlp page with the domain parameter

export const getServerSideProps: GetServerSideProps = async (context) => {
  const { domain } = context.params as { domain: string };

  // Valid domains for NLP
  const validDomains = ["general", "legal", "documents", "ethics", "forensics"];

  // If domain is valid, redirect to nlp with query param
  if (validDomains.includes(domain)) {
    return {
      redirect: {
        destination: `/nlp?domain=${domain}`,
        permanent: false,
      },
    };
  }

  // If domain is invalid, redirect to default nlp page
  return {
    redirect: {
      destination: "/nlp",
      permanent: false,
    },
  };
};

// This component won't be rendered due to the redirect
export default function NLPDomainRedirect() {
  return null;
}
