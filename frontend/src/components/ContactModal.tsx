import React, { useState } from 'react';
import { XIcon } from 'lucide-react';
const ContactModal = ({
  influencer,
  onClose
}) => {
  const [message, setMessage] = useState(`Hi ${influencer.name},\n\nI'm reaching out because I think you'd be a great fit for our upcoming campaign. We're looking for influencers in the ${influencer.niche} space, and your content really resonates with our brand vision.\n\nWould you be interested in discussing a potential collaboration?\n\nLooking forward to your response,\n[Your Name]`);
  const handleSend = () => {
    // In a real app, this would send the message
    setTimeout(() => {
      onClose();
      // Show success notification
    }, 1000);
  };
  return <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] flex flex-col">
        <div className="px-6 py-4 border-b flex justify-between items-center">
          <h3 className="text-lg font-medium text-gray-900">
            Contact {influencer.name}
          </h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-500">
            <XIcon className="w-5 h-5" />
          </button>
        </div>
        <div className="p-6 flex-1 overflow-auto">
          <div className="mb-6">
            <div className="flex items-center mb-4">
              <img src={`${influencer.profileImage}?auto=format&fit=crop&w=60&h=60`} alt={influencer.name} className="w-12 h-12 rounded-full mr-4" />
              <div>
                <h4 className="font-medium text-gray-900">{influencer.name}</h4>
                <p className="text-sm text-gray-500">{influencer.username}</p>
              </div>
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <h5 className="text-sm font-medium text-gray-700 mb-2">
                Influencer Details
              </h5>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div>
                  <span className="text-gray-500">Followers:</span>{' '}
                  <span className="font-medium">{influencer.followers}</span>
                </div>
                <div>
                  <span className="text-gray-500">Engagement:</span>{' '}
                  <span className="font-medium">
                    {influencer.engagementRate}
                  </span>
                </div>
                <div>
                  <span className="text-gray-500">Niche:</span>{' '}
                  <span className="font-medium">{influencer.niche}</span>
                </div>
                <div>
                  <span className="text-gray-500">Location:</span>{' '}
                  <span className="font-medium">{influencer.location}</span>
                </div>
              </div>
            </div>
          </div>
          <div>
            <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
              Message
            </label>
            <textarea id="message" rows={10} className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" value={message} onChange={e => setMessage(e.target.value)}></textarea>
            <p className="mt-1 text-sm text-gray-500">
              This message will be sent to the influencer's registered contact
              method.
            </p>
          </div>
        </div>
        <div className="px-6 py-4 bg-gray-50 border-t flex justify-end">
          <button type="button" className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 mr-3" onClick={onClose}>
            Cancel
          </button>
          <button type="button" className="px-4 py-2 bg-blue-600 border border-transparent rounded-md text-sm font-medium text-white hover:bg-blue-700" onClick={handleSend}>
            Send Message
          </button>
        </div>
      </div>
    </div>;
};
export default ContactModal;