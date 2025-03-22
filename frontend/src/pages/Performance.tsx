import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import { ThumbsUpIcon, ThumbsDownIcon, MessageSquareIcon, Share2Icon, DollarSignIcon } from 'lucide-react';
// Mock performance data
const performanceData = {
  campaignName: 'Summer Collection Launch',
  totalEngagements: 125750,
  conversions: 3240,
  revenue: 52680,
  roi: 315,
  influencers: [{
    id: 1,
    name: 'Sarah Johnson',
    username: '@sarahjbeauty',
    profileImage: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330',
    content: [{
      id: 1,
      type: 'image',
      thumbnail: 'https://images.unsplash.com/photo-1511707171634-5f897ff02ff9',
      likes: 45200,
      comments: 1200,
      shares: 850,
      views: 120000,
      conversions: 1250
    }, {
      id: 2,
      type: 'video',
      thumbnail: 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f',
      likes: 32800,
      comments: 980,
      shares: 1200,
      views: 98000,
      conversions: 890
    }]
  }, {
    id: 2,
    name: 'Alex Chen',
    username: '@alexchentech',
    profileImage: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d',
    content: [{
      id: 3,
      type: 'video',
      thumbnail: 'https://images.unsplash.com/photo-1523206489230-c012c64b2b48',
      likes: 28500,
      comments: 1500,
      shares: 950,
      views: 85000,
      conversions: 720
    }]
  }]
};
// Engagement data for charts
const engagementData = [{
  day: 'Day 1',
  likes: 12500,
  comments: 850,
  shares: 320
}, {
  day: 'Day 2',
  likes: 18700,
  comments: 1200,
  shares: 450
}, {
  day: 'Day 3',
  likes: 22400,
  comments: 1350,
  shares: 580
}, {
  day: 'Day 4',
  likes: 19800,
  comments: 980,
  shares: 410
}, {
  day: 'Day 5',
  likes: 24600,
  comments: 1450,
  shares: 620
}, {
  day: 'Day 6',
  likes: 27800,
  comments: 1680,
  shares: 750
}];
const conversionData = [{
  day: 'Day 1',
  conversions: 380,
  views: 35000
}, {
  day: 'Day 2',
  conversions: 420,
  views: 42000
}, {
  day: 'Day 3',
  conversions: 510,
  views: 48000
}, {
  day: 'Day 4',
  conversions: 580,
  views: 52000
}, {
  day: 'Day 5',
  conversions: 650,
  views: 58000
}, {
  day: 'Day 6',
  conversions: 700,
  views: 62000
}];
const Performance = () => {
  const [selectedContent, setSelectedContent] = useState(null);
  const [feedback, setFeedback] = useState('');
  const handleFeedbackSubmit = contentId => {
    // In a real app, this would send the feedback
    setFeedback('');
    // Show success notification
  };
  return <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">
        Influencer Performance
      </h1>
      {/* Campaign Overview */}
      <div className="bg-white rounded-lg shadow overflow-hidden mb-8">
        <div className="px-6 py-5 border-b">
          <h2 className="text-xl font-semibold text-gray-800">
            {performanceData.campaignName}
          </h2>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-blue-100 text-blue-600 mr-4">
                  <ThumbsUpIcon className="w-6 h-6" />
                </div>
                <div>
                  <p className="text-sm font-medium text-blue-600">
                    Total Engagements
                  </p>
                  <p className="text-2xl font-bold text-blue-800">
                    {performanceData.totalEngagements.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
            <div className="bg-green-50 rounded-lg p-4">
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-green-100 text-green-600 mr-4">
                  <Share2Icon className="w-6 h-6" />
                </div>
                <div>
                  <p className="text-sm font-medium text-green-600">
                    Conversions
                  </p>
                  <p className="text-2xl font-bold text-green-800">
                    {performanceData.conversions.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
            <div className="bg-purple-50 rounded-lg p-4">
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-purple-100 text-purple-600 mr-4">
                  <DollarSignIcon className="w-6 h-6" />
                </div>
                <div>
                  <p className="text-sm font-medium text-purple-600">Revenue</p>
                  <p className="text-2xl font-bold text-purple-800">
                    ${performanceData.revenue.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
            <div className="bg-amber-50 rounded-lg p-4">
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-amber-100 text-amber-600 mr-4">
                  <DollarSignIcon className="w-6 h-6" />
                </div>
                <div>
                  <p className="text-sm font-medium text-amber-600">ROI</p>
                  <p className="text-2xl font-bold text-amber-800">
                    {performanceData.roi}%
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* Performance Charts */}
      <div className="bg-white rounded-lg shadow overflow-hidden mb-8">
        <div className="px-6 py-5 border-b">
          <h2 className="text-xl font-semibold text-gray-800">
            Performance Metrics
          </h2>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <h3 className="text-lg font-medium text-gray-700 mb-4">
                Engagement Over Time
              </h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={engagementData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="day" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="likes" fill="#3b82f6" name="Likes" />
                    <Bar dataKey="comments" fill="#10b981" name="Comments" />
                    <Bar dataKey="shares" fill="#8b5cf6" name="Shares" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-700 mb-4">
                Conversions & Views
              </h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={conversionData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="day" />
                    <YAxis yAxisId="left" />
                    <YAxis yAxisId="right" orientation="right" />
                    <Tooltip />
                    <Legend />
                    <Line yAxisId="left" type="monotone" dataKey="conversions" stroke="#ef4444" name="Conversions" />
                    <Line yAxisId="right" type="monotone" dataKey="views" stroke="#f59e0b" name="Views" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* Influencer Content */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-5 border-b">
          <h2 className="text-xl font-semibold text-gray-800">
            Influencer Content
          </h2>
        </div>
        <div className="p-6">
          {performanceData.influencers.map(influencer => <div key={influencer.id} className="mb-8 last:mb-0">
              <div className="flex items-center mb-4">
                <img src={`${influencer.profileImage}?auto=format&fit=crop&w=60&h=60`} alt={influencer.name} className="w-12 h-12 rounded-full mr-4" />
                <div>
                  <h3 className="font-medium text-gray-900">
                    {influencer.name}
                  </h3>
                  <p className="text-sm text-gray-500">{influencer.username}</p>
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {influencer.content.map(content => <div key={content.id} className="border rounded-lg overflow-hidden">
                    <div className="aspect-w-16 aspect-h-9 bg-gray-100">
                      <img src={`${content.thumbnail}?auto=format&fit=crop&w=800&h=450`} alt="Content thumbnail" className="object-cover w-full h-full" />
                      {content.type === 'video' && <div className="absolute inset-0 flex items-center justify-center">
                          <div className="w-16 h-16 bg-black bg-opacity-60 rounded-full flex items-center justify-center">
                            <div className="w-0 h-0 border-t-8 border-t-transparent border-l-12 border-l-white border-b-8 border-b-transparent ml-1"></div>
                          </div>
                        </div>}
                    </div>
                    <div className="p-4">
                      <div className="flex flex-wrap gap-4 mb-4">
                        <div className="flex items-center text-gray-600">
                          <ThumbsUpIcon className="w-4 h-4 mr-1" />
                          <span>{content.likes.toLocaleString()}</span>
                        </div>
                        <div className="flex items-center text-gray-600">
                          <MessageSquareIcon className="w-4 h-4 mr-1" />
                          <span>{content.comments.toLocaleString()}</span>
                        </div>
                        <div className="flex items-center text-gray-600">
                          <Share2Icon className="w-4 h-4 mr-1" />
                          <span>{content.shares.toLocaleString()}</span>
                        </div>
                      </div>
                      <div className="mb-4">
                        <div className="flex justify-between text-sm mb-1">
                          <span className="font-medium text-gray-700">
                            Performance
                          </span>
                          <span className="text-blue-600">
                            {Math.round((content.likes + content.comments + content.shares) / content.views * 10000) / 100}
                            % engagement
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div className="bg-blue-600 h-2 rounded-full" style={{
                      width: `${Math.min(100, Math.round((content.likes + content.comments + content.shares) / content.views * 10000) / 100)}%`
                    }}></div>
                        </div>
                      </div>
                      <div className="mb-4">
                        <div className="flex justify-between text-sm mb-1">
                          <span className="font-medium text-gray-700">
                            Conversion Rate
                          </span>
                          <span className="text-green-600">
                            {Math.round(content.conversions / content.views * 10000) / 100}
                            %
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div className="bg-green-600 h-2 rounded-full" style={{
                      width: `${Math.min(100, Math.round(content.conversions / content.views * 1000))}%`
                    }}></div>
                        </div>
                      </div>
                      <button onClick={() => setSelectedContent(content)} className="w-full mt-2 bg-gray-100 text-gray-700 px-4 py-2 rounded-md text-sm font-medium hover:bg-gray-200 transition-colors">
                        Leave Feedback
                      </button>
                    </div>
                  </div>)}
              </div>
            </div>)}
          {/* Feedback Modal */}
          {selectedContent && <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
              <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full">
                <div className="px-6 py-4 border-b flex justify-between items-center">
                  <h3 className="text-lg font-medium text-gray-900">
                    Content Feedback
                  </h3>
                  <button onClick={() => setSelectedContent(null)} className="text-gray-400 hover:text-gray-500">
                    <XIcon className="w-5 h-5" />
                  </button>
                </div>
                <div className="p-6">
                  <div className="flex space-x-4 mb-6">
                    <img src={`${selectedContent.thumbnail}?auto=format&fit=crop&w=200&h=120`} alt="Content thumbnail" className="w-32 h-20 object-cover rounded" />
                    <div>
                      <h4 className="font-medium text-gray-900">
                        Content Performance
                      </h4>
                      <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
                        <div>
                          <span className="text-gray-500">Likes:</span>{' '}
                          {selectedContent.likes.toLocaleString()}
                        </div>
                        <div>
                          <span className="text-gray-500">Comments:</span>{' '}
                          {selectedContent.comments.toLocaleString()}
                        </div>
                        <div>
                          <span className="text-gray-500">Shares:</span>{' '}
                          {selectedContent.shares.toLocaleString()}
                        </div>
                        <div>
                          <span className="text-gray-500">Views:</span>{' '}
                          {selectedContent.views.toLocaleString()}
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="mb-4">
                    <label className="flex items-center space-x-2 mb-2">
                      <span className="text-gray-700 font-medium">
                        Was this content effective?
                      </span>
                    </label>
                    <div className="flex space-x-4">
                      <button className="flex items-center px-4 py-2 rounded-md border border-gray-300 hover:bg-gray-50">
                        <ThumbsUpIcon className="w-5 h-5 mr-2 text-green-600" />
                        <span>Yes, very effective</span>
                      </button>
                      <button className="flex items-center px-4 py-2 rounded-md border border-gray-300 hover:bg-gray-50">
                        <ThumbsDownIcon className="w-5 h-5 mr-2 text-red-600" />
                        <span>No, needs improvement</span>
                      </button>
                    </div>
                  </div>
                  <div>
                    <label htmlFor="feedback" className="block text-sm font-medium text-gray-700 mb-2">
                      Detailed Feedback
                    </label>
                    <textarea id="feedback" rows={4} className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="What worked well? What could be improved?" value={feedback} onChange={e => setFeedback(e.target.value)}></textarea>
                  </div>
                </div>
                <div className="px-6 py-4 bg-gray-50 border-t flex justify-end">
                  <button type="button" className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 mr-3" onClick={() => setSelectedContent(null)}>
                    Cancel
                  </button>
                  <button type="button" className="px-4 py-2 bg-blue-600 border border-transparent rounded-md text-sm font-medium text-white hover:bg-blue-700" onClick={() => handleFeedbackSubmit(selectedContent.id)}>
                    Submit Feedback
                  </button>
                </div>
              </div>
            </div>}
        </div>
      </div>
    </div>;
};
export default Performance;