import React, { useState, useEffect } from 'react';
import { Upload, Loader, Music, Film } from 'lucide-react';
import axios from 'axios';

const API_URL = 'https://movieweave.myblognow.uk';

export default function Dashboard() {
  const [file, setFile] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadedCount, setUploadedCount] = useState(0);

  useEffect(() => {
    const count = localStorage.getItem('movieweave_uploads') || '0';
    setUploadedCount(parseInt(count, 10));
    fetchJobs();
    const interval = setInterval(fetchJobs, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await axios.get(`${API_URL}/jobs`);
      if (response.data) {
        const jobsArray = Object.values(response.data);
        jobsArray.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        setJobs(jobsArray);
      }
    } catch (err) {
      console.error('Error fetching jobs:', err);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-GB', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric', 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const handleFileChange = (e) => {
    if (e.target.files?.[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('file', file);
      await axios.post(`${API_URL}/upload`, formData, { 
        headers: { 'Content-Type': 'multipart/form-data' } 
      });
      const newCount = uploadedCount + 1;
      setUploadedCount(newCount);
      localStorage.setItem('movieweave_uploads', newCount.toString());
      setFile(null);
      const fileInput = document.getElementById('file-input');
      if (fileInput) fileInput.value = '';
      await fetchJobs();
    } catch (err) {
      console.error('Upload error:', err);
      setError('Upload failed');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = (jobId, format) => {
    const url = `${API_URL}/download/${jobId}?format=${format}`;
    window.open(url, '_blank');
  };

  const isFree = uploadedCount <= 5;

  return (
    <div className="min-h-[calc(100vh-64px)] py-12 px-4 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-2 text-white">Dashboard</h1>
        <p className="text-slate-400 mb-8">Upload documents and convert to animated videos</p>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          <div className="lg:col-span-2 bg-slate-800/50 border-2 border-dashed border-slate-700 rounded-xl p-8">
            <form onSubmit={handleUpload} className="space-y-6">
              <div className="flex flex-col items-center gap-4 py-8">
                <Upload className="w-12 h-12 text-indigo-500" />
                <label htmlFor="file-input" className="text-center cursor-pointer">
                  <p className="text-lg font-semibold text-white">Click to upload</p>
                  <p className="text-slate-400">or drag and drop</p>
                </label>
                <input id="file-input" type="file" onChange={handleFileChange} className="hidden" />
                <p className="text-sm text-slate-500">PDF, TXT, DOC, DOCX</p>
              </div>
              {file && (
                <div className="bg-slate-700/50 p-4 rounded-lg">
                  <p className="text-sm text-slate-300">Selected: {file.name}</p>
                </div>
              )}
              {error && (
                <div className="bg-red-500/10 border border-red-500/50 text-red-400 p-4 rounded-lg text-sm">
                  {error}
                </div>
              )}
              <button 
                type="submit" 
                disabled={!file || loading} 
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-4 rounded-lg"
              >
                {loading ? 'Processing...' : 'Upload & Convert'}
              </button>
            </form>
          </div>

          <div className="bg-gradient-to-br from-indigo-900/30 to-purple-900/30 border border-indigo-500/20 rounded-xl p-6">
            <h3 className="text-lg font-semibold mb-6 text-white">Your Stats</h3>
            <div className="mb-6">
              <p className="text-slate-400 text-sm">Videos This Month</p>
              <p className="text-4xl font-bold text-indigo-400">{uploadedCount}</p>
            </div>
            <div className="pt-6 border-t border-indigo-500/20">
              <p className="text-slate-400 text-sm mb-2">Download Cost</p>
              <p className="text-3xl font-bold mb-2">{isFree ? 'FREE' : '£5.00'}</p>
              <p className="text-xs text-slate-500">{isFree ? '5 free videos' : 'Premium'}</p>
            </div>
          </div>
        </div>

        <h2 className="text-2xl font-bold mb-6 text-white">Your Conversions</h2>
        {jobs.length === 0 ? (
          <div className="bg-slate-800/30 border border-slate-700/50 rounded-xl p-12 text-center">
            <p className="text-slate-400">No conversions yet</p>
          </div>
        ) : (
          <div className="space-y-4">
            {jobs.map((job) => (
              <div key={job.job_id} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 flex justify-between items-center">
                <div>
                  <h3 className="font-semibold text-white">{job.filename}</h3>
                  <div className="flex items-center gap-4 mt-2">
                    <span className={`text-sm font-medium ${job.status === 'completed' ? 'text-green-400' : 'text-blue-400'}`}>
                      {job.status.toUpperCase()} {job.status === 'processing' && `(${job.progress}%)`}
                    </span>
                    <span className="text-xs text-slate-500">{formatDate(job.created_at)}</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  {job.status === 'completed' && (
                    <>
                      <button onClick={() => handleDownload(job.job_id, 'mp4')} className="bg-indigo-600 hover:bg-indigo-700 text-white py-2 px-3 rounded-lg flex items-center gap-2 text-sm">
                        <Film className="w-4 h-4" /> MP4
                      </button>
                      <button onClick={() => handleDownload(job.job_id, 'mp3')} className="bg-purple-600 hover:bg-purple-700 text-white py-2 px-3 rounded-lg flex items-center gap-2 text-sm">
                        <Music className="w-4 h-4" /> MP3
                      </button>
                    </>
                  )}
                  {job.status === 'processing' && <Loader className="w-5 h-5 animate-spin text-blue-400" />}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
