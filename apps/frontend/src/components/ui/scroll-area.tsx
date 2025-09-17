import React from "react";

export interface ScrollAreaProps extends React.HTMLAttributes<HTMLDivElement> {}

function ScrollArea({ className = "", style, children, ...props }: ScrollAreaProps) {
  return (
    <div
      className={`overflow-auto ${className}`}
      style={{ maxHeight: "100%", ...style }}
      {...props}
    >
      {children}
    </div>
  );
}

export { ScrollArea };
export default ScrollArea;

