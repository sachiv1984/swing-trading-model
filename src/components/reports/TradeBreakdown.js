import { useMemo } from "react";
import { motion } from "framer-motion";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";

const COLORS = ['#22d3ee', '#a78bfa', '#f472b6', '#34d399', '#fbbf24', '#f87171'];

export default function TradeBreakdown({ positions }) {
  const breakdownData = useMemo(() => {
    const closedPositions = positions.filter(p => p.status === "closed");
    
    // By market
    const byMarket = {};
    closedPositions.forEach(p => {
      const market = p.market || "Unknown";
      if (!byMarket[market]) {
        byMarket[market] = { trades: 0, pnl: 0 };
      }
      byMarket[market].trades += 1;
      byMarket[market].pnl += p.pnl || 0;
    });

    // By exit reason
    const byReason = {};
    closedPositions.forEach(p => {
      const reason = p.exit_reason || "unknown";
      if (!byReason[reason]) {
        byReason[reason] = { trades: 0, pnl: 0 };
      }
      byReason[reason].trades += 1;
      byReason[reason].pnl += p.pnl || 0;
    });

    const marketData = Object.entries(byMarket).map(([name, data]) => ({
      name,
      value: data.trades,
      pnl: data.pnl
    }));

    const reasonLabels = {
      stop_hit: "Stop Hit",
      manual: "Manual",
      target: "Target",
      market_regime: "Market Regime",
      unknown: "Unknown"
    };

    const reasonData = Object.entries(byReason).map(([name, data]) => ({
      name: reasonLabels[name] || name,
      value: data.trades,
      pnl: data.pnl
    }));

    return { marketData, reasonData };
  }, [positions]);

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-3 shadow-xl">
          <p className="text-white font-medium">{data.name}</p>
          <p className="text-slate-400 text-sm">{data.value} trades</p>
          <p className={`text-sm ${data.pnl >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
            £{data.pnl.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-6"
    >
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white">Trade Breakdown</h3>
        <p className="text-sm text-slate-400">Analysis by market and exit reason</p>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* By Market */}
        <div>
          <h4 className="text-sm font-medium text-slate-300 mb-3 text-center">By Market</h4>
          <div className="h-40">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={breakdownData.marketData}
                  cx="50%"
                  cy="50%"
                  innerRadius={30}
                  outerRadius={55}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {breakdownData.marketData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center gap-4 mt-2">
            {breakdownData.marketData.map((item, idx) => (
              <div key={idx} className="flex items-center gap-1.5">
                <div 
                  className="w-2.5 h-2.5 rounded-full" 
                  style={{ backgroundColor: COLORS[idx % COLORS.length] }}
                />
                <span className="text-xs text-slate-400">{item.name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* By Exit Reason */}
        <div>
          <h4 className="text-sm font-medium text-slate-300 mb-3 text-center">By Exit Reason</h4>
          <div className="h-40">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={breakdownData.reasonData}
                  cx="50%"
                  cy="50%"
                  innerRadius={30}
                  outerRadius={55}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {breakdownData.reasonData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[(index + 2) % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex flex-wrap justify-center gap-3 mt-2">
            {breakdownData.reasonData.map((item, idx) => (
              <div key={idx} className="flex items-center gap-1.5">
                <div 
                  className="w-2.5 h-2.5 rounded-full" 
                  style={{ backgroundColor: COLORS[(idx + 2) % COLORS.length] }}
                />
                <span className="text-xs text-slate-400">{item.name}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
