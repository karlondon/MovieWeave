import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Zap, Lock, BarChart3 } from 'lucide-react';

export default function Hero() {
  return (
    <div className="min-h-[calc(100vh-64px)] flex flex-col justify-center items-center px-4 py-20">
      <div className="max-w-4xl mx-auto text-center space-y-8 animate-fade-in">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-500/10 border border-indigo-500/20 rounded-full">
          <span className="w-2 h-2 bg-indigo-500 rounded-full animate-pulse"></span>
          <span className="text-sm text-indigo-300">AI-Powered Video Generation</span>
        </div>

        {/* Main Title */}
        <h1 className="text-5xl md:text-7xl font-bold leading-tight">
          Transform <span className="gradient-text">Books into Videos</span>
        </h1>

        {/* Subtitle */}
        <p className="text-xl md:text-2xl text-slate-300 max-w-2xl mx-auto">
          Turn your novels and stories into stunning animated videos using AI. Upload a PDF, get professional-quality animations in minutes.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-8">
          <Link to="/dashboard" className="btn-primary inline-flex items-center justify-center gap-2">
            Start Creating
            <ArrowRight size={20} />
          </Link>
          <Link to="/pricing" className="btn-secondary inline-flex items-center justify-center gap-2">
            View Pricing
          </Link>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 pt-16">
          <div className="space-y-2">
            <div className="text-3xl font-bold text-indigo-400">5 Free</div>
            <p className="text-slate-400">Videos per month</p>
          </div>
          <div className="space-y-2">
            <div className="text-3xl font-bold text-purple-400">2-5 min</div>
            <p className="text-slate-400">Processing time</p>
          </div>
          <div className="space-y-2">
            <div className="text-3xl font-bold text-pink-400">AI-Powered</div>
            <p className="text-slate-400">Advanced animations</p>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-16">
          <div className="card-hover p-6 bg-slate-800/50 border border-slate-700/50 rounded-xl">
            <Zap className="w-8 h-8 text-indigo-500 mb-4" />
            <h3 className="text-lg font-semibold mb-2">Lightning Fast</h3>
            <p className="text-slate-400">Get your animations in minutes, not hours</p>
          </div>
          <div className="card-hover p-6 bg-slate-800/50 border border-slate-700/50 rounded-xl">
            <Lock className="w-8 h-8 text-purple-500 mb-4" />
            <h3 className="text-lg font-semibold mb-2">Secure & Private</h3>
            <p className="text-slate-400">Your content is encrypted and private</p>
          </div>
          <div className="card-hover p-6 bg-slate-800/50 border border-slate-700/50 rounded-xl">
            <BarChart3 className="w-8 h-8 text-pink-500 mb-4" />
            <h3 className="text-lg font-semibold mb-2">Track Progress</h3>
            <p className="text-slate-400">Monitor your video generation in real-time</p>
          </div>
          <div className="card-hover p-6 bg-slate-800/50 border border-slate-700/50 rounded-xl">
            <ArrowRight className="w-8 h-8 text-indigo-500 mb-4" />
            <h3 className="text-lg font-semibold mb-2">Easy Download</h3>
            <p className="text-slate-400">Download and share your videos instantly</p>
          </div>
        </div>
      </div>
    </div>
  );
}
