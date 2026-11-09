import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, Activity, Menu, X } from 'lucide-react';
import Hero from './components/Hero';
import ClaimInput from './components/ClaimInput';
import ResultCard from './components/ResultCard';
import EvidenceList from './components/EvidenceList';
import HistoryPanel from './components/HistoryPanel';
import StatsBar from './components/StatsBar';
import Footer from './components/Footer';
import { analyzeClaim, getHistory } from './api';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleAnalyze = useCallback(async (claim) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await analyzeClaim(claim);
      setResult(data);
      setHistory((prev) => [
        { claim, verdict: data.verdict, confidence: data.confidence, timestamp: new Date().toISOString() },
        ...prev,
      ]);
    } catch (err) {
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  const handleHistoryClick = useCallback((item) => {
    handleAnalyze(item.claim);
    setShowHistory(false);
  }, [handleAnalyze]);

  const handleClearHistory = useCallback(() => {
    setHistory([]);
  }, []);

  const stats = {
    total: history.length,
    supports: history.filter((h) => h.verdict === 'SUPPORTS').length,
    refutes: history.filter((h) => h.verdict === 'REFUTES').length,
    notEnough: history.filter((h) => h.verdict === 'NOT_ENOUGH_EVIDENCE').length,
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] flex flex-col">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-xl border-b border-slate-100 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-indigo-500 to-indigo-700 p-2 rounded-xl shadow-md shadow-indigo-200">
                <Shield className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900 tracking-tight">
                  Fact-Sift
                </h1>
                <p className="text-[10px] text-slate-400 font-medium tracking-wide uppercase -mt-0.5">
                  Evidence-Based Verification
                </p>
              </div>
            </div>

            <div className="hidden sm:flex items-center gap-4">
              <button
                onClick={() => setShowHistory(!showHistory)}
                className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-slate-600 hover:text-indigo-600 hover:bg-indigo-50 rounded-xl transition-all duration-200"
              >
                <Activity className="w-4 h-4" />
                History
                {history.length > 0 && (
                  <span className="bg-indigo-100 text-indigo-700 text-xs font-semibold px-2 py-0.5 rounded-full">
                    {history.length}
                  </span>
                )}
              </button>
            </div>

            <button
              className="sm:hidden p-2 text-slate-600 hover:text-indigo-600 rounded-lg"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="sm:hidden border-t border-slate-100 bg-white"
            >
              <div className="px-4 py-3">
                <button
                  onClick={() => { setShowHistory(!showHistory); setMobileMenuOpen(false); }}
                  className="flex items-center gap-2 w-full px-4 py-2.5 text-sm font-medium text-slate-600 hover:text-indigo-600 hover:bg-indigo-50 rounded-xl transition-all"
                >
                  <Activity className="w-4 h-4" />
                  History
                  {history.length > 0 && (
                    <span className="bg-indigo-100 text-indigo-700 text-xs font-semibold px-2 py-0.5 rounded-full">
                      {history.length}
                    </span>
                  )}
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>

      {/* Main Content */}
      <main className="flex-1">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <Hero />

          {stats.total > 0 && <StatsBar stats={stats} />}

          <ClaimInput onAnalyze={handleAnalyze} loading={loading} />

          {/* Error State */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="max-w-3xl mx-auto mt-6"
              >
                <div className="bg-rose-50 border border-rose-200 text-rose-700 px-6 py-4 rounded-2xl text-sm font-medium">
                  {error}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Loading Skeleton */}
          <AnimatePresence>
            {loading && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="max-w-3xl mx-auto mt-8 space-y-4"
              >
                <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 space-y-4">
                  <div className="skeleton h-8 w-48" />
                  <div className="skeleton h-4 w-full" />
                  <div className="skeleton h-4 w-3/4" />
                  <div className="skeleton h-24 w-full mt-4" />
                </div>
                {[1, 2].map((i) => (
                  <div key={i} className="bg-white rounded-2xl shadow-sm border border-slate-100 p-5 space-y-3">
                    <div className="skeleton h-5 w-32" />
                    <div className="skeleton h-3 w-full" />
                    <div className="skeleton h-3 w-2/3" />
                  </div>
                ))}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Results */}
          <AnimatePresence>
            {result && !loading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="max-w-3xl mx-auto mt-8 space-y-6 pb-12"
              >
                <ResultCard result={result} />
                {result.evidence && result.evidence.length > 0 && (
                  <EvidenceList evidence={result.evidence} />
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>

      {/* History Slide-over */}
      <AnimatePresence>
        {showHistory && (
          <HistoryPanel
            history={history}
            onClose={() => setShowHistory(false)}
            onItemClick={handleHistoryClick}
            onClear={handleClearHistory}
          />
        )}
      </AnimatePresence>

      <Footer />
    </div>
  );
}

export default App;
