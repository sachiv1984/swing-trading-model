import { AlertCircle } from "lucide-react";
import { Button } from "./ui/button";

export default function UserNotRegisteredError() {
  const handleContactSupport = () => {
    window.location.href = "mailto:support@yourapp.com?subject=User Registration Issue";
  };

  const handleRetry = () => {
    window.location.reload();
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-slate-950">
      <div className="max-w-md p-8 rounded-xl bg-slate-900 border border-slate-800 text-center">
        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-rose-500/20 flex items-center justify-center">
          <AlertCircle className="w-8 h-8 text-rose-400" />
        </div>
        <h2 className="text-2xl font-bold text-white mb-2">User Not Registered</h2>
        <p className="text-slate-400 mb-6">
          Your account exists but hasn't been set up in this application yet. 
          Please contact support to complete your registration.
        </p>
        <div className="flex gap-3">
          <Button
            onClick={handleRetry}
            variant="outline"
            className="flex-1 border-slate-700 text-slate-300 hover:bg-slate-800"
          >
            Retry
          </Button>
          <Button
            onClick={handleContactSupport}
            className="flex-1 bg-gradient-to-r from-cyan-600 to-violet-600 hover:from-cyan-500 hover:to-violet-500"
          >
            Contact Support
          </Button>
        </div>
      </div>
    </div>
  );
}
