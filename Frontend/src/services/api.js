import axios from 'axios';

// Usamos 127.0.0.1 para evitar problemas de red local si estás en la misma máquina
const api = axios.create({
    baseURL: 'http://100.90.201.104:8000/api/v1', 
});

export const searchCandidatos = async (prompt) => {
    try {
        const response = await api.post('/search', { prompt });
        return response.data.matches; 
    } catch (error) {
        console.error("Error en la llamada a la API:", error);
        throw error; 
    }
};