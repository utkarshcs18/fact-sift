import { motion } from 'framer-motion';
import { BarChart3, CheckCircle2, XCircle, AlertTriangle } from 'lucide-react';
import { useEffect, useState } from 'react';

function AnimatedCount({ target, duration = 600 }) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    if (target === 0) { setCount(0); return; }
    let start = 0;
    const step = Math.max(1, Math.ceil(target / (duration / 16)));
    const timer = setInterval(() => {
      start += step;
      if (start >= target) {
        setCount(target);
        clearInterval(timer);
      } else {
        setCount(start);
      }
    }, 16);
    return () => clearInterval(timer);
  }, [target, duration]);

  return <span className="tabular-nums">{count}</span>;
}

const stats = [
  {
    key: 'total',
    label: 'Analyzed',
    icon: BarChart3,
    iconColor: 'text-indigo-500',
    iconBg: 'bg-indigo-50',
  },
  {
    key: 'supports',
    label: 'Supports',
    icon: CheckCircle2,
    iconColor: 'text-emerald-500',
    iconBg: 'bg-emerald-50',
  },
  {
    key: 'refutes',
    label: 'Refutes',
    icon: XCircle,
    iconColor: 'text-rose-500',
    iconBg: 'bg-rose-50',
  },
  {
    key: 'notEnough',
    label: 'Insufficient',
    icon: AlertTriangle,
    iconColor: 'text-amber-500',
    iconBg: 'bg-amber-50',
  },
];

export default function StatsBar({ stats: data }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-3xl mx-auto mb-8"
    >
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div
              key={stat.key}
              className="bg-white rounded-xl border border-slate-100 shadow-sm px-4 py-3 flex items-center gap-3 hover:shadow-md transition-shadow duration-200"
            >
              <div className={`p-2 rounded-lg ${stat.iconBg}`}>
                <Icon className={`w-4 h-4 ${stat.iconColor}`} />
              </div>
              <div>
                <p className="text-xl font-bold text-slate-800">
                  <AnimatedCount target={data[stat.key] || 0} />
                </p>
                <p className="text-xs text-slate-400 font-medium">{stat.label}</p>
              </div>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}
