import { useState, useEffect, useRef } from "react";
import PageHeader from "../components/ui/PageHeader";
import NotificationTabBar from "../components/notifications/NotificationTabBar";
import PreferenceRow from "../components/notifications/PreferenceRow";

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const ALERT_META = {
  stop_loss_approach: {
    label: "Stop Loss Approach",
    description: "Notify when current stop is within threshold % of price",
  },
  grace_period_warning: {
    label: "Grace Period Warning",
    description: "Notify on days 8–9 of the grace period",
  },
  market_regime_change: {
    label: "Market Regime Change",
    description: "Notify when market regime transitions to risk-off",
  },
  daily_portfolio_summary: {
    label: "Daily Portfolio Summary",
    description: "Receive a daily digest of portfolio status",
  },
};

export default function NotificationPreferences() {
  const [preferences, setPreferences] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [rowState, setRowState] = useState({});
  const debounceTimers = useRef({});

  useEffect(() => {
    fetch(`${API_BASE_URL}/notifications/preferences`)
      .then((r) => {
        if (!r.ok) throw new Error();
        return r.json();
      })
      .then((json) => {
        setPreferences(json.data.preferences);
        setLoading(false);
      })
      .catch(() => {
        setLoadError(true);
        setLoading(false);
      });
  }, []);

  const handleToggle = (alertType, newValue) => {
    setPreferences((prev) =>
      prev.map((p) =>
        p.alert_type === alertType ? { ...p, email_enabled: newValue } : p
      )
    );
    setRowState((prev) => ({ ...prev, [alertType]: { saved: false, error: null } }));

    if (debounceTimers.current[alertType]) {
      clearTimeout(debounceTimers.current[alertType]);
    }
    debounceTimers.current[alertType] = setTimeout(() => {
      fetch(`${API_BASE_URL}/notifications/preferences`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ [alertType]: { email_enabled: newValue } }),
      })
        .then((r) => {
          if (!r.ok) throw new Error();
          setRowState((prev) => ({ ...prev, [alertType]: { saved: true, error: null } }));
          setTimeout(() => {
            setRowState((prev) => ({ ...prev, [alertType]: { saved: false, error: null } }));
          }, 2000);
        })
        .catch(() => {
          setPreferences((prev) =>
            prev.map((p) =>
              p.alert_type === alertType ? { ...p, email_enabled: !newValue } : p
            )
          );
          setRowState((prev) => ({
            ...prev,
            [alertType]: { saved: false, error: "Failed to save preference. Please try again." },
          }));
        });
    }, 150);
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Notification Preferences"
        description="Configure which alerts you receive."
      />

      <NotificationTabBar />

      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 divide-y divide-slate-700/50">
        {loadError ? (
          <div className="p-6 text-rose-400 text-sm">
            Unable to load preferences. Please refresh.
          </div>
        ) : loading ? (
          Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="flex items-center justify-between px-6 py-5">
              <div className="space-y-2">
                <div className="h-4 w-48 bg-slate-700 rounded animate-pulse" />
                <div className="h-3 w-72 bg-slate-800 rounded animate-pulse" />
              </div>
              <div className="h-6 w-11 bg-slate-700 rounded-full animate-pulse" />
            </div>
          ))
        ) : (
          preferences.map((pref) => {
            const meta = ALERT_META[pref.alert_type] || { label: pref.alert_type, description: "" };
            const state = rowState[pref.alert_type] || { saved: false, error: null };
            return (
              <PreferenceRow
                key={pref.alert_type}
                label={meta.label}
                description={meta.description}
                enabled={pref.email_enabled}
                saved={state.saved}
                error={state.error}
                onToggle={(val) => handleToggle(pref.alert_type, val)}
              />
            );
          })
        )}
      </div>
    </div>
  );
}
