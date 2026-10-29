import { useId, useState } from "react";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "./tooltip";
import { cn } from "../../lib/utils";

export default function ExplainedMarker({ label, description, testId, className, children }) {
  const descriptionId = useId();
  const [open, setOpen] = useState(false);

  const keepOpenOnPress = (event) => event.preventDefault();
  const toggle = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setOpen((wasOpen) => !wasOpen);
  };

  return (
    <TooltipProvider delayDuration={200}>
      <Tooltip open={open} onOpenChange={setOpen}>
        <TooltipTrigger asChild>
          <button
            type="button"
            aria-label={label || undefined}
            aria-describedby={descriptionId}
            data-testid={testId}
            onPointerDown={keepOpenOnPress}
            onClick={toggle}
            className={cn(
              "inline-flex items-center gap-1 rounded focus-visible:outline-none focus-visible:ring-2",
              className
            )}
          >
            {children}
          </button>
        </TooltipTrigger>
        <TooltipContent className="max-w-xs text-left">{description}</TooltipContent>
      </Tooltip>
      <span id={descriptionId} className="sr-only">{description}</span>
    </TooltipProvider>
  );
}
