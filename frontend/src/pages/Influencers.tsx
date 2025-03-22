import React, { useState } from 'react';
import { SearchIcon, FilterIcon, InstagramIcon, YoutubeIcon, TwitterIcon } from 'lucide-react';
import ContactModal from '../components/ContactModal';
// Mock data for influencers
const mockInfluencers = [{
  id: 1,
  name: 'Sarah Johnson',
  username: '@sarahjbeauty',
  profileImage: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330',
  followers: '1.2M',
  engagementRate: '3.8%',
  niche: 'Beauty & Skincare',
  platform: 'instagram',
  location: 'Los Angeles, CA'
}, {
  id: 2,
  name: 'Alex Chen',
  username: '@alexchentech',
  profileImage: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d',
  followers: '850K',
  engagementRate: '4.2%',
  niche: 'Tech Reviews',
  platform: 'youtube',
  location: 'San Francisco, CA'
}, {
  id: 3,
  name: 'Maria Rodriguez',
  username: '@mariafit',
  profileImage: 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6',
  followers: '950K',
  engagementRate: '5.1%',
  niche: 'Fitness & Wellness',
  platform: 'instagram',
  location: 'Miami, FL'
}, {
  id: 4,
  name: 'James Wilson',
  username: '@jameswcooks',
  profileImage: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d',
  followers: '720K',
  engagementRate: '3.5%',
  niche: 'Cooking & Food',
  platform: 'youtube',
  location: 'Chicago, IL'
}, {
  id: 5,
  name: 'Priya Patel',
  username: '@priyatravel',
  profileImage: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb',
  followers: '520K',
  engagementRate: '4.7%',
  niche: 'Travel & Adventure',
  platform: 'instagram',
  location: 'New York, NY'
}, {
  id: 6,
  name: 'David Kim',
  username: '@davidgaming',
  profileImage: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e',
  followers: '1.5M',
  engagementRate: '6.2%',
  niche: 'Gaming',
  platform: 'twitter',
  location: 'Seattle, WA'
}];
const Influencers = ({
  currentBrief
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    platform: 'all',
    minFollowers: '',
    minEngagement: '',
    location: ''
  });
  const [showFilters, setShowFilters] = useState(false);
  const [selectedInfluencer, setSelectedInfluencer] = useState(null);
  const handleSearch = e => {
    setSearchTerm(e.target.value);
  };
  const handleFilterChange = e => {
    const {
      name,
      value
    } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };
  const filteredInfluencers = mockInfluencers.filter(influencer => {
    // Search filter
    if (searchTerm && !influencer.name.toLowerCase().includes(searchTerm.toLowerCase()) && !influencer.username.toLowerCase().includes(searchTerm.toLowerCase()) && !influencer.niche.toLowerCase().includes(searchTerm.toLowerCase())) {
      return false;
    }
    // Platform filter
    if (filters.platform !== 'all' && influencer.platform !== filters.platform) {
      return false;
    }
    // Followers filter
    if (filters.minFollowers) {
      const followerCount = parseFloat(influencer.followers) * (influencer.followers.includes('M') ? 1000000 : 1000);
      if (followerCount < parseFloat(filters.minFollowers) * 1000) {
        return false;
      }
    }
    // Engagement filter
    if (filters.minEngagement) {
      const engagementRate = parseFloat(influencer.engagementRate);
      if (engagementRate < parseFloat(filters.minEngagement)) {
        return false;
      }
    }
    // Location filter
    if (filters.location && !influencer.location.toLowerCase().includes(filters.location.toLowerCase())) {
      return false;
    }
    return true;
  });
  const getPlatformIcon = platform => {
    switch (platform) {
      case 'instagram':
        return <InstagramIcon className="w-5 h-5 text-pink-600" />;
      case 'youtube':
        return <YoutubeIcon className="w-5 h-5 text-red-600" />;
      case 'twitter':
        return <TwitterIcon className="w-5 h-5 text-blue-400" />;
      default:
        return null;
    }
  };
  return <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Influencers Found</h1>
        {currentBrief && <div className="bg-blue-50 text-blue-700 px-4 py-2 rounded-lg text-sm">
            Active Brief:{' '}
            <span className="font-medium">{currentBrief.name}</span>
          </div>}
      </div>
      <div className="bg-white rounded-lg shadow overflow-hidden mb-8">
        <div className="p-4 border-b flex flex-wrap items-center gap-4">
          <div className="flex-1 min-w-[240px]">
            <div className="relative">
              <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input type="text" placeholder="Search influencers by name, username or niche" className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" value={searchTerm} onChange={handleSearch} />
            </div>
          </div>
          <button className="flex items-center px-4 py-2 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors" onClick={() => setShowFilters(!showFilters)}>
            <FilterIcon className="w-4 h-4 mr-2" />
            Filters
          </button>
        </div>
        {showFilters && <div className="p-4 bg-gray-50 border-b">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Platform
                </label>
                <select name="platform" value={filters.platform} onChange={handleFilterChange} className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option value="all">All Platforms</option>
                  <option value="instagram">Instagram</option>
                  <option value="youtube">YouTube</option>
                  <option value="twitter">Twitter</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Min. Followers (K)
                </label>
                <input type="number" name="minFollowers" value={filters.minFollowers} onChange={handleFilterChange} placeholder="e.g. 100" className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Min. Engagement (%)
                </label>
                <input type="number" name="minEngagement" value={filters.minEngagement} onChange={handleFilterChange} placeholder="e.g. 3.5" className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Location
                </label>
                <input type="text" name="location" value={filters.location} onChange={handleFilterChange} placeholder="e.g. New York" className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
            </div>
          </div>}
        <div className="p-6">
          {filteredInfluencers.length > 0 ? <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredInfluencers.map(influencer => <div key={influencer.id} className="bg-white border rounded-lg overflow-hidden hover:shadow-md transition-shadow">
                  <div className="p-4 flex items-start space-x-4">
                    <div className="flex-shrink-0">
                      <img src={`${influencer.profileImage}?auto=format&fit=crop&w=80&h=80`} alt={influencer.name} className="w-20 h-20 rounded-full object-cover" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center">
                        <h3 className="text-lg font-semibold text-gray-800 truncate">
                          {influencer.name}
                        </h3>
                        <span className="ml-2">
                          {getPlatformIcon(influencer.platform)}
                        </span>
                      </div>
                      <p className="text-sm text-gray-500">
                        {influencer.username}
                      </p>
                      <p className="text-sm text-gray-600 mt-1">
                        {influencer.location}
                      </p>
                      <div className="mt-3 flex flex-wrap gap-2">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {influencer.followers} followers
                        </span>
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          {influencer.engagementRate} engagement
                        </span>
                      </div>
                      <div className="mt-2">
                        <span className="text-xs font-medium text-gray-500">
                          {influencer.niche}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="px-4 py-3 bg-gray-50 border-t">
                    <button onClick={() => setSelectedInfluencer(influencer)} className="w-full bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors">
                      Contact Influencer
                    </button>
                  </div>
                </div>)}
            </div> : <div className="text-center py-12">
              <p className="text-gray-500 text-lg">
                No influencers found matching your criteria.
              </p>
              <p className="text-gray-400 mt-2">
                Try adjusting your filters or search terms.
              </p>
            </div>}
        </div>
      </div>
      {selectedInfluencer && <ContactModal influencer={selectedInfluencer} onClose={() => setSelectedInfluencer(null)} />}
    </div>;
};
export default Influencers;