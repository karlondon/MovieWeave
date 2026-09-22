import React from 'react';
import { Link } from 'react-router-dom';
import { Film, Menu, X } from 'lucide-react';
import { useState } from 'react';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-slate-900/95 backdrop-blur-md border-b border-slate-700/50 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center gap-2 group">
            <Film className="w-8 h-8 text-indigo-500 group-hover:text-purple-500 transition" />
            <span className="text-xl font-bold gradient-text">MovieWeave</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex gap-8">
            <Link to="/" className="text-slate-300 hover:text-white transition">Home</Link>
            <Link to="/dashboard" className="text-slate-300 hover:text-white transition">Dashboard</Link>
            <Link to="/pricing" className="text-slate-300 hover:text-white transition">Pricing</Link>
          </div>

          <Link to="/dashboard" className="hidden md:block btn-primary">
            Get Started
          </Link>

          {/* Mobile Menu Button */}
          <button 
            className="md:hidden text-slate-300"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <div className="md:hidden pb-4 space-y-2">
            <Link to="/" className="block px-4 py-2 text-slate-300 hover:text-white hover:bg-slate-800 rounded">Home</Link>
            <Link to="/dashboard" className="block px-4 py-2 text-slate-300 hover:text-white hover:bg-slate-800 rounded">Dashboard</Link>
            <Link to="/pricing" className="block px-4 py-2 text-slate-300 hover:text-white hover:bg-slate-800 rounded">Pricing</Link>
          </div>
        )}
      </div>
    </nav>
  );
}
