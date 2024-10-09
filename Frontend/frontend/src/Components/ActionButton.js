// components/ActionButton.js
import React from 'react';

const ActionButton = ({ label, icon, bgColor }) => {
  return (
    <div className={`h-56 flex flex-col items-center justify-center p-5 ${bgColor} text-white border border-[#603a2a] rounded-md hover:opacity-90 cursor-pointer`}>
      <i className={`icon-${icon} text-2xl`}></i>
      <p className="mt-2">{label}</p>
    </div>
  );
};

export default ActionButton;