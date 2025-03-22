import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import ClientBrief from './pages/ClientBrief';
import Influencers from './pages/Influencers';
import Performance from './pages/Performance';
export function App() {
  const [currentBrief, setCurrentBrief] = useState(null);
  return <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<ClientBrief setCurrentBrief={setCurrentBrief} />} />
            <Route path="/influencers" element={<Influencers currentBrief={currentBrief} />} />
            <Route path="/performance" element={<Performance />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>;
}