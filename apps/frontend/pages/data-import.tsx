import { useEffect } from "react";
import { useRouter } from "next/router";

// Legacy redirect: data import moved into the main /data page as the "Import Files" tab.
export default function LegacyDataImportRedirect() {
  const router = useRouter();

  useEffect(() => {
    router.replace({ pathname: "/data", query: { tab: "import" } });
  }, [router]);

  return null;
}
