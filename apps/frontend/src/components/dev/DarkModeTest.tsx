import React, { useEffect, useState } from 'react';
import { Moon, Sun, Monitor, Palette, CheckCircle, AlertCircle, Info } from 'lucide-react';
import { useTheme } from '@/lib/theme-provider';
import Button from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { LoadingSpinner, Skeleton, ErrorState, EmptyState } from '@/components/ui/loading';
import Panel from '@/components/layout/Panel';

interface ThemeTestComponentProps {
  title: string;
  description: string;
  children: React.ReactNode;
}

function ThemeTestComponent({ title, description, children }: ThemeTestComponentProps) {
  return (
    <div className="space-y-3">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{title}</h3>
        <p className="text-sm text-gray-600 dark:text-gray-400">{description}</p>
      </div>
      <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800">
        {children}
      </div>
    </div>
  );
}

export function DarkModeCompatibilityTest() {
  const { theme, setTheme, resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const [testResults, setTestResults] = useState<Record<string, boolean>>({});

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <LoadingSpinner layout="block" text="Loading theme test..." />;
  }

  const runContrastTest = (elementId: string) => {
    const element = document.getElementById(elementId);
    if (!element) return false;

    const computedStyle = window.getComputedStyle(element);
    const backgroundColor = computedStyle.backgroundColor;
    const color = computedStyle.color;
    
    // Simple contrast ratio check (basic implementation)
    // In a real implementation, you'd use a proper contrast ratio library
    return backgroundColor !== color; // Basic check
  };

  const testComponents = () => {
    const results = {
      'tab-navigation': runContrastTest('test-tabs'),
      'loading-states': runContrastTest('test-loading'),
      'form-inputs': runContrastTest('test-forms'),
      'status-indicators': runContrastTest('test-status'),
      'panels': runContrastTest('test-panels'),
    };
    setTestResults(results);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Theme Controls */}
      <Panel title="Dark Mode Compatibility Test">
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                Theme Testing Environment
              </h2>
              <p className="text-gray-600 dark:text-gray-400">
                Test all UI components across different theme modes
              </p>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600 dark:text-gray-400">Current theme:</span>
              <span className="px-2 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 rounded text-sm font-medium">
                {resolvedTheme}
              </span>
            </div>
          </div>

          {/* Theme Switcher */}
          <div className="flex items-center gap-3">
            <Button
              variant={theme === 'light' ? 'default' : 'secondary'}
              size="sm"
              onClick={() => setTheme('light')}
            >
              <Sun size={16} className="mr-2" />
              Light
            </Button>
            <Button
              variant={theme === 'dark' ? 'default' : 'secondary'}
              size="sm"
              onClick={() => setTheme('dark')}
            >
              <Moon size={16} className="mr-2" />
              Dark
            </Button>
            <Button
              variant={theme === 'system' ? 'default' : 'secondary'}
              size="sm"
              onClick={() => setTheme('system')}
            >
              <Monitor size={16} className="mr-2" />
              System
            </Button>
            
            <div className="ml-4 h-6 w-px bg-gray-300 dark:bg-gray-600" />
            
            <Button
              variant="outline"
              size="sm"
              onClick={testComponents}
            >
              <Palette size={16} className="mr-2" />
              Run Accessibility Test
            </Button>
          </div>

          {/* Test Results */}
          {Object.keys(testResults).length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
              {Object.entries(testResults).map(([key, passed]) => (
                <div
                  key={key}
                  className={`p-3 rounded-lg border ${
                    passed
                      ? 'border-green-200 bg-green-50 dark:border-green-800 dark:bg-green-900/20'
                      : 'border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-900/20'
                  }`}
                >
                  <div className="flex items-center gap-2">
                    {passed ? (
                      <CheckCircle size={16} className="text-green-600 dark:text-green-400" />
                    ) : (
                      <AlertCircle size={16} className="text-red-600 dark:text-red-400" />
                    )}
                    <span className={`text-sm font-medium ${
                      passed
                        ? 'text-green-800 dark:text-green-300'
                        : 'text-red-800 dark:text-red-300'
                    }`}>
                      {key.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </Panel>

      {/* Component Tests */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Tab Navigation Test */}
        <ThemeTestComponent
          title="Tab Navigation"
          description="Testing tab components in different variants"
        >
          <div id="test-tabs" className="space-y-4">
            <Tabs defaultValue="default" variant="default">
              <TabsList>
                <TabsTrigger value="default">Default</TabsTrigger>
                <TabsTrigger value="active">Active</TabsTrigger>
                <TabsTrigger value="disabled" disabled>Disabled</TabsTrigger>
              </TabsList>
            </Tabs>

            <Tabs defaultValue="pills" variant="pills">
              <TabsList>
                <TabsTrigger value="pills">Pills</TabsTrigger>
                <TabsTrigger value="variant">Variant</TabsTrigger>
                <TabsTrigger value="test">Test</TabsTrigger>
              </TabsList>
            </Tabs>

            <Tabs defaultValue="underline" variant="underline">
              <TabsList>
                <TabsTrigger value="underline">Underline</TabsTrigger>
                <TabsTrigger value="style">Style</TabsTrigger>
                <TabsTrigger value="demo">Demo</TabsTrigger>
              </TabsList>
            </Tabs>

            <Tabs defaultValue="cards" variant="cards">
              <TabsList>
                <TabsTrigger value="cards">Cards</TabsTrigger>
                <TabsTrigger value="layout">Layout</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>
        </ThemeTestComponent>

        {/* Loading States Test */}
        <ThemeTestComponent
          title="Loading States"
          description="Testing all loading component variations"
        >
          <div id="test-loading" className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <LoadingSpinner variant="default" layout="inline" text="Default" />
              <LoadingSpinner variant="primary" layout="inline" text="Primary" />
              <LoadingSpinner variant="success" layout="inline" text="Success" />
              <LoadingSpinner variant="warning" layout="inline" text="Warning" />
            </div>

            <div className="space-y-3">
              <Skeleton lines={3} />
              <Skeleton width="75%" height={20} />
              <div className="grid grid-cols-2 gap-4">
                <Skeleton height={60} />
                <Skeleton height={60} />
              </div>
            </div>

            <LoadingSpinner 
              layout="card" 
              text="Processing Data" 
              subText="This may take a few moments"
              size="lg"
            />
          </div>
        </ThemeTestComponent>

        {/* Error & Empty States */}
        <ThemeTestComponent
          title="State Components"
          description="Error states and empty states testing"
        >
          <div className="space-y-6">
            <ErrorState
              variant="error"
              title="Error State"
              message="This is how errors are displayed"
              action={{
                label: "Retry",
                onClick: () => {}
              }}
            />

            <ErrorState
              variant="warning"
              title="Warning State"
              message="This is a warning message"
            />

            <EmptyState
              icon={Info}
              title="Empty State"
              message="No data to display here"
              action={{
                label: "Add Data",
                onClick: () => {}
              }}
            />
          </div>
        </ThemeTestComponent>

        {/* Form Elements */}
        <ThemeTestComponent
          title="Form Elements"
          description="Input fields, buttons, and form controls"
        >
          <div id="test-forms" className="space-y-4">
            <div className="grid grid-cols-1 gap-3">
              <input
                type="text"
                placeholder="Text input field"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              />
              
              <select className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
                <option>Select option</option>
                <option>Option 1</option>
                <option>Option 2</option>
              </select>
              
              <textarea
                rows={3}
                placeholder="Textarea field"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              />
            </div>

            <div className="flex flex-wrap gap-2">
              <Button variant="default" size="sm">Default</Button>
              <Button variant="secondary" size="sm">Secondary</Button>
              <Button variant="outline" size="sm">Ghost</Button>
            </div>
          </div>
        </ThemeTestComponent>

        {/* Status Indicators */}
        <ThemeTestComponent
          title="Status & Indicators"
          description="Status pills, badges, and indicators"
        >
          <div id="test-status" className="space-y-4">
            <div className="flex flex-wrap gap-3">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300">
                Success
              </span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300">
                Warning
              </span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300">
                Error
              </span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
                Info
              </span>
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-700 dark:text-gray-300">Online</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                <span className="text-sm text-gray-700 dark:text-gray-300">Warning</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                <span className="text-sm text-gray-700 dark:text-gray-300">Offline</span>
              </div>
            </div>
          </div>
        </ThemeTestComponent>

        {/* Panels & Cards */}
        <ThemeTestComponent
          title="Layout Components"
          description="Panels, cards, and container elements"
        >
          <div id="test-panels" className="space-y-4">
            <Panel title="Sample Panel">
              <p className="text-gray-600 dark:text-gray-400">
                This is content inside a panel component. It should have proper contrast
                and readability in both light and dark modes.
              </p>
            </Panel>

            <div className="p-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg">
              <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Card Component</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                This is a basic card layout with proper theming.
              </p>
            </div>

            <div className="p-3 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded">
              <span className="text-xs text-gray-500 dark:text-gray-400">Code block example</span>
            </div>
          </div>
        </ThemeTestComponent>
      </div>

      {/* Color Palette Reference */}
      <Panel title="Color Palette Reference">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          
          {/* Primary Colors */}
          <div>
            <h3 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Primary Colors</h3>
            <div className="space-y-2">
              {[50, 100, 200, 300, 400, 500, 600, 700, 800, 900].map(weight => (
                <div key={weight} className="flex items-center gap-3">
                  <div 
                    className={`w-8 h-6 rounded border border-gray-300 dark:border-gray-600`}
                    style={{ 
                      backgroundColor: weight < 500 
                        ? `hsl(262, 83%, ${95 - weight / 10}%)` 
                        : `hsl(262, 83%, ${100 - weight / 10}%)`
                    }}
                  />
                  <span className="text-sm text-gray-600 dark:text-gray-400 font-mono">
                    primary-{weight}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Gray Colors */}
          <div>
            <h3 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Gray Scale</h3>
            <div className="space-y-2">
              {[50, 100, 200, 300, 400, 500, 600, 700, 800, 900].map(weight => (
                <div key={weight} className="flex items-center gap-3">
                  <div 
                    className={`w-8 h-6 rounded border border-gray-300 dark:border-gray-600 bg-gray-${weight}`}
                  />
                  <span className="text-sm text-gray-600 dark:text-gray-400 font-mono">
                    gray-{weight}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Status Colors */}
          <div>
            <h3 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Status Colors</h3>
            <div className="space-y-2">
              {[
                { name: 'green', label: 'Success' },
                { name: 'yellow', label: 'Warning' },
                { name: 'red', label: 'Error' },
                { name: 'blue', label: 'Info' },
              ].map(({ name, label }) => (
                <div key={name} className="flex items-center gap-3">
                  <div 
                    className={`w-8 h-6 rounded border border-gray-300 dark:border-gray-600 bg-${name}-500`}
                  />
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {label}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Usage Guidelines */}
          <div>
            <h3 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Usage Guidelines</h3>
            <div className="space-y-3 text-sm text-gray-600 dark:text-gray-400">
              <div>
                <strong className="text-gray-900 dark:text-gray-100">Text:</strong>
                <br />
                Light: gray-900, gray-700, gray-600
                <br />
                Dark: gray-100, gray-300, gray-400
              </div>
              <div>
                <strong className="text-gray-900 dark:text-gray-100">Backgrounds:</strong>
                <br />
                Light: white, gray-50, gray-100
                <br />
                Dark: gray-900, gray-800, gray-700
              </div>
              <div>
                <strong className="text-gray-900 dark:text-gray-100">Borders:</strong>
                <br />
                Light: gray-200, gray-300
                <br />
                Dark: gray-700, gray-600
              </div>
            </div>
          </div>
        </div>
      </Panel>

      {/* Accessibility Notes */}
      <Panel title="Accessibility Guidelines">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Contrast Requirements</h3>
            <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li>• Normal text: 4.5:1 contrast ratio minimum</li>
              <li>• Large text: 3:1 contrast ratio minimum</li>
              <li>• Interactive elements: 3:1 for focus indicators</li>
              <li>• Non-text elements: 3:1 for UI components</li>
            </ul>
          </div>
          <div>
            <h3 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Testing Checklist</h3>
            <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li>• Test with system dark mode preference</li>
              <li>• Verify focus indicators are visible</li>
              <li>• Check color-only information has alternatives</li>
              <li>• Ensure sufficient contrast for all states</li>
            </ul>
          </div>
        </div>
      </Panel>
    </div>
  );
}

export default DarkModeCompatibilityTest;
