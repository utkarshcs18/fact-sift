import { motion } from 'framer-motion';
import { CheckCircle2, XCircle, AlertTriangle, Info, Cpu } from 'lucide-react';
import { useState, useEffect } from 'react';

const verdictConfig = {
  SUPPORTS: {
    icon: CheckCircle2,
    label: 'Supports',
    bgColor: 'bg-emerald-50',
    textColor: 'text-emerald-700',
    borderColor: 'border-emerald-200',
    barColor: 'bg-emerald-500',
    ringColor: 'ring-emerald-100',
    badgeBg: 'bg-emerald-100',
  },
  REFUTES: {
    icon: XCircle,
    label: 'Refutes',
    bgColor: 'bg-rose-50',
    textColor: 'text-rose-700',
    borderColor: 'border-rose-200',
    barColor: 'bg-rose-500',
    ringColor: 'ring-rose-100',
    badgeBg: 'bg-rose-100',
  },
  NOT_ENOUGH_EVIDENCE: {
    icon: AlertTriangle,
    label: 'Not Enough Evidence',
    bgColor: 'bg-amber-50',
    textColor: 'text-amber-700',
    borderColor: 'border-amber-200',
    barColor: 'bg-amber-500',
    ringColor: 'ring-amber-100',
    badgeBg: 'bg-amber-100',
  },
};

function ConfidenceMeter({ confidence, barColor }) {
  const [animatedValue, setAnimatedValue] = useState(0);
  const pct = Math.round(confidence * 100);

  useEffect(() => {
    const timer = setTimeout(() => setAnimatedValue(pct), 100);
    return () => clearTimeout(timer);
  }, [pct]);

  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
          Confidence
        </span>
        <span className="text-sm font-bold text-slate-700 tabular-nums">{pct}%</span>
      </div>
      <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${barColor}`}
          initial={{ width: 0 }}
          animate={{ width: `${animatedValue}%` }}
          transition={{ duration: 1, ease: 'easeOut', delay: 0.2 }}
        />
      </div>
    </div>
  );
}

export default function ResultCard({ result }) {
  const verdict = result.verdict || 'NOT_ENOUGH_EVIDENCE';
  const config = verdictConfig[verdict] || verdictConfig.NOT_ENOUGH_EVIDENCE;
  const Icon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className={`bg-white rounded-2xl shadow-sm border ${config.borderColor} overflow-hidden`}
    >
      {/* Top accent bar */}
      <div className={`h-1 ${config.barColor}`} />

      <div className="p-6 sm:p-8">
        {/* Verdict Badge */}
        <div className="flex flex-wrap items-center gap-3 mb-5">
          <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-xl ${config.badgeBg} ${config.textColor} ring-1 ${config.ringColor}`}>
            <Icon className="w-5 h-5" />
            <span className="font-bold text-sm">{config.label}</span>
          </div>
          {result.model_version && (
            <div className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-50 text-slate-500 text-xs font-medium rounded-lg border border-slate-100">
              <Cpu className="w-3 h-3" />
              {result.model_version}
            </div>
          )}
        </div>

        {/* Claim */}
        <div className="mb-5">
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
            Claim
          </p>
          <p className="text-slate-800 font-medium leading-relaxed">
            {result.claim}
          </p>
        </div>

        {/* Confidence */}
        {result.confidence != null && (
          <div className="mb-5">
            <ConfidenceMeter confidence={result.confidence} barColor={config.barColor} />
          </div>
        )}

        {/* Explanation */}
        {result.explanation && (
          <div className={`${config.bgColor} rounded-xl p-4 border ${config.borderColor}`}>
            <div className="flex gap-2.5">
              <Info className={`w-4 h-4 mt-0.5 flex-shrink-0 ${config.textColor}`} />
              <p className="text-sm text-slate-700 leading-relaxed">
                {result.explanation}
              </p>
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
}
