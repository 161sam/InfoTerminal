import SettingsGateway from './components/SettingsGateway';
import SettingsGraphDeepLink from './components/SettingsGraphDeepLink';

export default function SettingsPage() {
  return (
    <div className="p-4 space-y-8">
      <h1 className="text-xl">Settings</h1>
      <section className="space-y-2">
        <h2 className="text-lg">Gateway</h2>
        <SettingsGateway />
      </section>
      <section className="space-y-2">
        <h2 className="text-lg">Graph Deep-Links</h2>
        <SettingsGraphDeepLink />
      </section>
    </div>
  );
}
