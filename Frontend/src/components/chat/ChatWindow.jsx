import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import CandidateResults from '../results/CandidateResults';

const ChatWindow = () => {
    const [messages, setMessages] = useState([
        { text: '¡Hola! Soy tu asistente de selección. ¿Qué perfil estás buscando hoy?', sender: 'bot' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = { text: input, sender: 'user' };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            // Llamada a tu API de FastAPI
            const response = await axios.post('http://localhost:8000/api/v1/search', {
              prompt: input,
              n_results: 3
            });

            const botMessage = {
                text: response.data.answer, // El texto natural generado por DeepSeek
                sender: 'bot',
                results: response.data.matches // La lista de candidatos para las tarjetas
            };

            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error("Error en la búsqueda:", error);
            setMessages(prev => [...prev, { 
                text: 'Lo siento, ha ocurrido un error al conectar con el servidor.', 
                sender: 'bot' 
            }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen max-w-4xl mx-auto bg-gray-50 shadow-lg">
            {/* Header */}
            <div className="bg-blue-600 p-4 text-white font-bold flex items-center shadow-md">
                <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center text-blue-600 mr-3">AI</div>
                <div>
                    <h1 className="text-lg">Talent Scout AI</h1>
                    <p className="text-xs font-normal opacity-80">Sistema de Matchmaking</p>
                </div>
            </div>

            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((msg, index) => (
                    <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] rounded-2xl p-4 ${
                            msg.sender === 'user' 
                            ? 'bg-blue-600 text-white rounded-tr-none' 
                            : 'bg-white text-gray-800 shadow-sm border rounded-tl-none'
                        }`}>
                            <p className="text-sm leading-relaxed">{msg.text}</p>
                            
                            {/* Renderizar tarjetas de candidatos si existen en este mensaje */}
                            {msg.results && msg.results.length > 0 && (
                                <div className="mt-4 border-t pt-4">
                                    <p className="text-xs font-bold text-gray-400 mb-3 tracking-widest uppercase">Perfiles Recomendados:</p>
                                    {msg.results.map((candidate) => (
                                        <CandidateResults key={candidate.id} candidate={candidate} />
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-white p-4 rounded-2xl shadow-sm border animate-pulse">
                            <div className="flex space-x-2">
                                <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce"></div>
                                <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce delay-75"></div>
                                <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce delay-150"></div>
                            </div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-white border-t flex items-center space-x-3">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    placeholder="Busca perfiles (ej: Experto en Java o dame los 3 mejores)..."
                    className="flex-1 border rounded-full px-5 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50"
                />
                <button 
                    onClick={handleSend}
                    className="bg-blue-600 text-white p-3 rounded-full hover:bg-blue-700 transition-colors shadow-md"
                >
                    <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                    </svg>
                </button>
            </div>
            <div className="text-[10px] text-center pb-2 text-gray-400">
                TFG - Algoritmos de IA aplicados a RRHH
            </div>
        </div>
    );
};

export default ChatWindow;
