const jwt = require('jsonwebtoken');
const User = require('../models/user_model');

// Verifica token JWT
const authenticateToken = async (req, res, next) => {
    try {
        // Buscar token en headers
        const authHeader = req.headers['authorization'];
        const token = authHeader && authHeader.split(' ')[1];
        
        if (!token) {
            return res.status(401).json({ error: 'Token requerido' });
        }
        
        // Verificar token
        const decoded = jwt.verify(token, process.env.JWT_SECRET_KEY || 'clave_secreta_predeterminada');
        
        // Buscar usuario en la base de datos
        const user = await User.findById(decoded.user_id);
        
        if (!user || !user.is_active) {
            return res.status(401).json({ error: 'Usuario no encontrado o inactivo' });
        }
        
        // Guardar datos del usuario en request
        req.user = {
            user_id: user._id,
            username: user.username,
            role: user.role
        };
        
        next();
    } catch (error) {
        if (error.name === 'TokenExpiredError') {
            return res.status(401).json({ error: 'Token expirado' });
        }
        
        return res.status(401).json({ error: 'Token inválido' });
    }
};

// Verifica si el usuario es administrador
const isAdmin = (req, res, next) => {
    if (!req.user) {
        return res.status(401).json({ error: 'No autenticado' });
    }
    
    if (req.user.role !== 'admin') {
        return res.status(403).json({ error: 'Se requieren privilegios de administrador' });
    }
    
    next();
};

module.exports = {
    authenticateToken,
    isAdmin
};