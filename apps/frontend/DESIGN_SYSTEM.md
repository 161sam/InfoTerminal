# InfoTerminal Design System Documentation

## Overview

The InfoTerminal Design System provides a comprehensive set of components, patterns, and guidelines for building consistent and accessible user interfaces across the InfoTerminal v1.0.0 platform.

## 🎨 **Design Principles**

### **Consistency**
- Uniform visual language across all pages and components
- Predictable interaction patterns
- Coherent color, typography, and spacing systems

### **Accessibility**
- WCAG 2.1 AA compliant components
- Proper contrast ratios in both light and dark modes
- Keyboard navigation support
- Screen reader friendly markup

### **Performance**
- Lightweight components with minimal bundle impact
- Efficient re-renders and state management
- Responsive design that works across devices

### **Clarity**
- Clear hierarchy and information architecture
- Meaningful naming conventions (no "enhanced", "v2", "ultimate" etc.)
- Purpose-driven component design

---

## 📦 **Component Library**

### **Layout Components**

#### **PageLayout**
```typescript
import { PageLayout } from '@/components/layout/PageLayout';

<PageLayout
  title="Page Title"
  description="Page description for SEO"
  showBreadcrumbs={true}
  maxWidth="full"
  padding={true}
>
  <YourContent />
</PageLayout>
```

**Props:**
- `title`: String - Page title for document head
- `description`: String - Meta description
- `showBreadcrumbs`: Boolean - Show/hide breadcrumb navigation
- `maxWidth`: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full' - Container width
- `padding`: Boolean - Apply default padding
- `className`: String - Additional CSS classes

**Usage:**
- Base layout for all pages
- Automatic breadcrumb integration
- Mobile responsive design
- Dark mode compatible

#### **TabbedPageLayout** 
```typescript
import { TabbedPageLayout } from '@/components/layout/PageLayout';

<TabbedPageLayout
  title="Graph Analysis"
  tabs={[
    { key: 'explorer', label: 'Explorer', icon: Search },
    { key: 'query', label: 'Query', icon: Code2 }
  ]}
  activeTab={activeTab}
  onTabChange={setActiveTab}
>
  <TabContent />
</TabbedPageLayout>
```

**Props:**
- `tabs`: Array of tab objects with key, label, icon, disabled
- `activeTab`: String - Currently active tab key
- `onTabChange`: Function - Tab change handler
- `tabContent`: ReactNode - Optional content above main content

### **Navigation Components**

#### **Enhanced Tabs System**
```typescript
import { Tabs, TabsList, TabsTrigger, TabsContent, SubTabs } from '@/components/ui/tabs';

// Main tabs (default variant)
<Tabs value={tab} onValueChange={setTab} variant="default">
  <TabsList>
    <TabsTrigger value="graph" icon={Network}>Graph View</TabsTrigger>
    <TabsTrigger value="viz3d" icon={Cube}>3D Viz</TabsTrigger>
  </TabsList>
  <TabsContent value="graph">Content</TabsContent>
</Tabs>

// Sub-tabs (underline variant)
<SubTabs value={subTab} onValueChange={setSubTab}>
  <TabsList>
    <TabsTrigger value="explorer" icon={Search}>Explorer</TabsTrigger>
    <TabsTrigger value="query" icon={Code2}>Query</TabsTrigger>
  </TabsList>
</SubTabs>
```

**Variants:**
- `default`: Rounded buttons with background (main navigation)
- `pills`: Pill-shaped buttons (compact areas)
- `underline`: Bottom border tabs (sub-navigation)
- `cards`: Card-style tabs (special layouts)

**Props:**
- `variant`: 'default' | 'pills' | 'underline' | 'cards'
- `orientation`: 'horizontal' | 'vertical'
- `value`: String - Controlled active tab
- `onValueChange`: Function - Change handler
- `icon`: React component - Icon component
- `badge`: String | Number - Badge text
- `description`: String - Tab description

#### **Breadcrumb Navigation**
```typescript
import Breadcrumb, { useBreadcrumbs } from '@/components/navigation/Breadcrumb';

const breadcrumbItems = useBreadcrumbs('/graphx', 'viz3d');

<Breadcrumb 
  items={breadcrumbItems}
  showHome={true}
  className="mb-6"
/>
```

**Auto-Generated Breadcrumbs:**
- `/graphx?tab=viz3d` → Home > Graph Analysis > 3D Visualization
- `/nlp?domain=legal` → Home > NLP Analysis > Legal
- `/agent?tab=management` → Home > AI Agents > Agent Management

### **Feedback Components**

#### **Loading States**
```typescript
import { 
  LoadingSpinner, 
  Skeleton, 
  TabLoadingSkeleton,
  GraphLoadingSkeleton,
  TableLoadingSkeleton 
} from '@/components/ui/loading';

// Inline loading
<LoadingSpinner variant="primary" layout="inline" text="Loading..." />

// Block loading with card
<LoadingSpinner 
  layout="card" 
  text="Processing Data" 
  subText="This may take a few moments"
  size="lg"
/>

// Content skeletons
<Skeleton lines={3} />
<GraphLoadingSkeleton />
<TabLoadingSkeleton />
```

**Loading Variants:**
- `default`: Gray spinner
- `primary`: Primary color spinner
- `success`: Green spinner
- `warning`: Yellow spinner
- `danger`: Red spinner

**Layouts:**
- `inline`: Horizontal layout with text
- `block`: Vertical centered layout
- `overlay`: Full overlay with backdrop
- `card`: Card container with padding

#### **Error & Empty States**
```typescript
import { ErrorState, EmptyState } from '@/components/ui/loading';

<ErrorState
  variant="error"
  title="Connection Failed"
  message="Unable to connect to the graph database"
  action={{
    label: "Retry Connection",
    onClick: retryConnection
  }}
  icon={AlertCircle}
/>

<EmptyState
  icon={Network}
  title="No Graph Data"
  message="Load some data to start exploring"
  action={{
    label: "Load Sample Data",
    onClick: loadSampleData
  }}
/>
```

### **Form Components**

#### **Consistent Input Styling**
```css
/* Standard input classes - use across all forms */
.input-field {
  @apply w-full px-3 py-2 border border-gray-300 dark:border-gray-600 
         rounded-lg focus:ring-2 focus:ring-primary-500 
         bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100
         placeholder-gray-500 dark:placeholder-gray-400;
}

.select-field {
  @apply input-field;
}

.textarea-field {
  @apply input-field resize-vertical;
}
```

**Usage:**
```typescript
<input
  type="text"
  className="input-field"
  placeholder="Enter search term..."
/>

<select className="select-field">
  <option>Select option</option>
</select>

<textarea 
  className="textarea-field"
  rows={4}
  placeholder="Enter description..."
/>
```

---

## 🌓 **Dark Mode System**

### **Color Token System**
```css
/* Primary Colors */
--primary-50: #faf5ff;
--primary-100: #f3e8ff;
--primary-200: #e9d5ff;
--primary-300: #d8b4fe;
--primary-400: #c084fc;
--primary-500: #a855f7;
--primary-600: #9333ea;
--primary-700: #7c3aed;
--primary-800: #6b21a8;
--primary-900: #581c87;

/* Text Colors */
.text-light-primary { @apply text-gray-900; }
.text-light-secondary { @apply text-gray-700; }
.text-light-tertiary { @apply text-gray-600; }

.text-dark-primary { @apply dark:text-gray-100; }
.text-dark-secondary { @apply dark:text-gray-300; }
.text-dark-tertiary { @apply dark:text-gray-400; }
```

### **Background System**
```css
/* Backgrounds */
.bg-surface { @apply bg-white dark:bg-gray-800; }
.bg-surface-secondary { @apply bg-gray-50 dark:bg-gray-900; }
.bg-surface-tertiary { @apply bg-gray-100 dark:bg-gray-800; }

/* Borders */
.border-default { @apply border-gray-200 dark:border-gray-700; }
.border-secondary { @apply border-gray-300 dark:border-gray-600; }
```

### **Component Dark Mode Classes**
```typescript
// Use these class patterns for consistent dark mode
const componentClasses = {
  // Cards and panels
  panel: "bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700",
  
  // Interactive elements
  button: "bg-primary-600 hover:bg-primary-700 text-white",
  buttonSecondary: "bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600",
  
  // Status indicators
  success: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
  warning: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300",
  error: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300",
  info: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300"
};
```

---

## 📱 **Responsive Design**

### **Breakpoint System**
```css
/* Tailwind breakpoints used throughout InfoTerminal */
sm: '640px',   /* Mobile landscape, small tablets */
md: '768px',   /* Tablets */
lg: '1024px',  /* Desktop */
xl: '1280px',  /* Large desktop */
2xl: '1536px'  /* Extra large desktop */
```

### **Mobile-First Components**
```typescript
// Tab navigation responsive patterns
<TabsList className="
  flex-col gap-2 sm:flex-row sm:gap-1 
  w-full sm:w-auto
  p-2 sm:p-1
">
  {/* Mobile: vertical stack, Desktop: horizontal row */}
</TabsList>

// Grid responsive patterns
<div className="
  grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 
  gap-4 lg:gap-6
">
  {/* Mobile: 1 col, Tablet: 2 cols, Desktop: 3 cols */}
</div>
```

### **Mobile Navigation**
```typescript
// Bottom tab navigation (mobile)
const MobileNavigation = {
  bottomTabs: [
    'Dashboard', 'Search', 'Graph', 'NLP', 'Agents'
  ],
  hamburgerMenu: 'expandable with sub-items',
  breakpoint: 'lg:hidden' // Hide on desktop
}
```

---

## 🎯 **Usage Guidelines**

### **When to Use Each Tab Variant**

#### **Default Tabs** (`variant="default"`)
- **Use for:** Main page navigation, primary feature switching
- **Example:** Graph View | 3D Visualization | ML Analytics
- **Style:** Rounded buttons with background color
- **Best for:** 2-5 main options

#### **Underline Tabs** (`variant="underline"`)  
- **Use for:** Sub-navigation, secondary feature groups
- **Example:** Explorer | Query | Analysis | Tools
- **Style:** Bottom border with minimal background
- **Best for:** 3-7 related options

#### **Pills** (`variant="pills"`)
- **Use for:** Compact areas, filter selections, small groups
- **Example:** Active | Inactive | All
- **Style:** Rounded pill shapes
- **Best for:** 2-4 toggle options

#### **Cards** (`variant="cards"`)
- **Use for:** Complex options with descriptions, feature selection
- **Example:** Plan selection, configuration options
- **Style:** Full card layouts with borders
- **Best for:** 2-3 detailed options

### **Loading State Guidelines**

#### **Inline Loading** (`layout="inline"`)
```typescript
// Use inside buttons, small spaces
<Button disabled={isLoading}>
  {isLoading ? <LoadingSpinner size="sm" /> : <Save size={16} />}
  Save Changes
</Button>
```

#### **Block Loading** (`layout="block"`)
```typescript
// Use for entire content areas
{isLoading ? (
  <LoadingSpinner layout="block" text="Loading graph data..." />
) : (
  <GraphVisualization />
)}
```

#### **Skeleton Loading**
```typescript
// Use for maintaining layout during load
{isLoading ? <GraphLoadingSkeleton /> : <GraphComponent />}
```

### **Error Handling Patterns**

#### **Recoverable Errors**
```typescript
<ErrorState
  variant="warning"
  title="Connection Slow"
  message="The service is responding slowly. Please wait or try again."
  action={{ label: "Retry", onClick: retry }}
/>
```

#### **Critical Errors**
```typescript
<ErrorState
  variant="error"  
  title="Service Unavailable"
  message="The graph database is currently unavailable."
  action={{ label: "Go Back", onClick: goBack }}
/>
```

#### **Informational States**
```typescript
<ErrorState
  variant="info"
  title="Maintenance Mode"
  message="This feature is temporarily disabled for maintenance."
/>
```

---

## ✅ **Quality Checklist**

### **Before Using Components**
- [ ] Does the component have proper dark mode classes?
- [ ] Are loading states implemented?
- [ ] Is error handling included?
- [ ] Does it work on mobile devices?
- [ ] Are accessibility attributes present?
- [ ] Is the naming clear and meaningful?

### **Tab Navigation Checklist**
- [ ] Correct variant chosen for context
- [ ] Icons are consistent size (16px for tabs)
- [ ] Loading states show during tab switches
- [ ] URL routing works with tabs
- [ ] Mobile responsive behavior tested
- [ ] Keyboard navigation functional

### **Dark Mode Checklist**
- [ ] All text has proper contrast ratios
- [ ] Borders visible in both modes
- [ ] Interactive states clearly differentiated
- [ ] Status indicators use theme-aware colors
- [ ] No hardcoded colors in components

---

## 🚀 **Getting Started**

### **1. Import Design System Components**
```typescript
// Layout
import { PageLayout, TabbedPageLayout } from '@/components/layout/PageLayout';

// Navigation  
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import Breadcrumb from '@/components/navigation/Breadcrumb';

// Feedback
import { LoadingSpinner, ErrorState, EmptyState } from '@/components/ui/loading';

// Layout building blocks
import Panel from '@/components/layout/Panel';
import Button from '@/components/ui/button';
```

### **2. Follow Naming Conventions**
```typescript
// ✅ Good - Clear, meaningful names
const GraphExplorer = () => {};
const NetworkAnalysis = () => {};  
const UserProfilePanel = () => {};

// ❌ Avoid - Marketing terms, versions
const GraphExplorerEnhanced = () => {};
const NetworkAnalysisV2 = () => {};
const UserProfilePanelPro = () => {};
```

### **3. Implement Consistent Patterns**
```typescript
// Standard page structure
export default function MyPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  if (error) {
    return <ErrorState {...errorProps} />;
  }
  
  return (
    <PageLayout title="My Feature">
      {isLoading ? (
        <LoadingSpinner layout="block" text="Loading..." />
      ) : (
        <YourContent />
      )}
    </PageLayout>
  );
}
```

---

## 📚 **Resources**

- **Figma Design Files**: [Link to design system]
- **Color Palette**: See Dark Mode Test component
- **Icons**: Lucide React icon library
- **Fonts**: System fonts (Inter on most systems)
- **Accessibility**: WCAG 2.1 AA guidelines

---

**InfoTerminal Design System v1.0.0**
*Built for consistency, accessibility, and performance*
