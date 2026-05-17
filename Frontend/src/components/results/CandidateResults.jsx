const CandidateResults = ({ candidate }) => {
    const { data, score, id } = candidate;

    // 1. Limpieza y validación de campos (UX)
    const isValid = (field) => {
        if (!field) return false;
        if (typeof field === 'string') {
            const forbidden = ['not specified', 'n/a', 'undefined', 'null', 'unknown', 'none'];
            return field.trim() !== '' && !forbidden.includes(field.toLowerCase());
        }
        if (Array.isArray(field)) return field.length > 0;
        return true;
    };

    // 2. Lógica para el resumen inteligente
    const getCleanSummary = () => {
        const rawSummary = data.matchmaking_summary || data.summary;
        if (!isValid(rawSummary) || rawSummary.toLowerCase().includes("not generated")) {
            return `Especialista con enfoque en ${data.tech_stack?.slice(0, 3).join(', ') || 'tecnologías del sector'}. Perfil evaluado con un ${score}% de afinidad.`;
        }
        return rawSummary;
    };

    // 3. Extraer información relevante de historia y educación
    const lastJob = data.work_history?.[0];
    const topEducation = data.education?.[0];

    return (
        <div className="bg-white border border-gray-100 rounded-xl p-5 mb-4 shadow-sm hover:shadow-md hover:border-blue-300 transition-all cursor-pointer group">
            
            {/* ENCABEZADO */}
            <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                    <h3 className="font-bold text-gray-900 text-base group-hover:text-blue-600 transition-colors uppercase tracking-tight">
                        {data.full_name}
                    </h3>
                    <div className="flex flex-wrap gap-x-3 gap-y-1 mt-1 text-[11px] text-gray-500">
                        {isValid(data.location) && (
                            <span className="flex items-center">📍 {data.location}</span>
                        )}
                        {isValid(data.english_level) && (
                            <span className="flex items-center">🌐 {data.english_level}</span>
                        )}
                    </div>
                </div>
                <div className="text-right ml-4">
                    <div className={`text-[10px] font-bold px-2 py-1 rounded-md border ${
                        score >= 70 ? 'text-green-600 bg-green-50 border-green-100' : 'text-blue-600 bg-blue-50 border-blue-100'
                    }`}>
                        {score}% Match
                    </div>
                    <div className="text-[9px] text-gray-400 mt-1">ID: {id}</div>
                </div>
            </div>

            {/* RESUMEN DE LA IA */}
            <div className="mb-4">
                <p className="text-xs text-gray-600 leading-relaxed italic bg-gray-50/50 p-3 rounded-lg border-l-2 border-blue-400">
                    "{getCleanSummary()}"
                </p>
            </div>

            {/* SECCIÓN DE DETALLES (Habilitada por disponibilidad de datos) */}
            {(lastJob || topEducation) && (
                <div className="grid grid-cols-2 gap-4 mb-4 border-t border-gray-50 pt-3">
                    {lastJob && isValid(lastJob.job_title) && (
                        <div>
                            <p className="text-[10px] font-bold text-gray-400 uppercase mb-1">Último Rol</p>
                            <p className="text-[11px] text-gray-700 font-medium truncate">{lastJob.job_title}</p>
                            <p className="text-[10px] text-gray-400 truncate">{lastJob.company}</p>
                        </div>
                    )}
                    {topEducation && isValid(topEducation.degree) && (
                        <div>
                            <p className="text-[10px] font-bold text-gray-400 uppercase mb-1">Formación</p>
                            <p className="text-[11px] text-gray-700 font-medium truncate">{topEducation.degree}</p>
                            <p className="text-[10px] text-gray-400 truncate">{topEducation.institution}</p>
                        </div>
                    )}
                </div>
            )}

            {/* TECH STACK / SKILLS */}
            {isValid(data.tech_stack) && (
                <div className="mt-2">
                    <div className="flex flex-wrap gap-1">
                        {data.tech_stack.slice(0, 10).map((tech, idx) => (
                            <span 
                                key={idx} 
                                className="text-[9px] bg-blue-50 text-blue-600 px-2 py-0.5 rounded-full border border-blue-100 font-medium"
                            >
                                {tech}
                            </span>
                        ))}
                        {data.tech_stack.length > 10 && (
                            <span className="text-[9px] text-gray-400 self-center ml-1">
                                +{data.tech_stack.length - 10} más
                            </span>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default CandidateResults;