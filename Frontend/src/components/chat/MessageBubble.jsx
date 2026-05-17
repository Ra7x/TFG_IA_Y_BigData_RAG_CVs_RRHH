import CandidateCard from '../results/CandidateResults';


const MessageBubble = ({ message }) => {
  const isUser = message.sender === 'user';
  const hasResults = message.results && message.results.length > 0;

  return (
    <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} mb-4 animate-fadeIn`}>
      <div
        className={`max-w-[80%] px-4 py-2 rounded-2xl shadow-sm ${
          isUser 
            ? 'bg-blue-600 text-white rounded-tr-none' 
            : 'bg-white border border-gray-200 text-gray-800 rounded-tl-none'
        }`}
      >
        <p className="text-sm whitespace-pre-wrap">{message.text}</p>
      </div>

      {/* Si hay resultados (matches), los pintamos debajo de la burbuja */}
      {!isUser && hasResults && (
        <div className="w-full max-w-[90%] mt-3">
          <p className="text-[10px] font-bold text-gray-400 uppercase mb-2 ml-1">Perfiles recomendados:</p>
          {message.results.map((cand, idx) => (
            <CandidateCard key={idx} candidate={cand} />
          ))}
        </div>
      )}
    </div>
  );
};

export default MessageBubble;