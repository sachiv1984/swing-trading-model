import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";

const tabs = [
  { label: "Feed", path: "/notifications" },
  { label: "Preferences", path: "/notifications/preferences" },
];

export default function NotificationTabBar() {
  const { pathname } = useLocation();

  return (
    <div className="flex gap-1 border-b border-slate-700/50">
      {tabs.map((tab) => {
        const isActive = pathname === tab.path;
        return (
          <Link
            key={tab.path}
            to={tab.path}
            className={cn(
              "px-4 py-2 text-sm font-medium border-b-2 -mb-px transition-colors",
              isActive
                ? "border-cyan-400 text-cyan-400"
                : "border-transparent text-slate-400 hover:text-white"
            )}
          >
            {tab.label}
          </Link>
        );
      })}
    </div>
  );
}
