/**
 * pages.config.js - Page routing configuration
 * 
 * This file is AUTO-GENERATED. Do not add imports or modify PAGES manually.
 * Pages are auto-registered when you create files in the ./pages/ folder.
 * 
 * THE ONLY EDITABLE VALUE: mainPage
 * This controls which page is the landing page (shown when users visit the app).
 * 
 * Example file structure:
 * 
 *   import HomePage from './pages/HomePage';
 *   import Dashboard from './pages/Dashboard';
 *   import Settings from './pages/Settings';
 *   
 *   export const PAGES = {
 *       "HomePage": HomePage,
 *       "Dashboard": Dashboard,
 *       "Settings": Settings,
 *   }
 *   
 *   export const pagesConfig = {
 *       mainPage: "HomePage",
 *       Pages: PAGES,
 *   };
 * 
 * Example with Layout (wraps all pages):
 *
 *   import Home from './pages/Home';
 *   import Settings from './pages/Settings';
 *   import __Layout from './Layout.jsx';
 *
 *   export const PAGES = {
 *       "Home": Home,
 *       "Settings": Settings,
 *   }
 *
 *   export const pagesConfig = {
 *       mainPage: "Home",
 *       Pages: PAGES,
 *       Layout: __Layout,
 *   };
 *
 * To change the main page from HomePage to Dashboard, use find_replace:
 *   Old: mainPage: "HomePage",
 *   New: mainPage: "Dashboard",
 *
 * The mainPage value must match a key in the PAGES object exactly.
 */
import Dashboard from './pages/Dashboard';
import DashboardHome from './pages/DashboardHome';
import Positions from './pages/Positions';
import Reports from './pages/Reports';
import Settings from './pages/Settings';
import Signals from './pages/Signals';
import TradeEntry from './pages/TradeEntry';
import TradeHistory from './pages/TradeHistory';
import SystemStatus from './pages/SystemStatus';
import PerformanceAnalytics from './pages/PerformanceAnalytics';
import RiskDashboard from './pages/RiskDashboard';
import TradeReflection from './pages/TradeReflection';
import Watchlist from './pages/Watchlist';
import WeeklyDigest from './pages/WeeklyDigest';
import Screener from './pages/Screener';
import TradePlan from './pages/TradePlan';
import TradePlans from './pages/TradePlans';
import TickerUniverse from './pages/TickerUniverse';
import RedFlagJournal from './pages/RedFlagJournal';
import StrategyBenchmark from './pages/StrategyBenchmark';
import __Layout from './Layout.js';


export const PAGES = {
    "DashboardHome": DashboardHome,
    "Dashboard": Dashboard,
    "Positions": Positions,
    "Reports": Reports,
    "Settings": Settings,
    "Signals": Signals,
    "TradeEntry": TradeEntry,
    "TradeHistory": TradeHistory,
    "SystemStatus": SystemStatus,
    "PerformanceAnalytics": PerformanceAnalytics,
    "RiskDashboard": RiskDashboard,
    "TradeReflection": TradeReflection,
    "Watchlist": Watchlist,
    "WeeklyDigest": WeeklyDigest,
    "Screener": Screener,
    "TradePlan": TradePlan,
    "TradePlans": TradePlans,
    "TickerUniverse": TickerUniverse,
    "RedFlagJournal": RedFlagJournal,
    "StrategyBenchmark": StrategyBenchmark,
}

export const pagesConfig = {
    mainPage: "DashboardHome",
    Pages: PAGES,
    Layout: __Layout,
};
