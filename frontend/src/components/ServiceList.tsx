'use client';

import type { Service } from '@/types';

interface ServiceListProps {
  services: Service[];
  loading: boolean;
}

export default function ServiceList({ services, loading }: ServiceListProps) {
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-semibold mb-4">Our Services</h3>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-3 bg-gray-200 rounded w-full"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-h-[600px] overflow-y-auto">
      <h3 className="text-xl font-semibold mb-4 sticky top-0 bg-white pb-2">Our Services</h3>
      <div className="space-y-4">
        {services.map((service) => (
          <div
            key={service.id}
            className="border border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors cursor-pointer"
          >
            <h4 className="font-semibold text-gray-900 mb-2">{service.name}</h4>
            <p className="text-sm text-gray-600 mb-3">{service.description}</p>
            
            {service.key_features && service.key_features.length > 0 && (
              <div className="mb-2">
                <p className="text-xs font-medium text-gray-700 mb-1">Key Features:</p>
                <ul className="text-xs text-gray-600 space-y-1">
                  {service.key_features.slice(0, 3).map((feature, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-blue-600 mr-1">•</span>
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            <button className="text-sm text-blue-600 hover:text-blue-700 font-medium mt-2">
              Learn more →
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
