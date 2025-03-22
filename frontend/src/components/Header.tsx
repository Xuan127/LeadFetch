import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { BarChartIcon, FileTextIcon, UsersIcon } from 'lucide-react';
const Header = () => {
  const location = useLocation();
  const navItems = [{
    name: 'Client Brief',
    path: '/',
    icon: <FileTextIcon className="w-5 h-5" />
  }, {
    name: 'Influencers',
    path: '/influencers',
    icon: <UsersIcon className="w-5 h-5" />
  }, {
    name: 'Performance',
    path: '/performance',
    icon: <BarChartIcon className="w-5 h-5" />
  }];
  return <header className="bg-white shadow">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-blue-600">InfluencerHub</h1>
          </div>
          <nav className="flex space-x-4">
            {navItems.map(item => <Link key={item.path} to={item.path} className={`flex items-center px-3 py-2 rounded-md text-sm font-medium ${location.pathname === item.path ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'}`}>
                <span className="mr-2">{item.icon}</span>
                {item.name}
              </Link>)}
          </nav>
        </div>
      </div>
    </header>;
};
export default Header;