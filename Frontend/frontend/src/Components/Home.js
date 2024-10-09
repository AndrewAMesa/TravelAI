import React from 'react';
import ActionButton from './ActionButton';
import Sidebar from './Sidebar'
import TopBar from './TopBar';

const Home = () => {
    return (
        <div className="h-screen flex flex-col">
          {/* Top Bar */}
          <TopBar />
    
          <div className="flex flex-1">
            {/* Sidebar Section */}
            <div className="w-1/4 bg-[#563635] text-white p-5">
              <Sidebar />
            </div>
    
            {/* Main Content Section */}
            <div className="w-3/4 flex flex-col p-5 bg-[#fad4c0]">
              {/* Action Buttons Section */}
              <div className="grid grid-cols-3 gap-14 mb-8 mt-48">
                <ActionButton label="Find Flights" icon="flight" />
                <ActionButton label="Find Lodging" icon="hotel" />
                <ActionButton label="Itinerary Planning" icon="planning" />
              </div>
    
              {/* Search Bar Section (placed at the bottom) */}
              <div className="mt-auto w-full">
                <input
                  type="text"
                  placeholder="Search for flights, lodging, or destinations..."
                  className="p-3 border border-gray-300 rounded-md w-full"
                />
              </div>
            </div>
          </div>
        </div>
      );
};

export default Home;