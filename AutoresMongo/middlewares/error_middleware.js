const errorHandler = (err, req, res, next) => {
    console.error(err.stack);
    
    // Si es un error de validación de Mongoose
    if (err.name === 'ValidationError') {
        const errors = Object.values(err.errors).map(el => el.message);
        return res.status(400).json({ 
            error: 'Error de validación', 
            details: errors.join(', ') 
        });
    }
    
    // Si es un error de duplicado (unique constraint)
    if (err.code === 11000) {
        const field = Object.keys(err.keyValue)[0];
        return res.status(409).json({ 
            error: `El valor del campo ${field} ya existe`
        });
    }
    
    // Error genérico
    return res.status(500).json({
        error: 'Error interno del servidor',
        details: err.message
    });
};

module.exports = errorHandler;