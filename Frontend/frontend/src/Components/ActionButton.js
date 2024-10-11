// components/ActionButton.js
import React from 'react';

const ActionButton = ({ label, icon, onClick }) => (
    <div onClick={onClick} className="h-48 w-2/4 flex flex-col items-center justify-center p-4 bg-[#fadbca] text-[#563635] border border-[#563635] border-2 rounded-md hover:opacity-90 cursor-pointer">
        <img src={icon} alt={label} className="h-8 w-8 mb-auto ml-auto"/>
        <div className="w-full text-left">
            <p className="font-medium whitespace-pre-line">
                {label}
            </p>
        </div>
    </div>
);

export default ActionButton;