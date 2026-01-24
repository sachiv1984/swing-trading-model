import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { createPageUrl } from "../utils/utils";
import { motion, AnimatePresence } from "framer-motion";
import { 
  LayoutDashboard, 
  Briefcase, 
  PlusCircle, 
  History, 
  Settings,
  Menu,
  X,
  Sun,
  Moon,
  TrendingUp,
  ExternalLink,
  FileBarChart
} from "lucide-react";
import { Button } from "./components/ui/button";
import { cn } from "../lib/utils";

export default function Layout({ children, currentPageName }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [theme, setTheme] = useState("dark");
  const location = useLocation();

  useEffect(() => {
    const savedTheme = localStorage.getItem("theme") || "dark";
    setTheme(savedTheme);
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === "dark" ? "light" : "dark";
    setTheme(newTheme);
    localStorage.setItem("theme", newTheme);
  };

  const navItems = [
    { name: "Dashboard", icon: LayoutDashboard, page: "Dashboard" },
    { name: "Positions", icon: Briefcase, page: "Positions" },
    { name: "Trade Entry", icon: PlusCircle, page: "TradeEntry" },
    { name: "Trade History", icon: History, page: "TradeHistory" },
    { name: "Reports", icon: FileBarChart, page: "Reports" },
    { name: "Settings", icon: Settings, page: "Settings" },
  ];

  const isActive = (pageName) => currentPageName === pageName;

  const isDark = theme === "dark";

  return (
    <div className={cn(
      "min-h-screen transition-colors duration-300",
      isDark ? "dark bg-slate-950 text-white" : "bg-slate-100 text-slate-900"
    )}>
      {/* Gradient background effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className={cn(
          "absolute -top-40 -right-40 w-96 h-96 rounded-full blur-3xl",
          isDark ? "bg-cyan-500/10" : "bg-cyan-500/20"
        )} />
        <div className={cn(
          "absolute top-1/2 -left-40 w-96 h-96 rounded-full blur-3xl",
          isDark ? "bg-violet-500/10" : "bg-violet-500/15"
        )} />
        <div className={cn(
          "absolute -bottom-40 right-1/3 w-96 h-96 rounded-full blur-3xl",
          isDark ? "bg-fuchsia-500/10" : "bg-fuchsia-500/15"
        )} />
      </div>

      {/* Mobile Header */}
      <header className={cn(
        "lg:hidden fixed top-0 left-0 right-0 z-50 border-b backdrop-blur-xl",
        isDark ? "border-slate-800/50 bg-slate-950/80" : "border-slate-200 bg-white/80"
      )}>
        <div className="flex items-center justify-between px-4 h-16">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 via-violet-500 to-fuchsia-500 flex items-center justify-center shadow-lg shadow-violet-500/25">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-lg bg-gradient-to-r from-cyan-400 to-violet-400 bg-clip-text text-transparent">
              Position Manager
            </span>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
              className={cn(
                "h-9 w-9",
                isDark ? "text-slate-400 hover:text-white hover:bg-slate-800" : "text-slate-600 hover:text-slate-900 hover:bg-slate-200"
              )}
            >
              {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setSidebarOpen(true)}
              className={cn(
                "h-9 w-9",
                isDark ? "text-slate-400 hover:text-white hover:bg-slate-800" : "text-slate-600 hover:text-slate-900 hover:bg-slate-200"
              )}
            >
              <Menu className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </header>

      {/* Mobile Sidebar Overlay */}
      <AnimatePresence>
        {sidebarOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-sm"
            />
            <motion.aside
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", damping: 25, stiffness: 300 }}
              className={cn(
                "lg:hidden fixed top-0 right-0 bottom-0 z-50 w-72 border-l",
                isDark ? "bg-slate-900 border-slate-800" : "bg-white border-slate-200"
              )}
            >
              <div className={cn(
                "flex items-center justify-between p-4 border-b",
                isDark ? "border-slate-800" : "border-slate-200"
              )}>
                <span className={cn("font-semibold", isDark ? "text-white" : "text-slate-900")}>Menu</span>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setSidebarOpen(false)}
                  className={isDark ? "text-slate-400 hover:text-white" : "text-slate-600 hover:text-slate-900"}
                >
                  <X className="w-5 h-5" />
                </Button>
              </div>
              <nav className="p-4 space-y-1">
                {navItems.map((item) => {
                  const Icon = item.icon;
                  return (
                    <Link
                      key={item.page}
                      to={createPageUrl(item.page)}
                      onClick={() => setSidebarOpen(false)}
                      className={cn(
                        "flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all",
                        isActive(item.page)
                          ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-600 border border-cyan-500/30"
                          : isDark 
                            ? "text-slate-400 hover:text-white hover:bg-slate-800/50"
                            : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
                      )}
                    >
                      <Icon className="w-5 h-5" />
                      {item.name}
                    </Link>
                  );
                })}
              </nav>
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      {/* Desktop Sidebar */}
      <aside className={cn(
        "hidden lg:flex flex-col fixed top-0 left-0 bottom-0 w-64 backdrop-blur-xl border-r z-40",
        isDark ? "bg-slate-900/50 border-slate-800/50" : "bg-white/70 border-slate-200"
      )}>
        {/* Logo */}
        <div className={cn(
          "flex items-center gap-3 px-6 h-16 border-b",
          isDark ? "border-slate-800/50" : "border-slate-200"
        )}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 via-violet-500 to-fuchsia-500 flex items-center justify-center shadow-lg shadow-violet-500/25">
            <TrendingUp className="w-5 h-5 text-white" />
          </div>
          <span className="font-bold text-lg bg-gradient-to-r from-cyan-400 to-violet-400 bg-clip-text text-transparent">
            Position Manager
          </span>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.page}
                to={createPageUrl(item.page)}
                className={cn(
                  "flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all",
                  isActive(item.page)
                    ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-600 border border-cyan-500/30 shadow-lg shadow-cyan-500/10"
                    : isDark 
                      ? "text-slate-400 hover:text-white hover:bg-slate-800/50"
                      : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
                )}
              >
                <Icon className="w-5 h-5" />
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className={cn("p-4 border-t", isDark ? "border-slate-800/50" : "border-slate-200")}>
          <div className="flex items-center justify-between mb-4">
            <span className={cn("text-xs", isDark ? "text-slate-500" : "text-slate-500")}>Theme</span>
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleTheme}
              className={cn(
                "h-8 gap-2",
                isDark ? "text-slate-400 hover:text-white hover:bg-slate-800" : "text-slate-600 hover:text-slate-900 hover:bg-slate-200"
              )}
            >
              {isDark ? (
                <>
                  <Sun className="w-4 h-4" />
                  Light
                </>
              ) : (
                <>
                  <Moon className="w-4 h-4" />
                  Dark
                </>
              )}
            </Button>
          </div>
          <div className={cn("flex items-center justify-between text-xs", isDark ? "text-slate-500" : "text-slate-500")}>
            <span>v1.0.0</span>
            <a 
              href="#" 
              className="flex items-center gap-1 hover:text-slate-400 transition-colors"
            >
              Docs
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className={cn(
        "lg:ml-64 min-h-screen pt-16 lg:pt-0 relative",
        isDark ? "bg-slate-950" : "bg-slate-100"
      )}>
        <div className="p-4 lg:p-8 max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
