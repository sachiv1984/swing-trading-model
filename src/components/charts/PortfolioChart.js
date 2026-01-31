import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";
import { base44 } from "../../api/base44Client";
import { Loader2 } from "lucide-react";

export default function PortfolioChart() {
  const { data: historyData, isLoading } = useQuery({
    queryKey: ["portfolioHistory"],
    queryFn: () => base44.entities.Portfolio.getHistory(30),
    refetchInterval: false, // Only fetch once per page load
  });

  // Format data for the chart
  const chartData = historyData?.length > 0 
    ? historyData.map(snapshot => ({
        date: new Date(snapshot.date).toLocaleDateString('en-GB', { 
          day: '2-digit', 
          month: 'short' 
        }),
        value: Math.round(snapshot.total_value),
        pnl: Math.round(snapshot.total_pnl),
        positions: Math.round(snapshot.positions_value),
        cash: Math.round(snapshot.cash_balance)
      }))
    : generateSampleData(); // Fallback to sample data if no history

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-6"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-white">Portfolio Performance</h3>
          <p className="text-sm text-slate-400">
            {historyData?.length > 0 
              ? `Last ${historyData.length} days` 
              : "Sample data - create snapshots to see real history"}
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-cyan-400" />
            <span className="text-xs text-slate-400">Value</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-violet-400" />
            <span className="text-xs text-slate-400">P&L</span>
          </div>
        </div>
      </div>
      
      {isLoading ? (
        <div className="h-64 flex items-center justify-center">
          <Loader2 className="w-8 h-8 animate-spin text-slate-500" />
        </div>
      ) : (
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="valueGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#22d3ee" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="pnlGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#a78bfa" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#a78bfa" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
              <XAxis 
                dataKey="date" 
                axisLine={false} 
                tickLine={false}
                tick={{ fill: '#64748b', fontSize: 12 }}
              />
              <YAxis 
                axisLine={false} 
                tickLine={false}
                tick={{ fill: '#64748b', fontSize: 12 }}
                tickFormatter={(value) => `£${(value / 1000).toFixed(0)}k`}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1e293b', 
                  border: '1px solid #334155',
                  borderRadius: '12px',
                  boxShadow: '0 25px 50px -12px rgb(0 0 0 / 0.5)'
                }}
                labelStyle={{ color: '#94a3b8' }}
                itemStyle={{ color: '#f1f5f9' }}
                formatter={(value, name) => {
                  const label = name === 'value' ? 'Value' : name === 'pnl' ? 'P&L' : name;
                  return [`£${value.toLocaleString()}`, label];
                }}
              />
              <Area
                type="monotone"
                dataKey="value"
                stroke="#22d3ee"
                strokeWidth={2}
                fill="url(#valueGradient)"
                name="value"
              />
              <Area
                type="monotone"
                dataKey="pnl"
                stroke="#a78bfa"
                strokeWidth={2}
                fill="url(#pnlGradient)"
                name="pnl"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}
    </motion.div>
  );
}

function generateSampleData() {
  const data = [];
  let value = 5000;
  let pnl = 0;
  
  for (let i = 30; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    
    const change = (Math.random() - 0.45) * 100;
    value += change;
    pnl += change;
    
    data.push({
      date: date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short' }),
      value: Math.round(value),
      pnl: Math.round(pnl)
    });
  }
  
  return data;
}
