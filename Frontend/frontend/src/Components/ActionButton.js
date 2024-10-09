// components/ActionButton.js
import React from 'react';

const ActionButton = ({ label, icon, bgColor }) => {
  return (
    <div className={`h-48 w-48 flex flex-col items-center justify-center p-5 ${bgColor} text-[#563635] border border-[#563635] rounded-md hover:opacity-90 cursor-pointer`}>
      <img src={icon} alt={label} className="right-2 h-10 w-10 ml-32 mb-6"/>
      <p className="mb-20 font-bold">{label}</p>
    </div>
  );
};

export default ActionButton;