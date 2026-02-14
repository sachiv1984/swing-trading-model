import { useState } from "react";
import { ArrowUpDown, TrendingUp } from "lucide-react";
import { Badge } from "../ui/badge";

export default function TagPerformance({ trades }) {
  const [sortBy, setSortBy] = useState("pnl");
  const [sortDir, setSortDir] = useState("desc");

  // Extract and calculate tag performance
  const calculateTagData = () => {
    const tagMap = {};
    
    trades.forEach(trade => {
      if (trade.tags && Array.isArray(trade.tags)) {
        trade.tags.forEach(tag => {
          if (!tagMap[tag]) {
            tagMap[tag] = { count: 0, wins: 0, totalPnl: 0 };
          }
          tagMap[tag].count += 1;
          tagMap[tag].totalPnl += trade.pnl;
          if (trade.pnl > 0) tagMap[tag].wins += 1;
        });
      }
    });

    return Object.entries(tagMap).map(([tag, data]) => ({
      tag,
      count: data.count,
      wins: data.wins,
      totalPnl: data.totalPnl,
      winRate: (data.wins / data.count) * 100,
      avgPnl: data.totalPnl / data.count
    }));
  };

  const tagData = calculateTagData();

  // Return null if no tags
  if (tagData.length === 0) return null;

  // Sort data
  const sortedData = [...tagData].sort((a, b) => {
    let comparison = 0;
    if (sortBy === "pnl") comparison = a.totalPnl - b.totalPnl;
    else if (sortBy === "winRate") comparison = a.winRate - b.winRate;
    else if (sortBy === "count") comparison = a.count - b.count;
    return sortDir === "desc" ? -comparison : comparison;
  });

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortDir(sortDir === "desc" ? "asc" : "desc");
    } else {
      setSortBy(column);
      setSortDir("desc");
    }
  };

  const getWinRateColor = (rate) => {
    if (rate >= 60) return "bg-emerald-500/20 text-emerald-400";
    if (rate >= 50) return "bg-cyan-500/20 text-cyan-400";
    return "bg-slate-500/20 text-slate-400";
  };

  // Best tag insight
  const bestTag = sortedData[0];
  const metricLabels = {
    pnl: `highest total P&L (£${bestTag.totalPnl.toFixed(0)})`,
    winRate: `best win rate (${bestTag.winRate.toFixed(0)}%)`,
    count: `most trades`
  };

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm overflow-hidden">
      <div className="p-6 border-b border-slate-700/50">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 rounded-lg bg-gradient-to-br from-violet-500 to-purple-500">
            <TrendingUp className="w-5 h-5 text-white" />
          </div>
          <h3 className="text-lg font-semibold text-white">Performance by Strategy Tag</h3>
        </div>
        <p className="text-sm text-slate-400">Analyze which strategies are working best</p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-slate-800/50 border-b border-slate-700/50">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                Tag
              </th>
              <th
                className="px-6 py-4 text-right text-xs font-medium text-slate-400 uppercase tracking-wider cursor-pointer hover:text-slate-300 transition-colors"
                onClick={() => handleSort("count")}
              >
                <div className="flex items-center justify-end gap-1">
                  Count
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th
                className="px-6 py-4 text-right text-xs font-medium text-slate-400 uppercase tracking-wider cursor-pointer hover:text-slate-300 transition-colors"
                onClick={() => handleSort("winRate")}
              >
                <div className="flex items-center justify-end gap-1">
                  Win Rate
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th
                className="px-6 py-4 text-right text-xs font-medium text-slate-400 uppercase tracking-wider cursor-pointer hover:text-slate-300 transition-colors"
                onClick={() => handleSort("pnl")}
              >
                <div className="flex items-center justify-end gap-1">
                  Total P&L
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th className="px-6 py-4 text-right text-xs font-medium text-slate-400 uppercase tracking-wider">
                Avg P&L
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/30">
            {sortedData.map((item, idx) => (
              <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                <td className="px-6 py-4">
                  <Badge className="bg-violet-500/20 text-violet-300 border-violet-500/30">
                    {item.tag}
                  </Badge>
                </td>
                <td className="px-6 py-4 text-right text-sm text-slate-300">
                  {item.count}
                </td>
                <td className="px-6 py-4 text-right">
                  <Badge className={getWinRateColor(item.winRate)}>
                    {item.winRate.toFixed(0)}%
                  </Badge>
                </td>
                <td className={`px-6 py-4 text-right text-sm font-medium ${item.totalPnl >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                  {item.totalPnl >= 0 ? '+' : ''}£{item.totalPnl.toFixed(0)}
                </td>
                <td className={`px-6 py-4 text-right text-sm font-medium ${item.avgPnl >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                  {item.avgPnl >= 0 ? '+' : ''}£{item.avgPnl.toFixed(0)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="p-4 bg-slate-800/30 border-t border-slate-700/50">
        <p className="text-sm text-slate-400">
          Your <span className="text-violet-400 font-semibold">'{bestTag.tag}'</span> strategy has the {metricLabels[sortBy]} with {bestTag.count} trades.
        </p>
      </div>
    </div>
  );
}
