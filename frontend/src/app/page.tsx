'use client';

import { useState, useEffect } from 'react';
import ChatInterface from '@/components/ChatInterface';
import ServiceList from '@/components/ServiceList';
import LeadForm from '@/components/LeadForm';
import { servicesApi } from '@/lib/api';
import type { Service } from '@/types';

export default function Home() {
  const [services, setServices] = useState<Service[]>([]);
  const [showLeadForm, setShowLeadForm] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadServices();
  }, []);

  const loadServices = async () => {
    try {
      const data = await servicesApi.getAll();
      setServices(data);
    } catch (error) {
      console.error('Failed to load services:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">K2 Communications</h1>
              <p className="text-sm text-gray-600">India&apos;s Premier PR Agency</p>
            </div>
            <button
              onClick={() => setShowLeadForm(true)}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Get in Touch
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Chat Interface - Takes 2 columns on large screens */}
          <div className="lg:col-span-2">
            <ChatInterface />
          </div>

          {/* Services Sidebar */}
          <div className="lg:col-span-1">
            <ServiceList services={services} loading={loading} />
          </div>
        </div>
      </div>

      {/* Lead Form Modal */}
      {showLeadForm && (
        <LeadForm onClose={() => setShowLeadForm(false)} />
      )}
    </main>
  );
}
