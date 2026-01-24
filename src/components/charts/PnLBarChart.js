import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from "recharts";
import { motion } from "framer-motion";

export default function PnLBarChart({ trades }) {
  const data = trades?.slice(0, 10).map(t => ({
    ticker: t.ticker,
    pnl: t.pnl || 0,
    isProfit: (t.pnl || 0) >= 0
  })) || [];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-6"
    >
      <h3 className="text-lg font-semibold text-white mb-2">Trade P&L</h3>
      <p className="text-sm text-slate-400 mb-6">Recent closed positions</p>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <XAxis 
              dataKey="ticker" 
              axisLine={false} 
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 11 }}
            />
            <YAxis 
              axisLine={false} 
              tickLine={false}
              tick={{ fill: '#64748b', fontSize: 12 }}
              tickFormatter={(value) => `£${value}`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #334155',
                borderRadius: '12px'
              }}
              formatter={(value) => [`£${value.toLocaleString()}`, 'P&L']}
              cursor={{ fill: 'rgba(148, 163, 184, 0.1)' }}
            />
            <ReferenceLine y={0} stroke="#475569" />
            <Bar dataKey="pnl" radius={[6, 6, 0, 0]}>
              {data.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={entry.isProfit ? '#4ade80' : '#f87171'}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </motion.div>
  );
}
