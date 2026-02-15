import { useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { TrendingUp, ChevronDown, ChevronUp, ArrowUpDown } from "lucide-react";
import { Badge } from "../ui/badge";

export default function RMultipleAnalysis({ trades }) {
  const [expandedTags, setExpandedTags] = useState(false);
  const [tagSortBy, setTagSortBy] = useState("avgR");
  const [tagSortDir, setTagSortDir] = useState("desc");

  // Calculate R-multiple for each trade
  const calculateRMultiples = () => {
    return trades
      .filter(t => t.stop_price && t.entry_price && t.exit_price)
      .map(t => {
        const risk = Math.abs(t.entry_price - t.stop_price);
        const pnl = t.exit_price - t.entry_price;
        const rMultiple = risk === 0 ? 0 : pnl / risk;
        return { ...t, rMultiple };
      });
  };

  const tradesWithR = calculateRMultiples();

  // Check if we have valid data
  if (tradesWithR.length === 0) {
    return (
      <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm p-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-600">
            <TrendingUp className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">R-Multiple Analysis</h3>
            <p className="text-sm text-slate-400">Risk-adjusted returns</p>
          </div>
        </div>
        <div className="mt-4 p-4 bg-amber-500/10 border border-amber-500/30 rounded-lg">
          <p className="text-sm text-amber-400">R-Multiple requires stop prices to be defined for all trades</p>
        </div>
      </div>
    );
  }

  if (tradesWithR.length < 10) {
    return (
      <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm p-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-600">
            <TrendingUp className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">R-Multiple Analysis</h3>
            <p className="text-sm text-slate-400">Risk-adjusted returns</p>
          </div>
        </div>
        <div className="mt-4 p-4 bg-amber-500/10 border border-amber-500/30 rounded-lg">
          <p className="text-sm text-amber-400">Need 10+ trades for meaningful R-Multiple analysis ({tradesWithR.length} trades found)</p>
        </div>
      </div>
    );
  }

  // Calculate distribution
  const buckets = [
    { label: "-3R+", min: -Infinity, max: -2, count: 0 },
    { label: "-2R to -1R", min: -2, max: -1, count: 0 },
    { label: "-1R to 0R", min: -1, max: 0, count: 0 },
    { label: "0R to 1R", min: 0, max: 1, count: 0 },
    { label: "1R to 2R", min: 1, max: 2, count: 0 },
    { label: "2R to 3R", min: 2, max: 3, count: 0 },
    { label: "3R+", min: 3, max: Infinity, count: 0 }
  ];

  tradesWithR.forEach(t => {
    const bucket = buckets.find(b => t.rMultiple >= b.min && t.rMultiple < b.max);
    if (bucket) bucket.count++;
  });

  // Calculate statistics
  const avgR = tradesWithR.reduce((sum, t) => sum + t.rMultiple, 0) / tradesWithR.length;
  const winners = tradesWithR.filter(t => t.rMultiple > 0);
  const losers = tradesWithR.filter(t => t.rMultiple <= 0);
  const avgWinner = winners.length > 0 ? winners.reduce((sum, t) => sum + t.rMultiple, 0) / winners.length : 0;
  const avgLoser = losers.length > 0 ? losers.reduce((sum, t) => sum + t.rMultiple, 0) / losers.length : 0;
  const bestTrade = tradesWithR.reduce((max, t) => t.rMultiple > max.rMultiple ? t : max);
  const worstTrade = tradesWithR.reduce((min, t) => t.rMultiple < min.rMultiple ? t : min);
  const winRate = (winners.length / tradesWithR.length) * 100;

  // Calculate tag performance
  const calculateTagData = () => {
    const tagMap = {};
    tradesWithR.forEach(trade => {
      if (trade.tags && Array.isArray(trade.tags)) {
        trade.tags.forEach(tag => {
          if (!tagMap[tag]) {
            tagMap[tag] = { count: 0, totalR: 0, wins: 0 };
          }
          tagMap[tag].count += 1;
          tagMap[tag].totalR += trade.rMultiple;
          if (trade.rMultiple > 0) tagMap[tag].wins += 1;
        });
      }
    });

    return Object.entries(tagMap).map(([tag, data]) => ({
      tag,
      avgR: data.totalR / data.count,
      count: data.count,
      winRate: (data.wins / data.count) * 100
    }));
  };

  const tagData = calculateTagData();
  const sortedTagData = [...tagData].sort((a, b) => {
    let comparison = 0;
    if (tagSortBy === "avgR") comparison = a.avgR - b.avgR;
    else if (tagSortBy === "count") comparison = a.count - b.count;
    else if (tagSortBy === "winRate") comparison = a.winRate - b.winRate;
    return tagSortDir === "desc" ? -comparison : comparison;
  });

  const handleTagSort = (column) => {
    if (tagSortBy === column) {
      setTagSortDir(tagSortDir === "desc" ? "asc" : "desc");
    } else {
      setTagSortBy(column);
      setTagSortDir("desc");
    }
  };

  const getBarColor = (label) => {
    if (label.includes("-3R") || label === "-2R to -1R") return "#ef4444";
    if (label === "-1R to 0R") return "#f97316";
    if (label === "0R to 1R") return "#64748b";
    if (label === "1R to 2R") return "#06b6d4";
    if (label === "2R to 3R") return "#10b981";
    return "#059669";
  };

  const getAvgRColor = (r) => {
    if (r >= 1) return "text-emerald-400";
    if (r >= 0.5) return "text-amber-400";
    return "text-slate-400";
  };

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm overflow-hidden">
      <div className="p-6 border-b border-slate-700/50">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-600">
            <TrendingUp className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">R-Multiple Analysis</h3>
            <p className="text-sm text-slate-400">Risk-adjusted return distribution</p>
          </div>
        </div>
      </div>

      <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Distribution Chart */}
        <div>
          <h4 className="text-sm font-medium text-slate-400 mb-4">Distribution</h4>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={buckets}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.3} />
              <XAxis 
                dataKey="label" 
                stroke="#64748b"
                tick={{ fill: '#94a3b8', fontSize: 11 }}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis 
                stroke="#64748b"
                tick={{ fill: '#94a3b8', fontSize: 12 }}
              />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                labelStyle={{ color: '#e2e8f0' }}
              />
              <Bar dataKey="count" label={{ position: 'top', fill: '#94a3b8', fontSize: 11 }}>
                {buckets.map((entry, index) => (
                  <Cell key={index} fill={getBarColor(entry.label)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Statistics Grid */}
        <div>
          <h4 className="text-sm font-medium text-slate-400 mb-4">Statistics</h4>
          <div className="grid grid-cols-2 gap-4">
            {/* Average R */}
            <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/30">
              <div className={`text-3xl font-bold ${getAvgRColor(avgR)}`}>
                {avgR.toFixed(2)}R
              </div>
              <div className="text-xs text-slate-500 mt-1">Per trade</div>
            </div>

            {/* Best Trade */}
            <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/30">
              <div className="text-3xl font-bold text-emerald-400">
                {bestTrade.rMultiple.toFixed(1)}R
              </div>
              <div className="text-xs text-slate-500 mt-1">Max R • {bestTrade.ticker}</div>
            </div>

            {/* Worst Trade */}
            <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/30">
              <div className="text-3xl font-bold text-rose-400">
                {worstTrade.rMultiple.toFixed(1)}R
              </div>
              <div className="text-xs text-slate-500 mt-1">Max loss • {worstTrade.ticker}</div>
            </div>

            {/* Win Rate */}
            <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/30">
              <div className="text-3xl font-bold text-cyan-400">
                {winRate.toFixed(0)}%
              </div>
              <div className="text-xs text-slate-500 mt-1">Profitable trades</div>
            </div>

            {/* Avg Winner */}
            <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/30">
              <div className="text-3xl font-bold text-emerald-400">
                {avgWinner.toFixed(1)}R
              </div>
              <div className="text-xs text-slate-500 mt-1">When profitable</div>
            </div>

            {/* Avg Loser */}
            <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/30">
              <div className="text-3xl font-bold text-rose-400">
                {avgLoser.toFixed(1)}R
              </div>
              <div className="text-xs text-slate-500 mt-1">When stopped</div>
            </div>
          </div>
        </div>
      </div>

      {/* R-Multiple by Tag */}
      {tagData.length > 0 && (
        <div className="border-t border-slate-700/50">
          <button
            onClick={() => setExpandedTags(!expandedTags)}
            className="w-full p-4 flex items-center justify-between hover:bg-slate-800/30 transition-colors"
          >
            <span className="text-sm font-medium text-slate-300">R-Multiple by Tag</span>
            {expandedTags ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
          </button>
          
          {expandedTags && (
            <div className="px-4 pb-4">
              <table className="w-full">
                <thead className="bg-slate-800/50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Tag</th>
                    <th 
                      className="px-4 py-3 text-right text-xs font-medium text-slate-400 uppercase cursor-pointer hover:text-slate-300"
                      onClick={() => handleTagSort("avgR")}
                    >
                      <div className="flex items-center justify-end gap-1">
                        Avg R
                        <ArrowUpDown className="w-3 h-3" />
                      </div>
                    </th>
                    <th 
                      className="px-4 py-3 text-right text-xs font-medium text-slate-400 uppercase cursor-pointer hover:text-slate-300"
                      onClick={() => handleTagSort("count")}
                    >
                      <div className="flex items-center justify-end gap-1">
                        Count
                        <ArrowUpDown className="w-3 h-3" />
                      </div>
                    </th>
                    <th 
                      className="px-4 py-3 text-right text-xs font-medium text-slate-400 uppercase cursor-pointer hover:text-slate-300"
                      onClick={() => handleTagSort("winRate")}
                    >
                      <div className="flex items-center justify-end gap-1">
                        Win Rate
                        <ArrowUpDown className="w-3 h-3" />
                      </div>
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700/30">
                  {sortedTagData.map((item, idx) => (
                    <tr key={idx} className="hover:bg-slate-800/20">
                      <td className="px-4 py-3">
                        <Badge className="bg-violet-500/20 text-violet-300 border-violet-500/30">
                          {item.tag}
                        </Badge>
                      </td>
                      <td className={`px-4 py-3 text-right text-sm font-medium ${getAvgRColor(item.avgR)}`}>
                        {item.avgR.toFixed(2)}R
                      </td>
                      <td className="px-4 py-3 text-right text-sm text-slate-300">
                        {item.count}
                      </td>
                      <td className="px-4 py-3 text-right text-sm text-slate-300">
                        {item.winRate.toFixed(0)}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
