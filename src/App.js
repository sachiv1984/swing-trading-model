import { Toaster } from "./components/ui/toaster"
import { Toaster as SonnerToaster } from "sonner"
import NotificationPreferences from "./pages/NotificationPreferences"
import Notifications from "./pages/Notifications"
import NotificationsHistory from "./pages/NotificationsHistory"
import Research from "./pages/Research"
import StandingAlertHarness from "./pages/__StandingAlertHarness"
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClientInstance } from './lib/query-client'
import NavigationTracker from './lib/NavigationTracker'
import { pagesConfig } from './pages.config'
import { HashRouter as Router, Route, Routes } from 'react-router-dom';
import PageNotFound from './lib/PageNotFound';
import { AuthProvider, useAuth } from './lib/AuthContext';
import UserNotRegisteredError from './components/UserNotRegisteredError';

const { Pages, Layout, mainPage } = pagesConfig;
const mainPageKey = mainPage ?? Object.keys(Pages)[0];
const MainPage = mainPageKey ? Pages[mainPageKey] : <></>;

const LayoutWrapper = ({ children, currentPageName }) => Layout ?
  <Layout currentPageName={currentPageName}>{children}</Layout>
  : <>{children}</>;

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
