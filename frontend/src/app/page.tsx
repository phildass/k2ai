import ChatInterface from '@/components/ChatInterface';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            K2 Communications AI Assistant
          </h1>
          <p className="text-gray-600">
            Your intelligent PR and communications partner
          </p>
        </div>
        <ChatInterface />
      </div>
    </div>
  );
}
