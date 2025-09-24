import * as React from "react";

export type PanelProps = {
  title?: React.ReactNode;
  subtitle?: React.ReactNode;
  actions?: React.ReactNode;
  footer?: React.ReactNode;
  className?: string;
  padded?: boolean; // default: true
  children?: React.ReactNode;
} & React.HTMLAttributes<HTMLElement>;

/**
 * Unified Panel component (light-first, dark optional).
 * Provides default card styling + optional header/footer.
 *
 * Usage:
 *  <Panel title="My Panel" actions={<Button/>}>content</Panel>
 *  <Panel><Panel.Header>...</Panel.Header><Panel.Body>...</Panel.Body><Panel.Footer>...</Panel.Footer></Panel>
 */
function Panel({
  title,
  subtitle,
  actions,
  footer,
  className,
  padded = true,
  children,
  ...rest
}: PanelProps) {
  const base =
    "bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl shadow-sm";
  const pad = padded ? "p-4 sm:p-6" : "";
  const cls = [base, pad, className].filter(Boolean).join(" ");

  // If consumer uses compound subcomponents, avoid double padding:
  const hasCompound = React.Children.toArray(children).some(
    (c: any) => c?.type?.displayName?.startsWith("Panel.") || c?.props?.["data-panel-slot"],
  );

  return (
    <section className={cls} {...rest}>
      {!hasCompound && (title || actions || subtitle) ? (
        <div className="mb-4 flex items-start justify-between gap-3">
          <div>
            {title && (
              <h2 className="text-base font-semibold text-blue-600 dark:text-slate-100">{title}</h2>
            )}
            {subtitle && <p className="text-sm text-gray-500 dark:text-slate-400">{subtitle}</p>}
          </div>
          {actions && <div className="shrink-0">{actions}</div>}
        </div>
      ) : null}

      {!hasCompound ? <div>{children}</div> : children}

      {!hasCompound && footer ? (
        <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-800">{footer}</div>
      ) : null}
    </section>
  );
}

type SlotProps = React.HTMLAttributes<HTMLDivElement> & { children?: React.ReactNode };

function PanelHeader({ className, children, ...rest }: SlotProps) {
  return (
    <div
      data-panel-slot="header"
      className={["mb-4 flex items-start justify-between gap-3", className]
        .filter(Boolean)
        .join(" ")}
      {...rest}
    >
      {children}
    </div>
  );
}
PanelHeader.displayName = "Panel.Header";

function PanelBody({ className, children, ...rest }: SlotProps) {
  return (
    <div data-panel-slot="body" className={["", className].filter(Boolean).join(" ")} {...rest}>
      {children}
    </div>
  );
}
PanelBody.displayName = "Panel.Body";

function PanelFooter({ className, children, ...rest }: SlotProps) {
  return (
    <div
      data-panel-slot="footer"
      className={["mt-4 pt-4 border-t border-gray-200 dark:border-gray-800", className]
        .filter(Boolean)
        .join(" ")}
      {...rest}
    >
      {children}
    </div>
  );
}
PanelFooter.displayName = "Panel.Footer";

(Panel as any).Header = PanelHeader;
(Panel as any).Body = PanelBody;
(Panel as any).Footer = PanelFooter;

export default Panel;
