const ActionButton = ({ label, icon, bgColor, onClick, isSmall }) => {
  const [firstWord, secondWord] = label.split(" ");

  return (
    <div
      onClick={onClick}
      className={`transition-all duration-300 ease-in-out
        ${isSmall ? 'w-32 h-32' : 'w-48 h-48'}
        flex flex-col items-center justify-center mx-4
        ${bgColor} text-[#563635] border border-[#563635] rounded-md 
        hover:opacity-90 cursor-pointer`}
    >
      <img src={icon} alt={label} className="h-8 w-8 mb-2" />
      <div className="w-full text-center">
        <p className="font-medium whitespace-pre-line">
          {firstWord} <span className="font-bold">{secondWord}</span>
        </p>
      </div>
    </div>
  );
};

export default ActionButton;
