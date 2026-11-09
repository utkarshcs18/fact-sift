import { motion } from 'framer-motion';
import { X, Trash2, Clock, CheckCircle2, XCircle, AlertTriangle } from 'lucide-react';

const verdictIcons = {
  SUPPORTS: { icon: CheckCircle2, color: 'text-emerald-500', bg: 'bg-emerald-50' },
  REFUTES: { icon: XCircle, color: 'text-rose-500', bg: 'bg-rose-50' },
  NOT_ENOUGH_EVIDENCE: { icon: AlertTriangle, color: 'text-amber-500', bg: 'bg-amber-50' },
};

function formatTime(ts) {
  try {
    const date = new Date(ts);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  } catch {
    return '';
  }
}

export default function HistoryPanel({ history, onClose, onItemClick, onClear }) {
  return (
    <>
      {/* Backdrop */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
        className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40"
      />

      {/* Panel */}
      <motion.aside
        initial={{ x: '100%' }}
        animate={{ x: 0 }}
        exit={{ x: '100%' }}
        transition={{ type: 'spring', damping: 30, stiffness: 300 }}
        className="fixed top-0 right-0 h-full w-full sm:w-96 bg-white shadow-2xl z-50 flex flex-col"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-slate-400" />
            <h2 className="text-base font-bold text-slate-800">Analysis History</h2>
          </div>
          <div className="flex items-center gap-2">
            {history.length > 0 && (
              <button
                onClick={onClear}
                className="p-2 text-slate-400 hover:text-rose-500 hover:bg-rose-50 rounded-lg transition-all"
                title="Clear history"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            )}
            <button
              onClick={onClose}
              className="p-2 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-all"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* List */}
        <div className="flex-1 overflow-y-auto px-4 py-3">
          {history.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center px-6">
              <div className="bg-slate-50 rounded-full p-4 mb-4">
                <Clock className="w-8 h-8 text-slate-300" />
              </div>
              <p className="text-sm text-slate-400 font-medium">No analyses yet</p>
              <p className="text-xs text-slate-300 mt-1">Your verification history will appear here</p>
            </div>
          ) : (
            <div className="space-y-2">
              {history.map((item, index) => {
                const v = verdictIcons[item.verdict] || verdictIcons.NOT_ENOUGH_EVIDENCE;
                const Icon = v.icon;

                return (
                  <motion.button
                    key={`${item.claim}-${index}`}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    onClick={() => onItemClick(item)}
                    className="w-full text-left bg-slate-50 hover:bg-indigo-50 rounded-xl p-4 transition-all duration-200 group border border-transparent hover:border-indigo-100"
                  >
                    <div className="flex items-start gap-3">
                      <div className={`p-1.5 rounded-lg ${v.bg} flex-shrink-0 mt-0.5`}>
                        <Icon className={`w-3.5 h-3.5 ${v.color}`} />
                      </div>
                      <div className="min-w-0 flex-1">
                        <p className="text-sm text-slate-700 font-medium truncate group-hover:text-indigo-700 transition-colors">
                          {item.claim}
                        </p>
                        <div className="flex items-center gap-2 mt-1">
                          {item.confidence != null && (
                            <span className="text-xs text-slate-400 tabular-nums">
                              {Math.round(item.confidence * 100)}% confidence
                            </span>
                          )}
                          {item.timestamp && (
                            <span className="text-xs text-slate-300">
                              · {formatTime(item.timestamp)}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </motion.button>
                );
              })}
            </div>
          )}
        </div>
      </motion.aside>
    </>
  );
}
