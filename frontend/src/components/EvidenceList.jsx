import { motion } from 'framer-motion';
import { ExternalLink, ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';

const stanceConfig = {
  SUPPORTS: {
    label: 'Supports',
    bgColor: 'bg-emerald-50',
    textColor: 'text-emerald-700',
    borderColor: 'border-emerald-200',
    dotColor: 'bg-emerald-400',
  },
  REFUTES: {
    label: 'Refutes',
    bgColor: 'bg-rose-50',
    textColor: 'text-rose-700',
    borderColor: 'border-rose-200',
    dotColor: 'bg-rose-400',
  },
  NOT_ENOUGH_INFO: {
    label: 'Neutral',
    bgColor: 'bg-slate-50',
    textColor: 'text-slate-600',
    borderColor: 'border-slate-200',
    dotColor: 'bg-slate-400',
  },
};

function EvidenceCard({ item, index }) {
  const [expanded, setExpanded] = useState(false);
  const stance = item.stance || item.label || 'NOT_ENOUGH_INFO';
  const config = stanceConfig[stance] || stanceConfig.NOT_ENOUGH_INFO;
  const passage = item.passage || item.text || '';
  const isLong = passage.length > 200;

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1, ease: 'easeOut' }}
      className="bg-white rounded-2xl shadow-sm border border-slate-100 hover:shadow-md hover:border-slate-200 transition-all duration-300 overflow-hidden"
    >
      <div className="p-5">
        {/* Header */}
        <div className="flex flex-wrap items-start justify-between gap-2 mb-3">
          <div className="flex items-center gap-2 min-w-0">
            <div className={`w-2 h-2 rounded-full flex-shrink-0 ${config.dotColor}`} />
            <h4 className="text-sm font-semibold text-slate-800 truncate">
              {item.source || item.title || `Evidence ${index + 1}`}
            </h4>
          </div>
          <span
            className={`inline-flex items-center px-2.5 py-1 text-xs font-semibold rounded-lg ${config.bgColor} ${config.textColor} border ${config.borderColor} flex-shrink-0`}
          >
            {config.label}
          </span>
        </div>

        {/* Passage */}
        <p className="text-sm text-slate-600 leading-relaxed">
          {isLong && !expanded ? `${passage.slice(0, 200)}…` : passage}
        </p>

        {isLong && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="flex items-center gap-1 mt-2 text-xs font-medium text-indigo-500 hover:text-indigo-700 transition-colors"
          >
            {expanded ? (
              <>
                Show less <ChevronUp className="w-3 h-3" />
              </>
            ) : (
              <>
                Show more <ChevronDown className="w-3 h-3" />
              </>
            )}
          </button>
        )}

        {/* URL */}
        {item.url && (
          <a
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 mt-3 text-xs font-medium text-indigo-500 hover:text-indigo-700 transition-colors"
          >
            <ExternalLink className="w-3 h-3" />
            View source
          </a>
        )}
      </div>
    </motion.div>
  );
}

export default function EvidenceList({ evidence }) {
  return (
    <motion.section
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4, delay: 0.2 }}
    >
      <div className="flex items-center gap-2 mb-4">
        <h3 className="text-sm font-bold text-slate-700 uppercase tracking-wider">
          Evidence
        </h3>
        <span className="text-xs text-slate-400 font-medium bg-slate-100 px-2 py-0.5 rounded-full">
          {evidence.length} source{evidence.length !== 1 ? 's' : ''}
        </span>
      </div>
      <div className="space-y-3">
        {evidence.map((item, index) => (
          <EvidenceCard key={index} item={item} index={index} />
        ))}
      </div>
    </motion.section>
  );
}
