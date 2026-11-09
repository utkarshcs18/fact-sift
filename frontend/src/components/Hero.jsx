import { motion } from 'framer-motion';
import { Search, Sparkles, ShieldCheck } from 'lucide-react';

export default function Hero() {
  return (
    <section className="pt-16 pb-8 sm:pt-24 sm:pb-12 text-center">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, ease: 'easeOut' }}
        className="max-w-3xl mx-auto"
      >
        <div className="flex items-center justify-center gap-2 mb-6">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-semibold rounded-full border border-indigo-100">
            <Sparkles className="w-3 h-3" />
            AI-Powered Verification
          </span>
        </div>

        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-slate-900 leading-tight">
          Verify Claims with{' '}
          <span className="bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-500 bg-clip-text text-transparent">
            Evidence
          </span>
        </h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.15, ease: 'easeOut' }}
          className="mt-5 text-lg sm:text-xl text-slate-500 leading-relaxed max-w-2xl mx-auto font-light"
        >
          Submit any factual claim and our system retrieves evidence, analyzes it
          with machine learning, and returns a transparent verdict you can trust.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.3, ease: 'easeOut' }}
          className="flex flex-wrap items-center justify-center gap-6 mt-8 text-sm text-slate-400"
        >
          <div className="flex items-center gap-2">
            <Search className="w-4 h-4 text-indigo-400" />
            <span>Evidence Retrieval</span>
          </div>
          <div className="w-1 h-1 rounded-full bg-slate-300 hidden sm:block" />
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>NLI Verification</span>
          </div>
          <div className="w-1 h-1 rounded-full bg-slate-300 hidden sm:block" />
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-amber-400" />
            <span>Confidence Scoring</span>
          </div>
        </motion.div>
      </motion.div>
    </section>
  );
}
