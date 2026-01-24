import { useMemo } from "react";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, ReferenceLine } from "recharts";
import { motion } from "framer-motion";

export default function PortfolioGrowthChart({ positions, period, periodDates }) {
  const chartData = useMemo(() => {
    if (!positions || positions.length === 0) {
      return generateEmptyData(periodDates);
    }

    // Group trades by date and calculate cumulative P&L
    const tradesByDate = {};
    const closedPositions = positions.filter(p => p.status === "closed" && p.exit_date);
    
    closedPositions.forEach(p => {
      const date = p.exit_date;
      if (!tradesByDate[date]) {
        tradesByDate[date] = { pnl: 0, trades: 0 };
      }
      tradesByDate[date].pnl += p.pnl || 0;
      tradesByDate[date].trades += 1;
    });

    // Create daily data points
    const data = [];
    let cumulativePnL = 0;
    let cumulativeTrades = 0;
    
    const start = new Date(periodDates.start);
    const end = new Date(periodDates.end);
    
    for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
      const dateStr = d.toISOString().split('T')[0];
      
      if (tradesByDate[dateStr]) {
        cumulativePnL += tradesByDate[dateStr].pnl;
        cumulativeTrades += tradesByDate[dateStr].trades;
      }
      
      data.push({
        date: d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short' }),
        fullDate: dateStr,
        pnl: Math.round(cumulativePnL * 100) / 100,
        trades: cumulativeTrades
      });
    }

    // Reduce data points for longer periods
    if (data.length > 60) {
      const step = Math.ceil(data.length / 60);
      return data.filter((_, idx) => idx % step === 0 || idx === data.length - 1);
    }

    return data;
  }, [positions, periodDates]);

  const maxPnL = Math.max(...chartData.map(d => d.pnl), 0);
  const minPnL = Math.min(...chartData.map(d => d.pnl), 0);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-6"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-white">Portfolio Growth</h3>
          <p className="text-sm text-slate-400">Cumulative P&L over time</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-gradient-to-r from-cyan-400 to-violet-400" />
            <span className="text-xs text-slate-400">Cumulative P&L</span>
          </div>
        </div>
      </div>

      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="pnlGradientPositive" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#22d3ee" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="pnlGradientNegative" x1="0" y1="1" x2="0" y2="0">
                <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#f43f5e" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
            <XAxis
              dataKey="date"
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 11 }}
              interval="preserveStartEnd"
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 11 }}
              tickFormatter={(value) => `£${value >= 1000 ? `${(value / 1000).toFixed(1)}k` : value.toFixed(0)}`}
              domain={[minPnL - Math.abs(minPnL) * 0.1, maxPnL + Math.abs(maxPnL) * 0.1]}
            />
            <ReferenceLine y={0} stroke="#475569" strokeDasharray="3 3" />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #334155',
                borderRadius: '12px',
                boxShadow: '0 25px 50px -12px rgb(0 0 0 / 0.5)'
              }}
              labelStyle={{ color: '#94a3b8' }}
              formatter={(value, name) => {
                if (name === 'pnl') {
                  return [`£${value.toLocaleString(undefined, { minimumFractionDigits: 2 })}`, 'P&L'];
                }
                return [value, name];
              }}
            />
            <Area
              type="monotone"
              dataKey="pnl"
              stroke="url(#strokeGradient)"
              strokeWidth={2}
              fill="url(#pnlGradientPositive)"
              name="pnl"
            />
            <defs>
              <linearGradient id="strokeGradient" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#22d3ee" />
                <stop offset="100%" stopColor="#a78bfa" />
              </linearGradient>
            </defs>
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </motion.div>
  );
}

function generateEmptyData(periodDates) {
  const data = [];
  const start = new Date(periodDates.start);
  const end = new Date(periodDates.end);
  
  for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
    data.push({
      date: d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short' }),
      fullDate: d.toISOString().split('T')[0],
      pnl: 0,
      trades: 0
    });
  }
  
  // Reduce data points for longer periods
  if (data.length > 60) {
    const step = Math.ceil(data.length / 60);
    return data.filter((_, idx) => idx % step === 0 || idx === data.length - 1);
  }
  
  return data;
}
