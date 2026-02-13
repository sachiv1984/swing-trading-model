import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { Card } from "../components/ui/card";
import { Switch } from "../components/ui/switch";
import { Label } from "../components/ui/label";
import { 
  Activity, 
  RefreshCw, 
  Play, 
  CheckCircle2, 
  AlertTriangle, 
  XCircle, 
  HelpCircle,
  ChevronDown,
  Database,
  Globe,
  Server,
  Settings,
  Clock,
  Zap
} from "lucide-react";
import { cn } from "../lib/utils";
import { motion, AnimatePresence } from "framer-motion";
import moment from "moment";

export default function SystemStatus() {
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [expandedComponents, setExpandedComponents] = useState({});
  const queryClient = useQueryClient();

  // Get API URL from environment variable
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // DEBUG: Log environment info on mount
  useEffect(() => {
    console.log('=== SYSTEM STATUS DEBUG ===');
    console.log('API_URL:', API_URL);
    console.log('window.location:', window.location.href);
    console.log('All env vars:', process.env);
    console.log('==========================');
  }, [API_URL]);

  // Fetch health status
  const { data: healthData, isLoading: healthLoading, error: healthError, refetch: refetchHealth } = useQuery({
    queryKey: ['systemHealth'],
    queryFn: async () => {
      console.log(`Fetching: ${API_URL}/health/detailed`);
      const response = await fetch(`${API_URL}/health/detailed`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        mode: 'cors', // Explicitly set CORS mode
      });
      
      console.log('Health response status:', response.status);
      console.log('Health response headers:', [...response.headers.entries()]);
      
      if (!response.ok) {
        const text = await response.text();
        console.error('Health response error:', text);
        throw new Error(`HTTP ${response.status}: ${text}`);
      }
      
      const data = await response.json();
      console.log('Health data:', data);
      return data;
    },
    refetchInterval: autoRefresh ? 5000 : false,
    retry: false, // Don't retry on error
  });

  // Fetch endpoint tests
  const { data: testData, isLoading: testLoading, error: testError, mutate: runTests } = useMutation({
    mutationFn: async () => {
      console.log(`Posting to: ${API_URL}/test/endpoints`);
      const response = await fetch(`${API_URL}/test/endpoints`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        mode: 'cors',
      });
      
      console.log('Test response status:', response.status);
      
      if (!response.ok) {
        const text = await response.text();
        console.error('Test response error:', text);
        throw new Error(`HTTP ${response.status}: ${text}`);
      }
      
      const data = await response.json();
      console.log('Test data:', data);
      return data;
    }
  });

  const toggleComponentExpanded = (component) => {
    setExpandedComponents(prev => ({
      ...prev,
      [component]: !prev[component]
    }));
  };

  const overallStatus = healthData?.status || "unknown";
  const isHealthy = overallStatus === "healthy";
  const isDegraded = overallStatus === "degraded";

  const componentIcons = {
    database: Database,
    yahooFinance: Globe,
    services: Server,
    config: Settings
  };

  const statusConfig = {
    healthy: { color: "text-emerald-400", bg: "bg-emerald-500/20", border: "border-emerald-500/40", icon: CheckCircle2 },
    degraded: { color: "text-yellow-400", bg: "bg-yellow-500/20", border: "border-yellow-500/40", icon: AlertTriangle },
    unhealthy: { color: "text-rose-400", bg: "bg-rose-500/20", border: "border-rose-500/40", icon: XCircle },
    unknown: { color: "text-slate-400", bg: "bg-slate-500/20", border: "border-slate-500/40", icon: HelpCircle }
  };

  const testStatusConfig = {
    pass: { color: "text-emerald-400", bg: "bg-emerald-500/10", border: "border-emerald-500/30", icon: CheckCircle2 },
    fail: { color: "text-rose-400", bg: "bg-rose-500/10", border: "border-rose-500/30", icon: XCircle },
    error: { color: "text-yellow-400", bg: "bg-yellow-500/10", border: "border-yellow-500/30", icon: AlertTriangle }
  };

  const successRate = testData ? ((testData.passed / testData.totalTests) * 100).toFixed(1) : 0;

  return (
    <div className="space-y-6">
      {/* DEBUG INFO CARD */}
      <div className="p-4 rounded-lg bg-blue-500/10 border border-blue-500/30 text-blue-300 text-sm font-mono">
        <div className="font-bold mb-2">🔍 Debug Info:</div>
        <div>API URL: {API_URL}</div>
        <div>Current Location: {window.location.href}</div>
        <div>Health Error: {healthError?.message || 'None'}</div>
        <div>Test Error: {testError?.message || 'None'}</div>
      </div>

      {/* Page Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-violet-400 bg-clip-text text-transparent">
            System Status
          </h1>
          <p className="text-slate-400 mt-1">Monitor system health and test API endpoints</p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-slate-800/50 border border-slate-700/50">
            <Switch
              checked={autoRefresh}
              onCheckedChange={setAutoRefresh}
              id="auto-refresh"
            />
            <Label htmlFor="auto-refresh" className="text-sm text-slate-300 cursor-pointer">
              Auto-refresh
            </Label>
          </div>
          <Button
            onClick={() => refetchHealth()}
            disabled={healthLoading}
            className="bg-slate-800 hover:bg-slate-700 border border-slate-700"
          >
            <RefreshCw className={cn("w-4 h-4 mr-2", healthLoading && "animate-spin")} />
            Refresh Health
          </Button>
          <Button
            onClick={() => runTests()}
            disabled={testLoading}
            className="bg-gradient-to-r from-cyan-600 to-violet-600 hover:from-cyan-500 hover:to-violet-500"
          >
            <Play className="w-4 h-4 mr-2" />
            Run Tests
          </Button>
        </div>
      </div>

      {/* Show error if fetch failed */}
      {healthError && (
        <div className="p-4 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300">
          <div className="font-bold mb-2">❌ Health Check Failed:</div>
          <div className="text-sm">{healthError.message}</div>
          <div className="text-xs mt-2 opacity-70">
            This usually means CORS is blocking the request or the backend is not running.
          </div>
        </div>
      )}

      {/* Overall Status Hero Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className={cn(
          "p-8 rounded-2xl border-2 backdrop-blur-sm",
          isHealthy && "bg-gradient-to-br from-emerald-500/20 to-emerald-600/10 border-emerald-500/40",
          isDegraded && "bg-gradient-to-br from-yellow-500/20 to-yellow-600/10 border-yellow-500/40",
          !isHealthy && !isDegraded && "bg-gradient-to-br from-slate-500/20 to-slate-600/10 border-slate-500/40"
        )}
      >
        {healthLoading ? (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <RefreshCw className="w-12 h-12 text-slate-400 animate-spin mx-auto mb-4" />
              <p className="text-slate-400">Loading system status...</p>
            </div>
          </div>
        ) : (
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
            <div className="flex items-center gap-6">
              <div className={cn(
                "w-20 h-20 rounded-2xl flex items-center justify-center",
                isHealthy && "bg-emerald-500/30",
                isDegraded && "bg-yellow-500/30",
                !isHealthy && !isDegraded && "bg-slate-500/30"
              )}>
                {isHealthy && <CheckCircle2 className="w-12 h-12 text-emerald-400" />}
                {isDegraded && <AlertTriangle className="w-12 h-12 text-yellow-400" />}
                {!isHealthy && !isDegraded && <Activity className="w-12 h-12 text-slate-400" />}
              </div>
              <div>
                <h2 className={cn(
                  "text-4xl font-bold mb-2",
                  isHealthy && "text-emerald-400",
                  isDegraded && "text-yellow-400",
                  !isHealthy && !isDegraded && "text-slate-400"
                )}>
                  {isHealthy && "Healthy"}
                  {isDegraded && "Degraded"}
                  {!isHealthy && !isDegraded && "Unknown"}
                </h2>
                <p className="text-slate-300 text-lg">
                  {isHealthy && "System is operating normally"}
                  {isDegraded && "System is experiencing issues"}
                  {!isHealthy && !isDegraded && "System status unknown"}
                </p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-700/50">
                <div className="flex items-center gap-2 text-slate-400 text-sm mb-1">
                  <Zap className="w-4 h-4" />
                  Response Time
                </div>
                <p className="text-2xl font-bold text-white">
                  {healthData?.responseTime?.toFixed(1) || "0.0"}ms
                </p>
              </div>
              <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-700/50">
                <div className="flex items-center gap-2 text-slate-400 text-sm mb-1">
                  <Clock className="w-4 h-4" />
                  Last Updated
                </div>
                <p className="text-sm font-medium text-white">
                  {healthData?.timestamp ? moment(healthData.timestamp).fromNow() : "Never"}
                </p>
              </div>
            </div>
          </div>
        )}
      </motion.div>

      {/* Component Health Checks */}
      <div>
        <h2 className="text-xl font-bold text-white mb-4">Component Health Checks</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {healthData?.components && Object.entries(healthData.components).map(([key, component]) => {
            const Icon = componentIcons[key] || Server;
            const config = statusConfig[component.status] || statusConfig.unknown;
            const StatusIcon = config.icon;
            const isExpanded = expandedComponents[key];

            return (
              <motion.div
                key={key}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={cn(
                  "p-5 rounded-xl border backdrop-blur-sm",
                  config.bg,
                  config.border
                )}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className={cn("p-2 rounded-lg bg-slate-900/40")}>
                      <Icon className="w-5 h-5 text-slate-300" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-white capitalize">
                        {key.replace(/([A-Z])/g, ' $1').trim()}
                      </h3>
                      <Badge className={cn("mt-1 border", config.color, config.border)}>
                        <StatusIcon className="w-3 h-3 mr-1" />
                        {component.status}
                      </Badge>
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => toggleComponentExpanded(key)}
                    className="text-slate-400 hover:text-white"
                  >
                    <ChevronDown className={cn(
                      "w-4 h-4 transition-transform",
                      isExpanded && "rotate-180"
                    )} />
                  </Button>
                </div>

                <AnimatePresence>
                  {isExpanded && component.details && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mt-3 pt-3 border-t border-slate-700/50"
                    >
                      <pre className="text-xs text-slate-300 bg-slate-900/60 p-3 rounded-lg overflow-x-auto">
                        {JSON.stringify(component.details, null, 2)}
                      </pre>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Endpoint Tests Section */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-white">Endpoint Tests</h2>
          {testData && (
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2 text-sm">
                <span className="text-slate-400">Total:</span>
                <span className="font-bold text-white">{testData.totalTests}</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span className="text-slate-400">Passed:</span>
                <span className="font-bold text-emerald-400">{testData.passed}</span>
              </div>
              {testData.failed > 0 && (
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-slate-400">Failed:</span>
                  <span className="font-bold text-rose-400">{testData.failed}</span>
                </div>
              )}
              {testData.errors > 0 && (
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-slate-400">Errors:</span>
                  <span className="font-bold text-yellow-400">{testData.errors}</span>
                </div>
              )}
              <div className="flex items-center gap-2 text-sm">
                <span className="text-slate-400">Success Rate:</span>
                <span className="font-bold text-white">{successRate}%</span>
              </div>
            </div>
          )}
        </div>

        {testLoading ? (
          <div className="flex items-center justify-center py-12 bg-slate-800/30 rounded-xl border border-slate-700/50">
            <div className="text-center">
              <RefreshCw className="w-10 h-10 text-slate-400 animate-spin mx-auto mb-3" />
              <p className="text-slate-400">Running endpoint tests...</p>
              <p className="text-slate-500 text-sm mt-1">This may take 10-30 seconds</p>
            </div>
          </div>
        ) : !testData ? (
          <div className="flex items-center justify-center py-12 bg-slate-800/30 rounded-xl border border-slate-700/50">
            <div className="text-center">
              <Play className="w-10 h-10 text-slate-400 mx-auto mb-3" />
              <p className="text-slate-400">Click 'Run Tests' to verify all endpoints</p>
            </div>
          </div>
        ) : (
          <div className="space-y-2">
            {testData.tests?.map((test, index) => {
              const config = testStatusConfig[test.status] || testStatusConfig.error;
              const StatusIcon = config.icon;

              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className={cn(
                    "p-4 rounded-lg border flex items-center justify-between",
                    config.bg,
                    config.border
                  )}
                >
                  <div className="flex items-center gap-4 flex-1">
                    <StatusIcon className={cn("w-5 h-5", config.color)} />
                    <div className="flex-1">
                      <p className="font-medium text-white">{test.endpoint}</p>
                      {test.error && (
                        <p className="text-sm text-slate-400 mt-1 truncate max-w-md">
                          {test.error}
                        </p>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    {test.statusCode && (
                      <Badge variant="outline" className="text-slate-300">
                        {test.statusCode}
                      </Badge>
                    )}
                    {test.responseTime && (
                      <div className="text-right">
                        <p className="text-sm text-slate-400">Response Time</p>
                        <p className="font-bold text-white">{test.responseTime}ms</p>
                      </div>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
