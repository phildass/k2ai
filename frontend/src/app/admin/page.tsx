'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface QAPair {
  id: number;
  question: string;
  answer: string;
}

export default function AdminPage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');
  const [loginError, setLoginError] = useState('');
  
  const [qaPairs, setQaPairs] = useState<QAPair[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const [newQuestion, setNewQuestion] = useState('');
  const [newAnswer, setNewAnswer] = useState('');
  
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editQuestion, setEditQuestion] = useState('');
  const [editAnswer, setEditAnswer] = useState('');

  // Check for stored token on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('adminToken');
    if (storedToken) {
      setToken(storedToken);
      setIsAuthenticated(true);
      fetchQAPairs(storedToken);
    }
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError('');
    
    try {
      const response = await axios.post(`${API_URL}/api/admin/login`, {
        password: password
      });
      
      if (response.data.success) {
        const authToken = response.data.token;
        setToken(authToken);
        setIsAuthenticated(true);
        localStorage.setItem('adminToken', authToken);
        fetchQAPairs(authToken);
      } else {
        setLoginError(response.data.message || 'Invalid password');
      }
    } catch (err: any) {
      setLoginError(err.response?.data?.message || 'Login failed');
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setToken('');
    setPassword('');
    localStorage.removeItem('adminToken');
    setQaPairs([]);
  };

  const fetchQAPairs = async (authToken: string) => {
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.get(`${API_URL}/api/admin/qa`, {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      });
      setQaPairs(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch Q&A pairs');
      if (err.response?.status === 401) {
        handleLogout();
      }
    } finally {
      setLoading(false);
    }
  };

  const handleAddQA = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!newQuestion.trim() || !newAnswer.trim()) {
      setError('Question and answer are required');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      await axios.post(
        `${API_URL}/api/admin/qa`,
        {
          question: newQuestion,
          answer: newAnswer
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      setNewQuestion('');
      setNewAnswer('');
      fetchQAPairs(token);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to add Q&A pair');
    } finally {
      setLoading(false);
    }
  };

  const handleStartEdit = (qa: QAPair) => {
    setEditingId(qa.id);
    setEditQuestion(qa.question);
    setEditAnswer(qa.answer);
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditQuestion('');
    setEditAnswer('');
  };

  const handleUpdateQA = async (id: number) => {
    if (!editQuestion.trim() || !editAnswer.trim()) {
      setError('Question and answer are required');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      await axios.put(
        `${API_URL}/api/admin/qa/${id}`,
        {
          question: editQuestion,
          answer: editAnswer
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      setEditingId(null);
      setEditQuestion('');
      setEditAnswer('');
      fetchQAPairs(token);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update Q&A pair');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteQA = async (id: number) => {
    if (!confirm('Are you sure you want to delete this Q&A pair?')) {
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      await axios.delete(`${API_URL}/api/admin/qa/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      fetchQAPairs(token);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete Q&A pair');
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4">
        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2 text-center">Admin Login</h1>
          <p className="text-gray-600 mb-6 text-center">K2 Communications AI Assistant</p>
          
          <form onSubmit={handleLogin}>
            <div className="mb-4">
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter admin password"
                required
              />
            </div>
            
            {loginError && (
              <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
                {loginError}
              </div>
            )}
            
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Login
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Admin Panel</h1>
            <p className="text-gray-600">Manage Q&A Pairs</p>
          </div>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Logout
          </button>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Add New Q&A Form */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Add New Q&A Pair</h2>
          <form onSubmit={handleAddQA}>
            <div className="mb-4">
              <label htmlFor="question" className="block text-sm font-medium text-gray-700 mb-2">
                Question or Phrase
              </label>
              <input
                type="text"
                id="question"
                value={newQuestion}
                onChange={(e) => setNewQuestion(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter the question..."
                required
              />
            </div>
            
            <div className="mb-4">
              <label htmlFor="answer" className="block text-sm font-medium text-gray-700 mb-2">
                AI Response
              </label>
              <textarea
                id="answer"
                value={newAnswer}
                onChange={(e) => setNewAnswer(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[100px]"
                placeholder="Enter the response..."
                required
              />
            </div>
            
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {loading ? 'Adding...' : 'Add Q&A Pair'}
            </button>
          </form>
        </div>

        {/* Q&A Pairs List */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">
            Current Q&A Pairs ({qaPairs.length})
          </h2>
          
          {loading && qaPairs.length === 0 ? (
            <p className="text-gray-500 text-center py-8">Loading...</p>
          ) : qaPairs.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No Q&A pairs yet. Add your first one above!</p>
          ) : (
            <div className="space-y-4">
              {qaPairs.map((qa) => (
                <div key={qa.id} className="border border-gray-200 rounded-lg p-4">
                  {editingId === qa.id ? (
                    // Edit mode
                    <div>
                      <div className="mb-3">
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Question
                        </label>
                        <input
                          type="text"
                          value={editQuestion}
                          onChange={(e) => setEditQuestion(e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                      <div className="mb-3">
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Answer
                        </label>
                        <textarea
                          value={editAnswer}
                          onChange={(e) => setEditAnswer(e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[80px]"
                        />
                      </div>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleUpdateQA(qa.id)}
                          disabled={loading}
                          className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors disabled:opacity-50"
                        >
                          Save
                        </button>
                        <button
                          onClick={handleCancelEdit}
                          className="px-4 py-2 bg-gray-400 text-white rounded hover:bg-gray-500 transition-colors"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    // View mode
                    <div>
                      <div className="mb-2">
                        <span className="text-xs font-semibold text-gray-500 uppercase">Question</span>
                        <p className="text-gray-900 font-medium">{qa.question}</p>
                      </div>
                      <div className="mb-3">
                        <span className="text-xs font-semibold text-gray-500 uppercase">Answer</span>
                        <p className="text-gray-700 whitespace-pre-wrap">{qa.answer}</p>
                      </div>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleStartEdit(qa)}
                          className="px-4 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDeleteQA(qa.id)}
                          disabled={loading}
                          className="px-4 py-2 bg-red-600 text-white text-sm rounded hover:bg-red-700 transition-colors disabled:opacity-50"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
