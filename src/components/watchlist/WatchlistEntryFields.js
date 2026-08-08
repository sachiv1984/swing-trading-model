import PropTypes from "prop-types";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { cn } from "../../lib/utils";

const MARKETS = ["UK", "US"];
const PRICE_FIELDS = [
  { key: "target_entry_price", label: "Target Entry Price" },
  { key: "initial_stop_price", label: "Initial Stop Price" },
  { key: "current_stop_price", label: "Current Stop Price" },
];

function PriceField({ label, value, onChange }) {
  return (
    <div className="space-y-1.5">
      <Label className="text-slate-600 dark:text-slate-400 text-xs">{label}</Label>
      <Input
        type="number"
        step="0.01"
        value={value}
        onChange={onChange}
        placeholder="Optional"
        className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-600 dark:text-slate-400 h-9"
      />
    </div>
  );
}

PriceField.propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  onChange: PropTypes.func.isRequired,
};

function MarketToggle({ market, isEdit, onSelect }) {
  return (
    <div className="space-y-1.5">
      <Label className="text-slate-600 dark:text-slate-400 text-xs">Market</Label>
      <div className="grid grid-cols-2 gap-2">
        {MARKETS.map((m) => (
          <button
            key={m}
            type="button"
            disabled={isEdit}
            onClick={() => !isEdit && onSelect(m)}
            className={cn(
              "py-2 rounded-lg text-sm font-medium border transition-all",
              market === m
                ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 border-cyan-500/40 text-cyan-400"
                : "bg-slate-800/50 border-slate-700 text-slate-600 dark:text-slate-400",
              isEdit && "opacity-50 cursor-not-allowed"
            )}
          >
            {m}
          </button>
        ))}
      </div>
    </div>
  );
}

MarketToggle.propTypes = {
  market: PropTypes.string.isRequired,
  isEdit: PropTypes.bool,
  onSelect: PropTypes.func.isRequired,
};

export default function WatchlistEntryFields({ form, setForm, tickerError, isEdit, onTickerChange }) {
  return (
    <div className="space-y-4 py-2">
      <div className="space-y-1.5">
        <Label className="text-slate-600 dark:text-slate-400 text-xs">Ticker Symbol</Label>
        <Input
          value={form.ticker}
          onChange={(e) => onTickerChange(e.target.value)}
          disabled={isEdit}
          placeholder="e.g. AAPL"
          className={cn(
            "bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-600 dark:text-slate-400 h-9",
            isEdit && "opacity-50 cursor-not-allowed",
            tickerError && "border-rose-500/60"
          )}
        />
        {tickerError && (
          <p className="text-xs text-rose-700 dark:text-rose-400">{tickerError}</p>
        )}
      </div>

      <MarketToggle
        market={form.market}
        isEdit={isEdit}
        onSelect={(m) => setForm((f) => ({ ...f, market: m }))}
      />

      {PRICE_FIELDS.map(({ key, label }) => (
        <PriceField
          key={key}
          label={label}
          value={form[key]}
          onChange={(e) => setForm((f) => ({ ...f, [key]: e.target.value }))}
        />
      ))}
    </div>
  );
}

WatchlistEntryFields.propTypes = {
  form: PropTypes.shape({
    ticker: PropTypes.string.isRequired,
    market: PropTypes.string.isRequired,
    target_entry_price: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    initial_stop_price: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    current_stop_price: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  }).isRequired,
  setForm: PropTypes.func.isRequired,
  tickerError: PropTypes.string,
  isEdit: PropTypes.bool,
  onTickerChange: PropTypes.func.isRequired,
};
