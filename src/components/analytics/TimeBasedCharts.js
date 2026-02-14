import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ScatterChart, Scatter, ReferenceLine, Line, ComposedChart } from "recharts";

export default function TimeBasedCharts({ dayOfWeekData, monthlyData, holdingPeriodData, entryExitData }) {
  const [activeTab, setActiveTab] = useState("day");

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm">
      <h3 className="text-lg font-semibold text-white mb-6">Time-Based Analysis</h3>
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-slate-900/50 mb-6">
          <TabsTrigger value="day">Day of Week</TabsTrigger>
          <TabsTrigger value="month">Monthly</TabsTrigger>
          <TabsTrigger value="holding">Holding Period</TabsTrigger>
          <TabsTrigger value="entry">Entry Analysis</TabsTrigger>
        </TabsList>

        <TabsContent value="day" className="space-y-4">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={dayOfWeekData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="day" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                labelStyle={{ color: '#f8fafc' }}
              />
              <ReferenceLine y={0} stroke="#64748b" />
              <Bar dataKey="avgPnl" fill="#06b6d4" name="Avg P&L" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
          <div className="grid grid-cols-5 gap-2 text-xs text-center">
            {dayOfWeekData.map((day, idx) => (
              <div key={idx} className="p-2 bg-slate-900/50 rounded-lg">
                <p className="text-slate-400">{day.day}</p>
                <p className="text-white font-semibold">{day.trades} trades</p>
              </div>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="month" className="space-y-4">
          <ResponsiveContainer width="100%" height={300}>
            <ComposedChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="month" stroke="#94a3b8" angle={-45} textAnchor="end" height={80} />
              <YAxis yAxisId="left" stroke="#94a3b8" />
              <YAxis yAxisId="right" orientation="right" stroke="#8b5cf6" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                labelStyle={{ color: '#f8fafc' }}
              />
              <ReferenceLine y={0} stroke="#64748b" yAxisId="left" />
              <Bar yAxisId="left" dataKey="pnl" fill="#06b6d4" name="Monthly P&L" radius={[8, 8, 0, 0]} />
              <Line yAxisId="right" type="monotone" dataKey="cumulative" stroke="#8b5cf6" strokeWidth={2} name="Cumulative P&L" />
            </ComposedChart>
          </ResponsiveContainer>
        </TabsContent>

        <TabsContent value="holding" className="space-y-4">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={holdingPeriodData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="period" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                labelStyle={{ color: '#f8fafc' }}
              />
              <ReferenceLine y={0} stroke="#64748b" />
              <Bar dataKey="avgPnl" fill="#10b981" name="Avg P&L" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
          <div className="grid grid-cols-3 sm:grid-cols-5 gap-2 text-xs text-center">
            {holdingPeriodData.map((period, idx) => (
              <div key={idx} className="p-2 bg-slate-900/50 rounded-lg">
                <p className="text-slate-400">{period.period}</p>
                <p className="text-white font-semibold">{period.trades} trades</p>
                <p className="text-slate-400">{period.winRate}% win</p>
              </div>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="entry" className="space-y-4">
          <ResponsiveContainer width="100%" height={300}>
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis type="number" dataKey="entryPrice" name="Entry Price" stroke="#94a3b8" />
              <YAxis type="number" dataKey="pnl" name="P&L" stroke="#94a3b8" />
              <Tooltip
                cursor={{ strokeDasharray: '3 3' }}
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                labelStyle={{ color: '#f8fafc' }}
              />
              <ReferenceLine y={0} stroke="#64748b" />
              <Scatter name="UK" data={entryExitData.filter(d => d.market === 'UK')} fill="#06b6d4" />
              <Scatter name="US" data={entryExitData.filter(d => d.market === 'US')} fill="#8b5cf6" />
            </ScatterChart>
          </ResponsiveContainer>
          <div className="flex items-center justify-center gap-6 text-xs">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-cyan-500" />
              <span className="text-slate-400">UK Market</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-violet-500" />
              <span className="text-slate-400">US Market</span>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
