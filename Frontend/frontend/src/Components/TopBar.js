import React from 'react';

const TopBar = () => {
  return (
    <div className="w-full h-16 bg-[#563635] flex items-center justify-between px-4 text-white">
      <h1 className="text-xl font-bold">AI Travel Assistant</h1>
      <div className="flex items-center space-x-4">
        <button className="hover:bg-[#4e2c20] p-2 rounded">Profile</button>
      </div>
    </div>
  );
};

export default TopBar;