import React, { useState, useEffect } from 'react';
import { Upload, Download, AlertCircle, CheckCircle, Loader } from 'lucide-react';

const API_BASE = 'http://34.229.168.102:8000/api';

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [selected, setSelected] = useState(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const res = await fetch(`${API_BASE}/jobs`);
        const data = await res.json();
        setJobs(data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)));
      } catch (err) {
        console.error('Error:', err);
      }
    };

    fetchJobs();
    const interval = setInterval(fetchJobs, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    const form = new FormData();
    form.append('file', file);

    try {
      const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: form });
      const data = await res.json();
      setSelected(data.job_id);
    } catch (err) {
      alert('Upload failed: ' + err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <header className="bg-slate-900 border-b border-slate-700 p-6">
        <h1 className="text-3xl font-bold text-cyan-400">🎬 SceneWeave</h1>
        <p className="text-slate-400">Text-to-Video Generation</p>
      </header>

      <main className="max-w-5xl mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Upload */}
          <div className="lg:col-span-1">
            <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
              <h2 className="text-xl font-bold mb-4">Upload Story</h2>
              <label className="flex flex-col items-center justify-center w-full p-8 border-2 border-dashed border-slate-600 rounded-lg cursor-pointer hover:border-cyan-500 transition">
                <Upload className="w-8 h-8 text-cyan-400 mb-2" />
                <span className="text-sm text-slate-300">Click to upload .txt</span>
                <input type="file" accept=".txt" onChange={handleUpload} className="hidden" disabled={uploading} />
              </label>
              {uploading && <p className="text-cyan-400 mt-2 text-sm animate-pulse">Processing...</p>}
            </div>
          </div>

          {/* Jobs */}
          <div className="lg:col-span-2">
            <div className="bg-slate-800 border border-slate-700 rounded-lg overflow-hidden">
              <div className="bg-slate-900 px-6 py-3 border-b border-slate-700">
                <h2 className="font-bold">Jobs ({jobs.length})</h2>
              </div>
              <div className="divide-y divide-slate-700 max-h-96 overflow-y-auto">
                {jobs.length === 0 ? (
                  <div className="p-8 text-center text-slate-400">No jobs yet</div>
                ) : (
                  jobs.map((job) => (
                    <div key={job.job_id} onClick={() => setSelected(job.job_id)} className={`p-4 cursor-pointer hover:bg-slate-700/50 ${selected === job.job_id ? 'bg-slate-700/30 border-l-4 border-cyan-500' : ''}`}>
                      <div className="flex justify-between items-start mb-2">
                        <div className="flex-1">
                          <p className="font-semibold truncate">{job.filename}</p>
                          <p className="text-xs text-slate-400">{job.message || 'Processing...'}</p>
                        </div>
                        {job.status === 'completed' && job.output_file && (
                          <button onClick={(e) => { e.stopPropagation(); window.open(`${API_BASE}/download/${job.job_id}`, '_blank'); }} className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm ml-2">Download</button>
                        )}
                      </div>
                      <div className="bg-slate-700 rounded-full h-2">
                        <div className="bg-cyan-500 h-full" style={{ width: `${job.progress || 0}%` }} />
                      </div>
                      <p className="text-xs text-slate-400 mt-1">{job.progress}% • {job.status}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
