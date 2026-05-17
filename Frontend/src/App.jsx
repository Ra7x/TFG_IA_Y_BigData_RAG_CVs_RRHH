import './App.css'
import ChatWindow from './components/Chat/ChatWindow'

function App() {
  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4 font-sans">
      <div className="w-full max-w-4xl">
        <h1 className="text-white text-3xl font-bold mb-8 text-center">
          TFG: Sistema de Matchmaking Inteligente
        </h1>
        <ChatWindow />
      </div>
    </div>
  )
}

export default App