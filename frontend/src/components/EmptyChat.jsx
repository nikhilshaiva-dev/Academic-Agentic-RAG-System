import React from 'react';
import { 
  GraduationCap, 
  CalendarCheck, 
  Trophy, 
  AlertTriangle, 
  FileText, 
  TrendingUp,
  ArrowRight
} from 'lucide-react';

const SUGGESTED_PROMPTS = [
  {
    title: "Student Attendance",
    query: "Show attendance of STU0050",
    category: "Attendance",
    icon: CalendarCheck,
    color: "from-blue-500/10 to-indigo-500/10 text-blue-600 dark:text-blue-400 border-blue-200/60 dark:border-blue-900/40"
  },
  {
    title: "Academic Performance",
    query: "Show performance of STU0050",
    category: "Performance",
    icon: TrendingUp,
    color: "from-emerald-500/10 to-teal-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-200/60 dark:border-emerald-900/40"
  },
  {
    title: "Leaderboard Analytics",
    query: "Who are the top 10 students?",
    category: "Analytics",
    icon: Trophy,
    color: "from-amber-500/10 to-orange-500/10 text-amber-600 dark:text-amber-400 border-amber-200/60 dark:border-amber-900/40"
  },
  {
    title: "Risk Detection",
    query: "Find students at risk",
    category: "Alerts",
    icon: AlertTriangle,
    color: "from-rose-500/10 to-red-500/10 text-rose-600 dark:text-rose-400 border-rose-200/60 dark:border-rose-900/40"
  },
  {
    title: "University Policy RAG",
    query: "Explain the attendance policy",
    category: "Policy",
    icon: FileText,
    color: "from-purple-500/10 to-violet-500/10 text-purple-600 dark:text-purple-400 border-purple-200/60 dark:border-purple-900/40"
  }
];

export default function EmptyChat({ onSelectPrompt }) {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-6 max-w-3xl mx-auto text-center">
      {/* Icon and Branding */}
      <div className="w-16 h-16 mb-5 rounded-2xl bg-gradient-to-tr from-brand-600 via-indigo-600 to-violet-600 flex items-center justify-center text-white shadow-lg shadow-brand-500/20">
        <GraduationCap className="w-9 h-9" />
      </div>

      <h2 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-2 tracking-tight">
        How can I help you today?
      </h2>

      <p className="text-sm md:text-base text-gray-600 dark:text-gray-400 max-w-xl mb-8 leading-relaxed">
        Ask me anything about student performance, attendance, academic records, and university policies.
      </p>

      {/* Suggested prompt grid */}
      <div className="w-full grid grid-cols-1 sm:grid-cols-2 gap-3 text-left">
        {SUGGESTED_PROMPTS.map((item, idx) => {
          const Icon = item.icon;
          return (
            <button
              key={idx}
              onClick={() => onSelectPrompt(item.query)}
              className="group p-3.5 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-800/80 hover:border-brand-300 dark:hover:border-brand-700 hover:shadow-md transition-all duration-200 flex items-start justify-between text-left cursor-pointer"
            >
              <div className="flex items-start space-x-3 min-w-0">
                <div className={`p-2 rounded-lg bg-gradient-to-br ${item.color} border shrink-0`}>
                  <Icon className="w-4 h-4" />
                </div>
                <div className="min-w-0">
                  <div className="flex items-center space-x-2">
                    <span className="text-[11px] font-semibold uppercase tracking-wider text-gray-400 dark:text-gray-500">
                      {item.category}
                    </span>
                  </div>
                  <p className="text-sm font-medium text-gray-800 dark:text-gray-200 group-hover:text-brand-600 dark:group-hover:text-brand-400 transition-colors mt-0.5">
                    {item.query}
                  </p>
                </div>
              </div>
              <ArrowRight className="w-4 h-4 text-gray-400 group-hover:text-brand-500 group-hover:translate-x-0.5 transition-all shrink-0 mt-2.5 ml-2" />
            </button>
          );
        })}
      </div>
    </div>
  );
}

