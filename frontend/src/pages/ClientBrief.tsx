import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadCloudIcon } from 'lucide-react';
import { briefsApi, ClientBrief as ClientBriefType } from '../services/api';

// Define a simplified brief type for the upload functionality
interface UploadBrief {
  id: number;
  name: string;
  type: string;
  clientName?: string;
  productService?: string;
  targetAudience?: string;
  campaignGoal?: string;
  influencerType?: string;
  date: string;
}

interface ClientBriefProps {
  setCurrentBrief: (brief: ClientBriefType | UploadBrief | null) => void;
}

const ClientBrief: React.FC<ClientBriefProps> = ({
  setCurrentBrief
}) => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('upload');
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [formData, setFormData] = useState({
    clientName: '',
    productService: '',
    targetAudience: '',
    campaignGoal: '',
    influencerType: ''
  });
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    setUploading(true);
    // Simulate file upload with progress
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      setUploadProgress(progress);
      if (progress >= 100) {
        clearInterval(interval);
        setUploading(false);
        // Mock brief creation and navigation
        const mockBrief = {
          id: Date.now(),
          name: 'Uploaded Brief',
          type: 'upload',
          date: new Date().toLocaleDateString()
        };
        setCurrentBrief(mockBrief);
        navigate('/influencers');
      }
    }, 300);
  };
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const {
      name,
      value
    } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  const handleGenerateBrief = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    try {
      // Create the brief data
      const briefData = {
        id: Date.now(),
        name: formData.clientName,
        type: 'generated',
        clientName: formData.clientName,
        productService: formData.productService,
        targetAudience: formData.targetAudience,
        campaignGoal: formData.campaignGoal,
        influencerType: formData.influencerType,
        date: new Date().toLocaleDateString()
      };
      
      // Send to API
      const createdBrief = await briefsApi.create(briefData);
      
      // Update state and navigate
      setCurrentBrief(createdBrief);
      navigate('/influencers');
    } catch (error) {
      console.error('Error creating brief:', error);
      alert('Failed to create brief. Please try again.');
    }
  };
  return <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">
        Upload or Create Client Brief
      </h1>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="flex border-b">
          <button className={`px-6 py-4 text-sm font-medium ${activeTab === 'upload' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`} onClick={() => setActiveTab('upload')}>
            Upload Brief
          </button>
          <button className={`px-6 py-4 text-sm font-medium ${activeTab === 'generate' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`} onClick={() => setActiveTab('generate')}>
            Generate New Persona
          </button>
        </div>
        <div className="p-6">
          {activeTab === 'upload' ? <div>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-500 transition-colors cursor-pointer" onClick={() => {
                const fileInput = document.getElementById('fileUpload');
                if (fileInput) fileInput.click();
              }}>
                <UploadCloudIcon className="w-12 h-12 mx-auto text-gray-400 mb-4" />
                <h3 className="text-lg font-medium text-gray-700 mb-1">
                  Upload Client Brief
                </h3>
                <p className="text-sm text-gray-500 mb-4">
                  Drag and drop your file here or click to browse
                </p>
                <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
                  Select File
                </button>
                <input id="fileUpload" type="file" title="Upload Brief File" placeholder="Upload Brief File" className="hidden" onChange={handleFileUpload} />
              </div>
              {uploading && <div className="mt-6">
                  <div className="flex justify-between text-sm text-gray-600 mb-1">
                    <span>Uploading...</span>
                    <span>{uploadProgress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-blue-600 h-2 rounded-full transition-all duration-300" style={{
                width: `${uploadProgress}%`
              }}></div>
                  </div>
                </div>}
            </div> : <form onSubmit={handleGenerateBrief}>
              <div className="space-y-6">
                <div>
                  <label htmlFor="clientName" className="block text-sm font-medium text-gray-700 mb-1">
                    Client Name
                  </label>
                  <input type="text" id="clientName" name="clientName" value={formData.clientName} onChange={handleInputChange} className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required />
                </div>
                <div>
                  <label htmlFor="productService" className="block text-sm font-medium text-gray-700 mb-1">
                    Product/Service
                  </label>
                  <select id="productService" name="productService" value={formData.productService} onChange={handleInputChange} className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                    <option value="">Select a product/service</option>
                    <option value="Fashion">Fashion</option>
                    <option value="Beauty">Beauty</option>
                    <option value="Tech">Tech</option>
                    <option value="Food">Food & Beverage</option>
                    <option value="Fitness">Fitness</option>
                    <option value="Travel">Travel</option>
                    <option value="Lifestyle">Lifestyle</option>
                  </select>
                </div>
                <div>
                  <label htmlFor="targetAudience" className="block text-sm font-medium text-gray-700 mb-1">
                    Target Audience
                  </label>
                  <select id="targetAudience" name="targetAudience" value={formData.targetAudience} onChange={handleInputChange} className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                    <option value="">Select target audience</option>
                    <option value="Gen Z">Gen Z (18-24)</option>
                    <option value="Millennials">Millennials (25-40)</option>
                    <option value="Gen X">Gen X (41-56)</option>
                    <option value="Boomers">Baby Boomers (57-75)</option>
                    <option value="Parents">Parents</option>
                    <option value="Professionals">Young Professionals</option>
                  </select>
                </div>
                <div>
                  <label htmlFor="campaignGoal" className="block text-sm font-medium text-gray-700 mb-1">
                    Campaign Goal
                  </label>
                  <textarea id="campaignGoal" name="campaignGoal" value={formData.campaignGoal} onChange={handleInputChange} rows={3} className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Describe your campaign goals..." required></textarea>
                </div>
                <div>
                  <label htmlFor="influencerType" className="block text-sm font-medium text-gray-700 mb-1">
                    Preferred Influencer Type
                  </label>
                  <textarea id="influencerType" name="influencerType" value={formData.influencerType} onChange={handleInputChange} rows={3} className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Describe your preferred influencer types..." required></textarea>
                </div>
                <div>
                  <button type="submit" className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
                    Generate Brief
                  </button>
                </div>
              </div>
            </form>}
        </div>
      </div>
    </div>;
};
export default ClientBrief;
