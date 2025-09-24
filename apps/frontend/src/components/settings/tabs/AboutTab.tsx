import React, { useEffect, useState } from "react";
import { Download, Globe } from "lucide-react";
import Panel from "@/components/layout/Panel";
import Button from "@/components/ui/button";

type RuntimeDetails = {
  runtime: "Server" | "Client";
  buildTime: string;
  userAgentFull: string;
  userAgentSummary: string;
};

export const AboutTab: React.FC = () => {
  const [runtimeDetails, setRuntimeDetails] = useState<RuntimeDetails>({
    runtime: "Server",
    buildTime: "Loading",
    userAgentFull: "N/A",
    userAgentSummary: "N/A",
  });

  useEffect(() => {
    if (typeof window === "undefined") return;
    const ua = navigator.userAgent;
    setRuntimeDetails({
      runtime: "Client",
      buildTime: new Date().toLocaleString(),
      userAgentFull: ua,
      userAgentSummary: ua.split(" ")[0] || ua,
    });
  }, []);

  return (
    <div className="space-y-6">
      <Panel>
        <div className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-2">
              System Information
            </h3>
            <p className="text-sm text-gray-600 dark:text-slate-400">
              Technical details about your installation
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-slate-400">Environment:</span>
                <span className="font-mono text-gray-900 dark:text-slate-100">
                  {process.env.NODE_ENV || "development"}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-slate-400">Runtime:</span>
                <span className="font-mono text-gray-900 dark:text-slate-100">
                  {runtimeDetails.runtime}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-slate-400">Build Time:</span>
                <span className="font-mono text-gray-900 dark:text-slate-100">
                  {runtimeDetails.buildTime}
                </span>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-slate-400">User Agent:</span>
                <span
                  className="font-mono text-gray-900 dark:text-slate-100 text-xs truncate max-w-32"
                  title={runtimeDetails.userAgentFull}
                >
                  {runtimeDetails.userAgentSummary}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-slate-400">Storage:</span>
                <span className="font-mono text-gray-900 dark:text-slate-100">localStorage</span>
              </div>
            </div>
          </div>
        </div>
      </Panel>

      <Panel>
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100">
            Storage & Data
          </h3>
          <div className="text-sm text-gray-600 dark:text-slate-400">
            <p className="mb-2">
              Settings are stored locally in your browser using localStorage with the key:
            </p>
            <code className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded text-xs font-mono">
              it.settings.endpoints
            </code>
          </div>

          <div className="flex gap-2">
            <Button variant="outline" size="sm">
              <Download size={14} className="mr-2" />
              Export Settings
            </Button>
            <Button variant="outline" size="sm">
              <Globe size={14} className="mr-2" />
              Clear Cache
            </Button>
          </div>
        </div>
      </Panel>
    </div>
  );
};

export default AboutTab;
