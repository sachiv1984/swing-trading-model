import PropTypes from "prop-types";
import { FileDown } from "lucide-react";
import { toast } from "sonner";
import { Button } from "../ui/button";
import { cn } from "../../lib/utils";

// ST-03 (EPIC-01, v9.6, BLG-FEAT-97): same label/weight as the Reports "Download CSV" button.
// Disabled with a "Nothing to export" tooltip when there are no displayed rows; generation is
// synchronous so there is no "Generating…" state. Failure -> Error toast, 8s.
export default function DownloadCsvButton({ onDownload, disabled, className, testId = "download-csv-btn" }) {
  const handleClick = () => {
    try {
      onDownload();
    } catch (e) {
      toast.error("CSV download failed. Please try again.", { duration: 8000 });
    }
  };
  return (
    <Button
      type="button"
      variant="outline"
      onClick={handleClick}
      disabled={disabled}
      title={disabled ? "Nothing to export" : undefined}
      data-testid={testId}
      className={cn("border-slate-600 text-slate-300 hover:text-white hover:border-slate-500 h-9", className)}
    >
      <FileDown className="w-4 h-4 mr-2" />
      Download CSV
    </Button>
  );
}

DownloadCsvButton.propTypes = {
  onDownload: PropTypes.func.isRequired,
  disabled: PropTypes.bool,
  className: PropTypes.string,
  testId: PropTypes.string,
};
