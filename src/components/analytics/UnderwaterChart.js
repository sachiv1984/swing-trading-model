import { useState, useEffect, useRef, useCallback } from "react";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, Dot } from "recharts";
import { TrendingDown, ZoomIn, ZoomOut, RotateCcw } from "lucide-react";

const MIN_POINTS = 4;

export default function UnderwaterChart({ trades }) {
  const [zoomRange, setZoomRange] = useState(null); // [startIdx, endIdx] or null when full range
  const [dragState, setDragState] = useState(null); // { x, range } while dragging
  const [hintVisible, setHintVisible] = useState(false);
  const containerRef = useRef(null);
  const hintShownRef = useRef(false);
  const zoomRef = useRef(null);
  const dataRef = useRef([]);

  // Calculate underwater curve data — uses snake_case field names from API
  const calculateUnderwaterData = () => {
    if (!trades || trades.length === 0) return [];

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
        drawdown,
        equity: runningEquity,
        peak: peakEquity
      });
    });

    return data;
  };

  const data = calculateUnderwaterData();

  // Keep refs in sync with current state/data so event handlers always see fresh values
  useEffect(() => { zoomRef.current = zoomRange; }, [zoomRange]);
  useEffect(() => { dataRef.current = data; }, [data]);

  // Zoom by direction: +1 = zoom in, -1 = zoom out
  const applyZoom = useCallback((direction) => {
    const total = dataRef.current.length;
    if (total < MIN_POINTS) return;
    const [s, e] = zoomRef.current || [0, total];
    const currentLen = e - s;
    const delta = Math.max(1, Math.round(currentLen * 0.2));
    const newLen = direction > 0
      ? Math.max(MIN_POINTS, currentLen - delta)
      : Math.min(total, currentLen + delta);
    const center = Math.round((s + e) / 2);
    let newS = Math.max(0, center - Math.floor(newLen / 2));
    let newE = Math.min(total, newS + newLen);
    // If end-capped (near right edge), shift start left to fill the intended window
    if (newE - newS < newLen) {
      newS = Math.max(0, newE - newLen);
    }
    if (newLen >= total) {
      setZoomRange(null);
    } else {
      setZoomRange([newS, newE]);
    }
  }, []);

  // Attach non-passive wheel listener so we can call preventDefault()
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const handler = (e) => {
      e.preventDefault();
      applyZoom(e.deltaY < 0 ? 1 : -1);
    };
    el.addEventListener("wheel", handler, { passive: false });
    return () => el.removeEventListener("wheel", handler);
  }, [applyZoom]);

  const isZoomed = zoomRange !== null;
  const displayData = isZoomed ? data.slice(zoomRange[0], zoomRange[1]) : data;

  // Max drawdown from all-time data; dot renders only when the point is in displayData
  const maxDrawdownPoint = data.length > 0
    ? data.reduce((max, curr) => curr.drawdown < max.drawdown ? curr : max, data[0])
    : null;

  // Pan: click-drag shifts the zoom window
  const handleMouseDown = (e) => {
    if (!isZoomed) return;
    setDragState({ x: e.clientX, range: [...zoomRange] });
  };

  const handleMouseMove = (e) => {
    if (!dragState) return;
    const containerWidth = containerRef.current?.clientWidth ?? 600;
    const [s, end] = dragState.range;
    const rangeLen = end - s;
    const pxPerPt = containerWidth / rangeLen;
    // Drag right = pan left (earlier trades come into view)
    const shift = Math.round((dragState.x - e.clientX) / pxPerPt);
    const newS = Math.max(0, s + shift);
    const newE = Math.min(data.length, newS + rangeLen);
    setZoomRange([newS, newE]);
  };

  const handleMouseUp = () => setDragState(null);

  const handleMouseEnter = () => {
    if (!hintShownRef.current && data.length > MIN_POINTS) {
      hintShownRef.current = true;
      setHintVisible(true);
      setTimeout(() => setHintVisible(false), 3000);
    }
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload[0]) {
      const d = payload[0].payload;
      return (
        <div className="bg-slate-900 border border-slate-700 rounded-lg p-3 shadow-xl">
          <p className="text-xs text-slate-400 mb-1">{new Date(d.date).toLocaleDateString()}</p>
          <p className="text-sm font-semibold text-rose-400">{d.drawdown.toFixed(2)}%</p>
          <p className="text-xs text-slate-400 mt-1">Current: £{d.equity.toFixed(0)}</p>
          <p className="text-xs text-slate-400">Peak: £{d.peak.toFixed(0)}</p>
        </div>
      );
    }
    return null;
  };

  const CustomDot = (props) => {
    const { cx, cy, payload } = props;
    if (maxDrawdownPoint && payload.date === maxDrawdownPoint.date) {
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

  const hasData = data.length > 2;

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm overflow-hidden">
      <div className="p-6 border-b border-slate-700/50">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-to-br from-rose-500 to-red-600">
              <TrendingDown className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white">Underwater Equity Curve</h3>
              <p className="text-sm text-slate-400">% Below Peak Equity</p>
            </div>
          </div>
          {hasData && (
            <div className="flex items-center gap-1">
              <button
                onClick={() => applyZoom(1)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-700/50 transition-colors"
                title="Zoom in"
              >
                <ZoomIn className="w-4 h-4" />
              </button>
              <button
                onClick={() => applyZoom(-1)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-700/50 transition-colors"
                title="Zoom out"
              >
                <ZoomOut className="w-4 h-4" />
              </button>
              {isZoomed && (
                <button
                  onClick={() => setZoomRange(null)}
                  className="px-2 py-1 rounded-lg text-xs text-slate-300 hover:text-white bg-slate-700/50 hover:bg-slate-700 transition-colors flex items-center gap-1"
                  title="Reset zoom"
                >
                  <RotateCcw className="w-3 h-3" />
                  Reset
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      <div
        ref={containerRef}
        data-testid="underwater-chart"
        className="p-6 select-none"
        style={{ cursor: isZoomed ? (dragState ? "grabbing" : "grab") : "default" }}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onMouseEnter={handleMouseEnter}
      >
        {data.length === 0 ? (
          <div className="h-64 flex items-center justify-center text-slate-400">
            No trade data available
          </div>
        ) : data.length <= 2 ? (
          <div className="h-64 flex items-center justify-center text-slate-400">
            Need more trades for trend analysis
          </div>
        ) : (
          <>
            {hintVisible && (
              <p className="text-xs text-slate-400 text-center mb-2 transition-opacity duration-300">
                Scroll to zoom
              </p>
            )}
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={displayData} style={{ cursor: "inherit" }}>
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
                  tick={{ fill: "#94a3b8", fontSize: 12 }}
                  tickFormatter={(date) => new Date(date).toLocaleDateString("en-GB", { month: "short", day: "numeric" })}
                />
                <YAxis
                  stroke="#64748b"
                  tick={{ fill: "#94a3b8", fontSize: 12 }}
                  tickFormatter={(value) => `${value.toFixed(0)}%`}
                  domain={["auto", 0]}
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
          </>
        )}
      </div>
    </div>
  );
}
