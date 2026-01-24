import { motion } from "framer-motion";

export default function WinRateChart({ winRate, wins, losses }) {
  const circumference = 2 * Math.PI * 45;
  const strokeDashoffset = circumference - (winRate / 100) * circumference;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-6"
    >
      <h3 className="text-lg font-semibold text-white mb-2">Win Rate</h3>
      <p className="text-sm text-slate-400 mb-6">Overall performance</p>

      <div className="flex items-center justify-center">
        <div className="relative">
          <svg width="140" height="140" className="transform -rotate-90">
            {/* Background circle */}
            <circle
              cx="70"
              cy="70"
              r="45"
              stroke="#334155"
              strokeWidth="12"
              fill="none"
            />
            {/* Progress circle */}
            <circle
              cx="70"
              cy="70"
              r="45"
              stroke="url(#gradient)"
              strokeWidth="12"
              fill="none"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              style={{ transition: 'stroke-dashoffset 1s ease-out' }}
            />
            <defs>
              <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#22d3ee" />
                <stop offset="100%" stopColor="#a78bfa" />
              </linearGradient>
            </defs>
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-3xl font-bold text-white">{winRate.toFixed(0)}%</span>
          </div>
        </div>
      </div>

      <div className="flex items-center justify-center gap-8 mt-6">
        <div className="text-center">
          <div className="flex items-center gap-2 justify-center">
            <div className="w-3 h-3 rounded-full bg-emerald-400" />
            <span className="text-2xl font-semibold text-white">{wins}</span>
          </div>
          <p className="text-xs text-slate-400 mt-1">Wins</p>
        </div>
        <div className="w-px h-10 bg-slate-700" />
        <div className="text-center">
          <div className="flex items-center gap-2 justify-center">
            <div className="w-3 h-3 rounded-full bg-rose-400" />
            <span className="text-2xl font-semibold text-white">{losses}</span>
          </div>
          <p className="text-xs text-slate-400 mt-1">Losses</p>
        </div>
      </div>
    </motion.div>
  );
}
