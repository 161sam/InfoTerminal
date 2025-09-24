import DocumentUploader from "@/components/docs/DocumentUploader";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";

export default function DocsPage() {
  return (
    <DashboardLayout title="Documents">
      <div className="max-w-3xl">
        <h1 className="text-2xl font-semibold mb-6">Dokumente</h1>
        <Panel>
          <DocumentUploader />
        </Panel>
      </div>
    </DashboardLayout>
  );
}
