import React from 'react';
import ActionButton from './ActionButton';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import itineraryIcon from '../Images/itinerary.png'
import flightIcon from '../Images/plane.png'
import lodgingIcon from '../Images/hotel.png'

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
              <div className="grid grid-cols-3 ml-32 mb-1 mt-24">
                <ActionButton label="Find Flights" icon={flightIcon} />
                <ActionButton label="Find Lodging" icon={lodgingIcon} />
                <ActionButton label="Itinerary Planning" icon={itineraryIcon} />
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