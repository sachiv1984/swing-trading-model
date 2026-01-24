import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "../ui/dialog";
import { Button } from "../ui/button";
import { FileSpreadsheet, FileText, Download, Loader2, Check } from "lucide-react";
import { motion } from "framer-motion";

export default function ExportModal({ open, onClose, positions, metrics, period, portfolio }) {
  const [exporting, setExporting] = useState(null);
  const [exported, setExported] = useState(null);

  const exportToCSV = () => {
    setExporting("csv");
    
    const closedPositions = positions.filter(p => p.status === "closed");
    
    const headers = [
      "Ticker", "Market", "Entry Date", "Exit Date", "Entry Price", "Exit Price",
      "Shares", "P&L", "P&L %", "Exit Reason", "Fees"
    ];
    
    const rows = closedPositions.map(p => [
      p.ticker,
      p.market,
      p.entry_date,
      p.exit_date,
      p.entry_price,
      p.exit_price,
      p.shares,
      p.pnl?.toFixed(2),
      p.pnl_percent?.toFixed(2),
      p.exit_reason,
      p.fees?.toFixed(2)
    ]);

    const csvContent = [
      headers.join(","),
      ...rows.map(row => row.join(","))
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `trade_history_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();

    setTimeout(() => {
      setExporting(null);
      setExported("csv");
      setTimeout(() => setExported(null), 2000);
    }, 500);
  };

  const exportToPDF = () => {
    setExporting("pdf");
    
    // Create a simple HTML report and print to PDF
    const closedPositions = positions.filter(p => p.status === "closed");
    
    const htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>Performance Report - ${period}</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 40px; color: #1e293b; }
          h1 { color: #0f172a; border-bottom: 2px solid #22d3ee; padding-bottom: 10px; }
          h2 { color: #334155; margin-top: 30px; }
          .summary { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 20px 0; }
          .stat { background: #f8fafc; padding: 15px; border-radius: 8px; border-left: 4px solid #22d3ee; }
          .stat-label { font-size: 12px; color: #64748b; }
          .stat-value { font-size: 20px; font-weight: bold; color: #0f172a; }
          table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 12px; }
          th { background: #f1f5f9; padding: 10px; text-align: left; border-bottom: 2px solid #e2e8f0; }
          td { padding: 10px; border-bottom: 1px solid #e2e8f0; }
          .positive { color: #10b981; }
          .negative { color: #ef4444; }
          .footer { margin-top: 40px; text-align: center; color: #94a3b8; font-size: 12px; }
        </style>
      </head>
      <body>
        <h1>Performance Report</h1>
        <p>Period: ${period} | Generated: ${new Date().toLocaleDateString()}</p>
        
        <h2>Summary</h2>
        <div class="summary">
          <div class="stat">
            <div class="stat-label">Total P&L</div>
            <div class="stat-value ${metrics.totalPnL >= 0 ? 'positive' : 'negative'}">£${metrics.totalPnL.toLocaleString(undefined, { minimumFractionDigits: 2 })}</div>
          </div>
          <div class="stat">
            <div class="stat-label">Win Rate</div>
            <div class="stat-value">${metrics.winRate.toFixed(1)}%</div>
          </div>
          <div class="stat">
            <div class="stat-label">Profit Factor</div>
            <div class="stat-value">${metrics.profitFactor === Infinity ? '∞' : metrics.profitFactor.toFixed(2)}</div>
          </div>
          <div class="stat">
            <div class="stat-label">Total Trades</div>
            <div class="stat-value">${metrics.totalTrades}</div>
          </div>
        </div>

        <div class="summary">
          <div class="stat">
            <div class="stat-label">Gross Profit</div>
            <div class="stat-value positive">£${metrics.grossProfit.toLocaleString(undefined, { minimumFractionDigits: 2 })}</div>
          </div>
          <div class="stat">
            <div class="stat-label">Gross Loss</div>
            <div class="stat-value negative">£${metrics.grossLoss.toLocaleString(undefined, { minimumFractionDigits: 2 })}</div>
          </div>
          <div class="stat">
            <div class="stat-label">Average Win</div>
            <div class="stat-value">£${metrics.avgWin.toLocaleString(undefined, { minimumFractionDigits: 2 })}</div>
          </div>
          <div class="stat">
            <div class="stat-label">Average Loss</div>
            <div class="stat-value">£${metrics.avgLoss.toLocaleString(undefined, { minimumFractionDigits: 2 })}</div>
          </div>
        </div>

        <h2>Trade History</h2>
        <table>
          <thead>
            <tr>
              <th>Ticker</th>
              <th>Market</th>
              <th>Entry</th>
              <th>Exit</th>
              <th>Shares</th>
              <th>P&L</th>
              <th>Reason</th>
            </tr>
          </thead>
          <tbody>
            ${closedPositions.map(p => `
              <tr>
                <td><strong>${p.ticker}</strong></td>
                <td>${p.market}</td>
                <td>${p.entry_date}</td>
                <td>${p.exit_date || '-'}</td>
                <td>${p.shares}</td>
                <td class="${(p.pnl || 0) >= 0 ? 'positive' : 'negative'}">£${(p.pnl || 0).toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
                <td>${p.exit_reason || '-'}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>

        <div class="footer">
          <p>Position Manager - Performance Report</p>
        </div>
      </body>
      </html>
    `;

    const printWindow = window.open('', '_blank');
    printWindow.document.write(htmlContent);
    printWindow.document.close();
    printWindow.print();

    setTimeout(() => {
      setExporting(null);
      setExported("pdf");
      setTimeout(() => setExported(null), 2000);
    }, 500);
  };

  const exportOptions = [
    {
      id: "csv",
      title: "Export to CSV",
      description: "Download trade history as a spreadsheet",
      icon: FileSpreadsheet,
      action: exportToCSV,
      color: "from-emerald-500 to-cyan-500"
    },
    {
      id: "pdf",
      title: "Export to PDF",
      description: "Generate a printable performance report",
      icon: FileText,
      action: exportToPDF,
      color: "from-violet-500 to-fuchsia-500"
    }
  ];

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-md">
        <DialogHeader>
          <DialogTitle className="text-xl font-bold text-white">Export Report</DialogTitle>
          <DialogDescription className="text-slate-400">
            Export your {period.toLowerCase()} trading data
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-3 mt-4">
          {exportOptions.map((option) => {
            const Icon = option.icon;
            const isExporting = exporting === option.id;
            const isExported = exported === option.id;
            
            return (
              <motion.button
                key={option.id}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={option.action}
                disabled={exporting !== null}
                className="w-full flex items-center gap-4 p-4 rounded-xl bg-slate-800/50 border border-slate-700/50 hover:border-slate-600 transition-all text-left disabled:opacity-50"
              >
                <div className={`p-3 rounded-xl bg-gradient-to-br ${option.color}`}>
                  {isExporting ? (
                    <Loader2 className="w-5 h-5 text-white animate-spin" />
                  ) : isExported ? (
                    <Check className="w-5 h-5 text-white" />
                  ) : (
                    <Icon className="w-5 h-5 text-white" />
                  )}
                </div>
                <div className="flex-1">
                  <p className="font-medium text-white">{option.title}</p>
                  <p className="text-sm text-slate-400">{option.description}</p>
                </div>
                <Download className="w-5 h-5 text-slate-500" />
              </motion.button>
            );
          })}
        </div>

        <div className="mt-4 p-3 rounded-lg bg-slate-800/30 border border-slate-700/30">
          <p className="text-xs text-slate-400">
            <strong className="text-slate-300">Included data:</strong> {positions.filter(p => p.status === "closed").length} closed trades, 
            performance metrics, and trade breakdown for {period.toLowerCase()}.
          </p>
        </div>
      </DialogContent>
    </Dialog>
  );
}
