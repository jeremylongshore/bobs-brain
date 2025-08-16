import React, { useState, useEffect } from 'react';
import { Database, AlertCircle, Tool, Truck, DollarSign, Activity } from 'lucide-react';

const Neo4jDashboard = () => {
  const [showEmbedded, setShowEmbedded] = useState(false);
  const [stats, setStats] = useState({
    equipment: 15,
    errorCodes: 38,
    parts: 20,
    problems: 35,
    repairCases: 3,
    totalNodes: 258
  });

  const NEO4J_CONSOLE_URL = 'https://console.neo4j.io';
  const NEO4J_URI = 'neo4j+s://d3653283.databases.neo4j.io';

  const sampleQueries = [
    {
      title: 'Find all equipment',
      query: 'MATCH (e:Equipment) RETURN e'
    },
    {
      title: 'Error codes for Ford trucks',
      query: `MATCH (e:Equipment)-[:THROWS_CODE]->(c:ErrorCode)
WHERE e.brand = 'Ford'
RETURN e.model, c.code, c.description`
    },
    {
      title: 'Expensive parts (>$1000)',
      query: 'MATCH (p:Part) WHERE p.price > 1000 RETURN p ORDER BY p.price DESC'
    },
    {
      title: 'Complete repair paths',
      query: `MATCH path = (e:Equipment)-[:THROWS_CODE]->(c:ErrorCode)<-[:CAUSES]-(p:Problem)<-[:FIXES]-(part:Part)
RETURN path`
    }
  ];

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-500 to-purple-800 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-xl shadow-xl p-8 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2">
                StartAI Tools - Equipment Knowledge Graph
              </h1>
              <p className="text-gray-600">
                <span className="inline-block w-2 h-2 bg-green-500 rounded-full animate-pulse mr-2"></span>
                Neo4j Connected | {stats.totalNodes} Nodes | Real-time Knowledge Base
              </p>
            </div>
            <Database className="w-12 h-12 text-purple-600" />
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <Truck className="w-8 h-8 text-blue-500" />
              <span className="text-3xl font-bold text-gray-800">{stats.equipment}</span>
            </div>
            <h3 className="font-semibold text-gray-700">Equipment</h3>
            <p className="text-sm text-gray-500">Bobcat, Ford, Ram, GMC</p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <AlertCircle className="w-8 h-8 text-red-500" />
              <span className="text-3xl font-bold text-gray-800">{stats.errorCodes}</span>
            </div>
            <h3 className="font-semibold text-gray-700">Error Codes</h3>
            <p className="text-sm text-gray-500">P0087, P0299, P0191...</p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <Tool className="w-8 h-8 text-green-500" />
              <span className="text-3xl font-bold text-gray-800">{stats.parts}</span>
            </div>
            <h3 className="font-semibold text-gray-700">Parts</h3>
            <p className="text-sm text-gray-500">$85 - $3,800 range</p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <DollarSign className="w-8 h-8 text-yellow-500" />
              <span className="text-3xl font-bold text-gray-800">{stats.repairCases}</span>
            </div>
            <h3 className="font-semibold text-gray-700">Repair Cases</h3>
            <p className="text-sm text-gray-500">With cost data</p>
          </div>
        </div>

        {/* Neo4j Access Section */}
        <div className="bg-white rounded-xl shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">🔗 Neo4j Access</h2>

          <div className="flex flex-wrap gap-4 mb-6">
            <a
              href={NEO4J_CONSOLE_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors flex items-center gap-2"
            >
              <Database className="w-5 h-5" />
              Open Neo4j Console
            </a>

            <button
              onClick={() => setShowEmbedded(!showEmbedded)}
              className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
            >
              <Activity className="w-5 h-5" />
              {showEmbedded ? 'Hide' : 'Show'} Embedded View
            </button>

            <button
              onClick={() => copyToClipboard(NEO4J_URI)}
              className="px-6 py-3 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors"
            >
              Copy Connection URI
            </button>
          </div>

          {/* Connection Details */}
          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <h3 className="font-semibold text-gray-700 mb-2">Connection Details:</h3>
            <code className="text-sm bg-gray-800 text-green-400 p-2 rounded block">
              URI: {NEO4J_URI}<br />
              User: neo4j<br />
              Database: neo4j
            </code>
          </div>

          {/* Sample Queries */}
          <div className="mb-6">
            <h3 className="font-semibold text-gray-700 mb-4">Sample Queries:</h3>
            <div className="space-y-3">
              {sampleQueries.map((sq, idx) => (
                <div key={idx} className="bg-gray-50 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-medium text-gray-700">{sq.title}</h4>
                    <button
                      onClick={() => copyToClipboard(sq.query)}
                      className="text-sm text-blue-600 hover:text-blue-800"
                    >
                      Copy
                    </button>
                  </div>
                  <pre className="text-sm bg-gray-800 text-green-400 p-3 rounded overflow-x-auto">
                    {sq.query}
                  </pre>
                </div>
              ))}
            </div>
          </div>

          {/* Embedded Neo4j */}
          {showEmbedded && (
            <div className="border-2 border-gray-300 rounded-lg overflow-hidden" style={{ height: '600px' }}>
              <iframe
                src={NEO4J_CONSOLE_URL}
                className="w-full h-full"
                title="Neo4j Console"
              />
            </div>
          )}
        </div>

        {/* Data Sources */}
        <div className="bg-white rounded-xl shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">📡 Live Data Sources</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-purple-50 rounded-lg p-6">
              <h3 className="font-semibold text-purple-800 mb-2">YouTube Channels</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Pine Hollow Auto Diagnostics</li>
                <li>• Scanner Danner</li>
                <li>• FarmCraft101</li>
                <li>• Diesel Tech Ron</li>
              </ul>
            </div>

            <div className="bg-blue-50 rounded-lg p-6">
              <h3 className="font-semibold text-blue-800 mb-2">Reddit Communities</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• r/MechanicAdvice</li>
                <li>• r/Diesel</li>
                <li>• r/Skidsteers</li>
                <li>• r/Powerstroke</li>
              </ul>
            </div>

            <div className="bg-green-50 rounded-lg p-6">
              <h3 className="font-semibold text-green-800 mb-2">Equipment Forums</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• BobcatForum.com</li>
                <li>• TractorByNet.com</li>
                <li>• DieselTruckResource.com</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Neo4jDashboard;
