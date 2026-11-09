import { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Loader2, Lightbulb } from 'lucide-react';

const EXAMPLE_CLAIMS = [
  'The Earth revolves around the Sun.',
  'Humans only use 10% of their brains.',
  'The Great Wall of China is visible from space.',
  'Water boils at 100°C at sea level.',
  'Lightning never strikes the same place twice.',
];

export default function ClaimInput({ onAnalyze, loading }) {
  const [claim, setClaim] = useState('');
  const maxChars = 500;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (claim.trim() && !loading) {
      onAnalyze(claim.trim());
    }
  };

  const handleExampleClick = (example) => {
    setClaim(example);
  };

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.2 }}
      className="max-w-3xl mx-auto mb-8"
    >
      <form onSubmit={handleSubmit}>
        <div className="relative bg-white rounded-2xl shadow-sm border border-slate-200 hover:shadow-md hover:border-indigo-200 transition-all duration-300 focus-within:shadow-lg focus-within:border-indigo-300 focus-within:ring-4 focus-within:ring-indigo-50">
          <textarea
            value={claim}
            onChange={(e) => setClaim(e.target.value.slice(0, maxChars))}
            placeholder="Enter a claim to verify..."
            rows={3}
            className="w-full px-6 pt-5 pb-3 text-base sm:text-lg text-slate-800 placeholder-slate-300 bg-transparent resize-none focus:outline-none rounded-2xl font-light leading-relaxed"
          />
          <div className="flex items-center justify-between px-6 pb-4">
            <span className="text-xs text-slate-300 font-medium tabular-nums">
              {claim.length}/{maxChars}
            </span>
            <button
              type="submit"
              disabled={!claim.trim() || loading}
              className="inline-flex items-center gap-2 px-6 py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-indigo-600 to-indigo-500 rounded-xl shadow-md shadow-indigo-200 hover:shadow-lg hover:shadow-indigo-300 hover:from-indigo-500 hover:to-indigo-600 disabled:opacity-40 disabled:cursor-not-allowed disabled:shadow-none transition-all duration-200 active:scale-[0.97]"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Analyzing…
                </>
              ) : (
                <>
                  <Search className="w-4 h-4" />
                  Analyze
                </>
              )}
            </button>
          </div>
        </div>
      </form>

      {/* Example Claims */}
      <div className="mt-5">
        <div className="flex items-center gap-2 mb-3">
          <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
            Try an example
          </span>
        </div>
        <div className="flex flex-wrap gap-2">
          {EXAMPLE_CLAIMS.map((example) => (
            <button
              key={example}
              onClick={() => handleExampleClick(example)}
              className="px-3 py-1.5 text-xs font-medium text-slate-500 bg-white border border-slate-200 rounded-full hover:border-indigo-300 hover:text-indigo-600 hover:bg-indigo-50 transition-all duration-200 active:scale-95"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </motion.section>
  );
}
