import React, { useState } from "react";
import { Copy, Check, Eye, Code, Palette, Book } from "lucide-react";
import {
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
  SubTabs,
  MainTabs,
  NavigationTabs,
  CardTabs,
} from "@/components/ui/tabs";
import {
  LoadingSpinner,
  Skeleton,
  ErrorState,
  EmptyState,
  TabLoadingSkeleton,
  GraphLoadingSkeleton,
} from "@/components/ui/loading";
import Button from "@/components/ui/button";
import Panel from "@/components/layout/Panel";
import { PageLayout, TabbedPageLayout, DashboardLayout } from "@/components/layout/PageLayout";
import DarkModeCompatibilityTest from "./DarkModeTest";

interface ComponentExampleProps {
  title: string;
  description: string;
  code: string;
  children: React.ReactNode;
}

function ComponentExample({ title, description, code, children }: ComponentExampleProps) {
  const [showCode, setShowCode] = useState(false);
  const [copied, setCopied] = useState(false);

  const copyCode = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-4 border border-gray-200 dark:border-gray-700 rounded-lg">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{title}</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{description}</p>
          </div>

          <div className="flex items-center gap-2">
            <Button size="sm" variant="secondary" onClick={() => setShowCode(!showCode)}>
              {showCode ? <Eye size={14} /> : <Code size={14} />}
              {showCode ? "Preview" : "Code"}
            </Button>
            <Button size="sm" variant="outline" onClick={copyCode}>
              {copied ? <Check size={14} /> : <Copy size={14} />}
              {copied ? "Copied!" : "Copy"}
            </Button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        {showCode ? (
          <pre className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg overflow-x-auto text-sm">
            <code className="text-gray-900 dark:text-gray-100">{code}</code>
          </pre>
        ) : (
          <div className="space-y-4">{children}</div>
        )}
      </div>
    </div>
  );
}

export function ComponentShowcase() {
  const [activeTab, setActiveTab] = useState("overview");
  const [demoTab, setDemoTab] = useState("default");
  const [subTab, setSubTab] = useState("explorer");

  return (
    <PageLayout
      title="Design System Showcase"
      description="Interactive component library for InfoTerminal"
      showBreadcrumbs={false}
    >
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Hero Section */}
        <div className="text-center py-12 bg-gradient-to-br from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 rounded-xl border border-primary-200 dark:border-primary-800">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-4">
            InfoTerminal Design System
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            A comprehensive component library built for consistency, accessibility, and performance.
            Explore all components with live examples and ready-to-use code.
          </p>

          <div className="flex items-center justify-center gap-4 mt-8">
            <Button onClick={() => setActiveTab("components")}>
              <Book size={16} className="mr-2" />
              Browse Components
            </Button>
            <Button variant="secondary" onClick={() => setActiveTab("dark-mode")}>
              <Palette size={16} className="mr-2" />
              Dark Mode Test
            </Button>
          </div>
        </div>

        {/* Main Navigation */}
        <Tabs value={activeTab} onValueChange={setActiveTab} variant="default">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="components">Components</TabsTrigger>
            <TabsTrigger value="layouts">Layouts</TabsTrigger>
            <TabsTrigger value="dark-mode">Dark Mode</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Panel title="🎨 Design Principles">
                <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                  <li>
                    • <strong>Consistency:</strong> Unified visual language
                  </li>
                  <li>
                    • <strong>Accessibility:</strong> WCAG 2.1 AA compliant
                  </li>
                  <li>
                    • <strong>Performance:</strong> Lightweight and efficient
                  </li>
                  <li>
                    • <strong>Clarity:</strong> Meaningful naming conventions
                  </li>
                </ul>
              </Panel>

              <Panel title="📦 Component Count">
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Navigation</span>
                    <span className="font-medium">8 components</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Layout</span>
                    <span className="font-medium">6 components</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Feedback</span>
                    <span className="font-medium">12 components</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Forms</span>
                    <span className="font-medium">5 components</span>
                  </div>
                </div>
              </Panel>

              <Panel title="🚀 Quick Start">
                <div className="space-y-3 text-sm">
                  <p className="text-gray-600 dark:text-gray-400">
                    Import components from our design system:
                  </p>
                  <pre className="bg-gray-100 dark:bg-gray-800 p-2 rounded text-xs">
                    {`import { Tabs, TabsList } from 
  '@/components/ui/tabs';`}
                  </pre>
                </div>
              </Panel>

              <Panel title="🌓 Dark Mode Ready">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                  All components support dark mode with proper contrast ratios and accessibility.
                </p>
                <Button size="sm" onClick={() => setActiveTab("dark-mode")}>
                  Test Dark Mode
                </Button>
              </Panel>

              <Panel title="📱 Mobile Responsive">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                  Components adapt automatically to different screen sizes using mobile-first
                  design.
                </p>
                <div className="flex gap-2">
                  <div className="w-4 h-6 bg-primary-200 dark:bg-primary-800 rounded-sm" />
                  <div className="w-6 h-6 bg-primary-300 dark:bg-primary-700 rounded-sm" />
                  <div className="w-8 h-6 bg-primary-400 dark:bg-primary-600 rounded-sm" />
                </div>
              </Panel>

              <Panel title="♿ Accessibility First">
                <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                  <li>• Keyboard navigation</li>
                  <li>• Screen reader support</li>
                  <li>• Focus management</li>
                  <li>• ARIA attributes</li>
                </ul>
              </Panel>
            </div>
          </TabsContent>

          {/* Components Tab */}
          <TabsContent value="components">
            <div className="space-y-12">
              {/* Tab Components */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">
                  Tab Navigation
                </h2>

                <div className="space-y-8">
                  {/* Default Tabs */}
                  <ComponentExample
                    title="Default Tabs"
                    description="Main navigation tabs with background styling"
                    code={`<Tabs value={tab} onValueChange={setTab} variant="default">
  <TabsList>
    <TabsTrigger value="graph" icon={Network}>Graph View</TabsTrigger>
    <TabsTrigger value="viz3d" icon={Cube}>3D Visualization</TabsTrigger>
    <TabsTrigger value="ml" icon={Brain}>ML Analytics</TabsTrigger>
  </TabsList>
  <TabsContent value="graph">Graph content...</TabsContent>
</Tabs>`}
                  >
                    <Tabs value={demoTab} onValueChange={setDemoTab} variant="default">
                      <TabsList>
                        <TabsTrigger value="default">Default</TabsTrigger>
                        <TabsTrigger value="active">Active</TabsTrigger>
                        <TabsTrigger value="disabled" disabled>
                          Disabled
                        </TabsTrigger>
                      </TabsList>
                      <TabsContent value="default">
                        <p className="text-gray-600 dark:text-gray-400 p-4">Default tab content</p>
                      </TabsContent>
                      <TabsContent value="active">
                        <p className="text-gray-600 dark:text-gray-400 p-4">Active tab content</p>
                      </TabsContent>
                    </Tabs>
                  </ComponentExample>

                  {/* Underline Tabs */}
                  <ComponentExample
                    title="Underline Tabs"
                    description="Sub-navigation tabs with minimal styling"
                    code={`<SubTabs value={subTab} onValueChange={setSubTab}>
  <TabsList>
    <TabsTrigger value="explorer" icon={Search}>Explorer</TabsTrigger>
    <TabsTrigger value="query" icon={Code2}>Query</TabsTrigger>
    <TabsTrigger value="analysis" icon={BarChart3}>Analysis</TabsTrigger>
  </TabsList>
</SubTabs>`}
                  >
                    <SubTabs value={subTab} onValueChange={setSubTab}>
                      <TabsList>
                        <TabsTrigger value="explorer">Explorer</TabsTrigger>
                        <TabsTrigger value="query">Query</TabsTrigger>
                        <TabsTrigger value="analysis">Analysis</TabsTrigger>
                        <TabsTrigger value="tools">Tools</TabsTrigger>
                      </TabsList>
                    </SubTabs>
                  </ComponentExample>

                  {/* Pills Tabs */}
                  <ComponentExample
                    title="Pills Tabs"
                    description="Compact pill-shaped tabs for filters"
                    code={`<NavigationTabs defaultValue="all">
  <TabsList>
    <TabsTrigger value="all">All</TabsTrigger>
    <TabsTrigger value="active">Active</TabsTrigger>
    <TabsTrigger value="inactive">Inactive</TabsTrigger>
  </TabsList>
</NavigationTabs>`}
                  >
                    <NavigationTabs defaultValue="all">
                      <TabsList>
                        <TabsTrigger value="all">All</TabsTrigger>
                        <TabsTrigger value="active">Active</TabsTrigger>
                        <TabsTrigger value="inactive">Inactive</TabsTrigger>
                      </TabsList>
                    </NavigationTabs>
                  </ComponentExample>

                  {/* Card Tabs */}
                  <ComponentExample
                    title="Card Tabs"
                    description="Card-style tabs for complex options"
                    code={`<CardTabs defaultValue="basic">
  <TabsList>
    <TabsTrigger value="basic">
      Basic Plan
      <span className="text-xs opacity-70">$10/month</span>
    </TabsTrigger>
    <TabsTrigger value="pro">
      Pro Plan
      <span className="text-xs opacity-70">$25/month</span>
    </TabsTrigger>
  </TabsList>
</CardTabs>`}
                  >
                    <CardTabs defaultValue="basic">
                      <TabsList>
                        <TabsTrigger value="basic">Basic Plan</TabsTrigger>
                        <TabsTrigger value="pro">Pro Plan</TabsTrigger>
                      </TabsList>
                    </CardTabs>
                  </ComponentExample>
                </div>
              </section>

              {/* Loading Components */}
              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">
                  Loading States
                </h2>

                <div className="space-y-8">
                  {/* Spinner Variants */}
                  <ComponentExample
                    title="Loading Spinners"
                    description="Various loading spinner styles and layouts"
                    code={`<LoadingSpinner variant="primary" layout="inline" text="Loading..." />
<LoadingSpinner layout="block" text="Processing" subText="Please wait" />
<LoadingSpinner layout="card" size="lg" text="Analyzing Data" />`}
                  >
                    <div className="space-y-6">
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <LoadingSpinner variant="default" layout="inline" text="Default" />
                        <LoadingSpinner variant="primary" layout="inline" text="Primary" />
                        <LoadingSpinner variant="success" layout="inline" text="Success" />
                        <LoadingSpinner variant="warning" layout="inline" text="Warning" />
                      </div>

                      <LoadingSpinner
                        layout="card"
                        text="Processing Data"
                        subText="This may take a few moments"
                        size="lg"
                      />
                    </div>
                  </ComponentExample>

                  {/* Skeletons */}
                  <ComponentExample
                    title="Skeleton Loaders"
                    description="Placeholder skeletons that maintain layout structure"
                    code={`<Skeleton lines={3} />
<Skeleton width="75%" height={20} />
<TabLoadingSkeleton />
<GraphLoadingSkeleton />`}
                  >
                    <div className="space-y-6">
                      <div className="space-y-3">
                        <Skeleton lines={3} />
                        <Skeleton width="60%" height={16} />
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <Skeleton height={120} />
                        <Skeleton height={120} />
                      </div>
                    </div>
                  </ComponentExample>

                  {/* Error States */}
                  <ComponentExample
                    title="Error & Empty States"
                    description="User-friendly error and empty state components"
                    code={`<ErrorState
  variant="error"
  title="Connection Failed"
  message="Unable to connect to the database"
  action={{ label: "Retry", onClick: retry }}
/>

<EmptyState
  icon={Database}
  title="No Data Available"
  message="Get started by adding some content"
  action={{ label: "Add Data", onClick: addData }}
/>`}
                  >
                    <div className="space-y-6">
                      <ErrorState
                        variant="warning"
                        title="Service Slow"
                        message="The service is responding slowly. Please wait or try again."
                        action={{
                          label: "Retry",
                          onClick: () => console.log("Retry clicked"),
                        }}
                      />

                      <EmptyState
                        title="No Results Found"
                        message="Try adjusting your search criteria"
                        action={{
                          label: "Clear Filters",
                          onClick: () => console.log("Clear filters"),
                        }}
                      />
                    </div>
                  </ComponentExample>
                </div>
              </section>
            </div>
          </TabsContent>

          {/* Layouts Tab */}
          <TabsContent value="layouts">
            <div className="space-y-12">
              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">
                  Layout Components
                </h2>

                <div className="space-y-8">
                  {/* PageLayout */}
                  <ComponentExample
                    title="PageLayout"
                    description="Base layout wrapper with breadcrumbs and responsive design"
                    code={`<PageLayout
  title="My Page"
  description="Page description"
  showBreadcrumbs={true}
  maxWidth="full"
>
  <YourContent />
</PageLayout>`}
                  >
                    <div className="p-6 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
                      <div className="space-y-3">
                        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/3" />
                        <div className="h-32 bg-gray-100 dark:bg-gray-800 rounded" />
                      </div>
                    </div>
                  </ComponentExample>

                  {/* TabbedPageLayout */}
                  <ComponentExample
                    title="TabbedPageLayout"
                    description="Layout with integrated tab navigation"
                    code={`<TabbedPageLayout
  title="Graph Analysis"
  tabs={[
    { key: 'explorer', label: 'Explorer', icon: Search },
    { key: 'query', label: 'Query', icon: Code2 }
  ]}
  activeTab={activeTab}
  onTabChange={setActiveTab}
>
  <TabContent />
</TabbedPageLayout>`}
                  >
                    <div className="space-y-4">
                      <div className="flex gap-2">
                        <div className="px-3 py-2 bg-primary-100 dark:bg-primary-900/30 rounded text-sm">
                          Explorer
                        </div>
                        <div className="px-3 py-2 bg-gray-100 dark:bg-gray-800 rounded text-sm">
                          Query
                        </div>
                      </div>
                      <div className="h-32 bg-gray-50 dark:bg-gray-900 rounded" />
                    </div>
                  </ComponentExample>

                  {/* Panel */}
                  <ComponentExample
                    title="Panel Component"
                    description="Reusable panel container with consistent styling"
                    code={`<Panel title="Graph Statistics">
  <div className="space-y-2">
    <div className="flex justify-between">
      <span>Nodes</span>
      <span>1,234</span>
    </div>
    <div className="flex justify-between">
      <span>Edges</span>
      <span>5,678</span>
    </div>
  </div>
</Panel>`}
                  >
                    <Panel title="Sample Panel">
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600 dark:text-gray-400">Metric 1</span>
                          <span className="font-medium">123</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600 dark:text-gray-400">Metric 2</span>
                          <span className="font-medium">456</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600 dark:text-gray-400">Status</span>
                          <span className="text-green-600 dark:text-green-400">Active</span>
                        </div>
                      </div>
                    </Panel>
                  </ComponentExample>
                </div>
              </section>
            </div>
          </TabsContent>

          {/* Dark Mode Tab */}
          <TabsContent value="dark-mode">
            <DarkModeCompatibilityTest />
          </TabsContent>
        </Tabs>
      </div>
    </PageLayout>
  );
}

export default ComponentShowcase;
