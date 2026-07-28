import { Info } from "lucide-react";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "../ui/tooltip";

const EXPLAINER_TEXT =
  "Your stop tightens as a position becomes profitable and stays wide while it's losing or flat — this locks in gains without cutting winners short on noise. ATR is recalculated daily (14-day period). Once tightened, a stop never loosens, even if the position gives back some profit.";

export default function TrailingStopExplainerIcon() {
  return (
    <TooltipProvider delayDuration={200}>
      <Tooltip>
        <TooltipTrigger asChild>
          <button
            type="button"
            className="inline-flex items-center justify-center text-slate-600 dark:text-slate-400 hover:text-slate-300"
            aria-label="Why is my stop moving? Explanation of trailing stop behaviour."
          >
            <Info className="w-3.5 h-3.5" />
          </button>
        </TooltipTrigger>
        <TooltipContent className="max-w-xs text-left">
          <p className="font-semibold mb-1">Why is my stop moving?</p>
          <p>{EXPLAINER_TEXT}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
