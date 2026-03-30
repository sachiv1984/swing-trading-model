import { useState, useEffect } from "react";
import { Bell } from "lucide-react";
import PageHeader from "../components/ui/PageHeader";
import NotificationTabBar from "../components/notifications/NotificationTabBar";
import NotificationRow from "../components/notifications/NotificationRow";
import { useToast } from "../components/ui/use-toast";
import { apiFetch } from "../api/base44Client";
import DataState from "../components/ui/DataState";

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    apiFetch(`${API_BASE_URL}/notifications?page=1`)
      .then((r) => {
        if (!r.ok) throw new Error();
        return r.json();
      })
      .then((json) => {
        setNotifications(json.data.notifications);
        setHasMore(json.data.has_more);
        setPage(1);
        setLoading(false);
      })
      .catch(() => {
        setLoadError(true);
        setLoading(false);
      });
  }, []);

  const handleLoadMore = () => {
    const nextPage = page + 1;
    setLoadingMore(true);
    apiFetch(`${API_BASE_URL}/notifications?page=${nextPage}`)
      .then((r) => {
        if (!r.ok) throw new Error();
        return r.json();
      })
      .then((json) => {
        setNotifications((prev) => [...prev, ...json.data.notifications]);
        setHasMore(json.data.has_more);
        setPage(nextPage);
        setLoadingMore(false);
      })
      .catch(() => {
        setLoadingMore(false);
      });
  };

  const handleMarkRead = (id) => {
    // Optimistic update
    setNotifications((prev) =>
      prev.map((n) => (n.id === id ? { ...n, read: true, _error: false } : n))
    );
    apiFetch(`${API_BASE_URL}/notifications/${id}`, { method: "PATCH" })
      .then((r) => {
        if (!r.ok) throw new Error();
      })
      .catch(() => {
        // Revert
        setNotifications((prev) =>
          prev.map((n) => (n.id === id ? { ...n, read: false, _error: true } : n))
        );
        // Clear error after 3s
        setTimeout(() => {
          setNotifications((prev) =>
            prev.map((n) => (n.id === id ? { ...n, _error: false } : n))
          );
        }, 3000);
      });
  };

  const handleMarkAllRead = () => {
    const prior = notifications.map((n) => ({ id: n.id, read: n.read }));
    // Optimistic update
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
    apiFetch(`${API_BASE_URL}/notifications/mark-all-read`, { method: "POST" })
      .then((r) => {
        if (!r.ok) throw new Error();
      })
      .catch(() => {
        // Revert
        setNotifications((prev) =>
          prev.map((n) => {
            const original = prior.find((p) => p.id === n.id);
            return original ? { ...n, read: original.read } : n;
          })
        );
        toast({
          title: "Error",
          description: "Failed to mark all as read. Please try again.",
          variant: "destructive",
        });
      });
  };

  const hasUnread = notifications.some((n) => !n.read);

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4">
        <PageHeader
          title="Notifications"
          description="Recent alerts and system events."
        />
        {hasUnread && !loading && !loadError && (
          <button
            onClick={handleMarkAllRead}
            className="mt-1 text-sm text-cyan-400 hover:text-cyan-300 transition-colors shrink-0"
          >
            Mark all as read
          </button>
        )}
      </div>

      <NotificationTabBar />

      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 divide-y divide-slate-700/50">
        <DataState
          loading={loading}
          error={loadError}
          onRetry={() => {
            setLoadError(false);
            setLoading(true);
            apiFetch(`${API_BASE_URL}/notifications?page=1`)
              .then((r) => { if (!r.ok) throw new Error(); return r.json(); })
              .then((json) => {
                setNotifications(json.data.notifications);
                setHasMore(json.data.has_more);
                setPage(1);
                setLoading(false);
              })
              .catch(() => { setLoadError(true); setLoading(false); });
          }}
          empty={!loading && !loadError && notifications.length === 0}
          emptyIcon={<Bell className="w-10 h-10 text-slate-600" />}
          emptyHeading="No notifications yet"
          emptyBody="Alert notifications will appear here when triggered."
        >
          <>
            {notifications.map((n) => (
              <NotificationRow
                key={n.id}
                notification={n}
                onMarkRead={() => handleMarkRead(n.id)}
              />
            ))}
            {hasMore && (
              <div className="px-6 py-4">
                <button
                  onClick={handleLoadMore}
                  disabled={loadingMore}
                  className="text-sm text-cyan-400 hover:text-cyan-300 transition-colors disabled:opacity-50"
                >
                  {loadingMore ? "Loading…" : "Load more"}
                </button>
              </div>
            )}
          </>
        </DataState>
      </div>
    </div>
  );
}
