import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Positions from './pages/Positions';
import TradeEntry from './pages/TradeEntry';
import TradeHistory from './pages/TradeHistory';
import Reports from './pages/Reports';
import Settings from './pages/Settings';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout currentPageName="Dashboard"><Dashboard /></Layout>} />
          <Route path="/positions" element={<Layout currentPageName="Positions"><Positions /></Layout>} />
          <Route path="/trade-entry" element={<Layout currentPageName="TradeEntry"><TradeEntry /></Layout>} />
          <Route path="/trade-history" element={<Layout currentPageName="TradeHistory"><TradeHistory /></Layout>} />
          <Route path="/reports" element={<Layout currentPageName="Reports"><Reports /></Layout>} />
          <Route path="/settings" element={<Layout currentPageName="Settings"><Settings /></Layout>} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
