import { Github, Heart } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-slate-100 bg-white mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-sm text-slate-400">
            <span>Built with</span>
            <Heart className="w-3.5 h-3.5 text-rose-400 fill-rose-400" />
            <span>using React, Tailwind CSS & FastAPI</span>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              {['React', 'Tailwind', 'FastAPI', 'PyTorch'].map((tech) => (
                <span
                  key={tech}
                  className="px-2.5 py-1 text-xs font-medium text-slate-400 bg-slate-50 rounded-md border border-slate-100"
                >
                  {tech}
                </span>
              ))}
            </div>
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 text-slate-400 hover:text-slate-700 hover:bg-slate-50 rounded-lg transition-all"
              title="GitHub"
            >
              <Github className="w-4 h-4" />
            </a>
          </div>
        </div>

        <div className="mt-4 text-center">
          <p className="text-xs text-slate-300">
            © 2026 Fact-Sift. Evidence-based claim verification system.
          </p>
        </div>
      </div>
    </footer>
  );
}
