import DocumentUploader from '@/components/docs/DocumentUploader';

export default function DocsPage() {
  return (
    <main style={{ maxWidth: 800, margin: '1rem auto' }}>
      <h1>Dokumente</h1>
      <DocumentUploader />
    </main>
  );
}
