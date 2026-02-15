import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, Dot } from "recharts";
import { TrendingDown } from "lucide-react";

export default function UnderwaterChart({ trades }) {
  // Calculate underwater curve data
  const calculateUnderwaterData = () => {
    if (!trades || trades.length === 0) return [];

    // Sort trades by exit date
    const sortedTrades = [...trades]
      .filter(t => t.exit_date)
      .sort((a, b) => new Date(a.exit_date) - new Date(b.exit_date));

    if (sortedTrades.length === 0) return [];

    const data = [];
    let runningEquity = 0;
    let peakEquity = 0;

    sortedTrades.forEach(trade => {
      runningEquity += trade.pnl;
      if (runningEquity > peakEquity) {
        peakEquity = runningEquity;
      }

      const drawdown = peakEquity === 0 ? 0 : ((runningEquity - peakEquity) / peakEquity) * 100;

      data.push({
        date: trade.exit_date,
        drawdown: drawdown,
        equity: runningEquity,
        peak: peakEquity
      });
    });

    return data;
  };

  const data = calculateUnderwaterData();

  if (data.length === 0) {
    return (
      <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm p-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 rounded-lg bg-gradient-to-br from-rose-500 to-red-600">
            <TrendingDown className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">Underwater Equity Curve</h3>
            <p className="text-sm text-slate-400">% Below Peak Equity</p>
          </div>
        </div>
        <div className="h-64 flex items-center justify-center text-slate-400">
          No trade data available
        </div>
      </div>
    );
  }

  if (data.length <= 2) {
    return (
      <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm p-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 rounded-lg bg-gradient-to-br from-rose-500 to-red-600">
            <TrendingDown className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">Underwater Equity Curve</h3>
            <p className="text-sm text-slate-400">% Below Peak Equity</p>
          </div>
        </div>
        <div className="h-64 flex items-center justify-center text-slate-400">
          Need more trades for trend analysis
        </div>
      </div>
    );
  }

  // Find max drawdown point
  const maxDrawdownPoint = data.reduce((max, curr) => 
    curr.drawdown < max.drawdown ? curr : max
  , data[0]);

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload[0]) {
      const data = payload[0].payload;
      return (
        <div className="bg-slate-900 border border-slate-700 rounded-lg p-3 shadow-xl">
          <p className="text-xs text-slate-400 mb-1">{new Date(data.date).toLocaleDateString()}</p>
          <p className="text-sm font-semibold text-rose-400">{data.drawdown.toFixed(2)}%</p>
          <p className="text-xs text-slate-400 mt-1">Current: £{data.equity.toFixed(0)}</p>
          <p className="text-xs text-slate-400">Peak: £{data.peak.toFixed(0)}</p>
        </div>
      );
    }
    return null;
  };

  const CustomDot = (props) => {
    const { cx, cy, payload } = props;
    if (payload.date === maxDrawdownPoint.date) {
      return (
        <>
          <Dot cx={cx} cy={cy} r={5} fill="#ef4444" stroke="#fff" strokeWidth={2} />
          <text x={cx} y={cy - 15} textAnchor="middle" fill="#ef4444" fontSize="11" fontWeight="600">
            Max DD
          </text>
        </>
      );
    }
    return null;
  };

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm overflow-hidden">
      <div className="p-6 border-b border-slate-700/50">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 rounded-lg bg-gradient-to-br from-rose-500 to-red-600">
            <TrendingDown className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">Underwater Equity Curve</h3>
            <p className="text-sm text-slate-400">% Below Peak Equity</p>
          </div>
        </div>
      </div>

      <div className="p-6">
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={data}>
            <defs>
              <linearGradient id="drawdownGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#dc2626" stopOpacity={0.1} />
                <stop offset="100%" stopColor="#dc2626" stopOpacity={0.4} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.3} />
            <XAxis 
              dataKey="date" 
              stroke="#64748b"
              tick={{ fill: '#94a3b8', fontSize: 12 }}
              tickFormatter={(date) => new Date(date).toLocaleDateString('en-GB', { month: 'short', day: 'numeric' })}
            />
            <YAxis 
              stroke="#64748b"
              tick={{ fill: '#94a3b8', fontSize: 12 }}
              tickFormatter={(value) => `${value.toFixed(0)}%`}
              domain={['auto', 0]}
            />
            <Tooltip content={<CustomTooltip />} />
            <ReferenceLine y={0} stroke="#334155" strokeWidth={2} />
            <Area 
              type="monotone" 
              dataKey="drawdown" 
              stroke="#dc2626" 
              strokeWidth={2}
              fill="url(#drawdownGradient)"
              dot={<CustomDot />}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
