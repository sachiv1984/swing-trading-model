import { Toaster } from "./components/ui/toaster"
import { Toaster as SonnerToaster } from "sonner"
import NotificationPreferences from "./pages/NotificationPreferences"
import Notifications from "./pages/Notifications"
import NotificationsHistory from "./pages/NotificationsHistory"
import Research from "./pages/Research"
import TickerUniverse from "./pages/TickerUniverse"
import StandingAlertHarness from "./pages/__StandingAlertHarness"
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClientInstance } from './lib/query-client'
import NavigationTracker from './lib/NavigationTracker'
import { pagesConfig } from './pages.config'
import { HashRouter as Router, Route, Routes, Navigate, useLocation } from 'react-router-dom';
import PageNotFound from './lib/PageNotFound';
import { AuthProvider, useAuth } from './lib/AuthContext';
import UserNotRegisteredError from './components/UserNotRegisteredError';

const { Pages, Layout, mainPage } = pagesConfig;
const mainPageKey = mainPage ?? Object.keys(Pages)[0];
const MainPage = mainPageKey ? Pages[mainPageKey] : <></>;

const LayoutWrapper = ({ children, currentPageName }) => Layout ?
  <Layout currentPageName={currentPageName}>{children}</Layout>
  : <>{children}</>;

// performance.md §7 (ST-06, BLG-FE-259, v9.17): /Reports and
// /PerformanceAnalytics redirect to their Performance section (replace),
// keeping other query params. ?section=strategy-compliance (the SI-05 digest
// link) maps to the Compliance section.
const PerformanceRedirect = ({ section, mapDigestSection = true }) => {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const old = params.get('section');
  params.delete('section');
  params.set('section', mapDigestSection && old === 'strategy-compliance' ? 'compliance' : section);
  return <Navigate to={`/Performance?${params.toString()}`} replace />;
};

// journal.md §5 (ST-05, BLG-FE-258, v9.17): the old Trade Reflections and Red
// Flag Journal routes redirect to their Journal section with a replace
// navigation, keeping any query string except `section`.
const JournalRedirect = ({ section }) => {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  params.delete('section');
  const rest = params.toString();
  return <Navigate to={`/Journal?section=${section}${rest ? `&${rest}` : ''}`} replace />;
};

// navigation.md v2.5 (ST-08, BLG-FE-323, v9.18): Ticker Universe moved under
// Settings. /TickerUniverse redirects (replace), keeping its query string.
const TickerUniverseRedirect = () => {
  const location = useLocation();
  return <Navigate to={`/settings/ticker-universe${location.search}`} replace />;
};

const AuthenticatedApp = () => {
  const { isLoadingAuth, isLoadingPublicSettings, authError, navigateToLogin } = useAuth();

  // Show loading spinner while checking app public settings or auth
  if (isLoadingPublicSettings || isLoadingAuth) {
    return (
      <div className="fixed inset-0 flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-slate-200 border-t-slate-800 rounded-full animate-spin"></div>
      </div>
    );
  }

  // Handle authentication errors
  if (authError) {
    if (authError.type === 'user_not_registered') {
      return <UserNotRegisteredError />;
    } else if (authError.type === 'auth_required') {
      // Redirect to login automatically
      navigateToLogin();
      return null;
    }
  }

  // Render the main app
  return (
    <Routes>
      <Route path="/" element={
        <LayoutWrapper currentPageName={mainPageKey}>
          <MainPage />
        </LayoutWrapper>
      } />
      {Object.entries(Pages).map(([path, Page]) => (
        <Route
          key={path}
          path={`/${path}`}
          element={
            <LayoutWrapper currentPageName={path}>
              <Page />
            </LayoutWrapper>
          }
        />
      ))}
      {/* ST-12 (BLG-FE-247, v9.15): the legacy widget Dashboard is removed;
          /Dashboard redirects to the Dashboard home with a replace navigation
          so Back does not return to the redirect (navigation.md §Legacy Dashboard Route). */}
      <Route path="/Dashboard" element={<Navigate to="/" replace />} />
      <Route path="/TradeReflection" element={<JournalRedirect section="reflections" />} />
      <Route path="/RedFlagJournal" element={<JournalRedirect section="red-flags" />} />
      <Route path="/Reports" element={<PerformanceRedirect section="reports" />} />
      <Route path="/PerformanceAnalytics" element={<PerformanceRedirect section="analytics" />} />
      {/* performance.md v1.3 §7 (ST-08, BLG-FE-323, v9.18): Strategy Benchmark is
          the "Strategy vs backtest" section; its own ?section= (the retired
          panel index) is replaced, ?tab= and other params are kept. */}
      <Route path="/StrategyBenchmark" element={<PerformanceRedirect section="strategy-vs-backtest" mapDigestSection={false} />} />
      <Route path="/TickerUniverse" element={<TickerUniverseRedirect />} />
      <Route path="/settings/ticker-universe" element={
        <LayoutWrapper currentPageName="TickerUniverse">
          <TickerUniverse />
        </LayoutWrapper>
      } />
      <Route path="/notifications" element={
        <LayoutWrapper currentPageName="notifications">
          <Notifications />
        </LayoutWrapper>
      } />
      <Route path="/NotificationPreferences" element={
        <LayoutWrapper currentPageName="NotificationPreferences">
          <NotificationPreferences />
        </LayoutWrapper>
      } />
      <Route path="/notifications/preferences" element={
        <LayoutWrapper currentPageName="NotificationPreferences">
          <NotificationPreferences />
        </LayoutWrapper>
      } />
      <Route path="/notifications/history" element={
        <LayoutWrapper currentPageName="notifications">
          <NotificationsHistory />
        </LayoutWrapper>
      } />
      {/* ST-01 (BLG-FE-250, v9.16): Research landing — sidebar and palette
          entry (navigation.md §Page Placement). Submitting a ticker goes to
          /research/:ticker. */}
      <Route path="/Research" element={
        <LayoutWrapper currentPageName="Research">
          <Research />
        </LayoutWrapper>
      } />
      <Route path="/research/:ticker" element={
        <LayoutWrapper currentPageName="Research">
          <Research />
        </LayoutWrapper>
      } />
      {/* Test-only route (ST-04, EPIC-04, v7.7, BLG-FE-120) — see
          src/pages/__StandingAlertHarness.js header comment. No nav/palette entry. */}
      <Route path="/__test/standing-alert" element={<StandingAlertHarness />} />
      <Route path="*" element={<PageNotFound />} />
    </Routes>
  );
};


function App() {

  return (
    <AuthProvider>
      <QueryClientProvider client={queryClientInstance}>
        <Router>
          <NavigationTracker />
          <AuthenticatedApp />
        </Router>
        <Toaster />
        <SonnerToaster />
      </QueryClientProvider>
    </AuthProvider>
  )
}

export default App
