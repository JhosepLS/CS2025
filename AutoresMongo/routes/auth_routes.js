const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const User = require('../models/user_model');
const { authenticateToken } = require('../middlewares/auth_middleware');

// Registrar nuevo usuario
router.post('/auth/register', async (req, res, next) => {
    try {
        const { username, password, email, role } = req.body;
        
        // Validar datos requeridos
        if (!username || !password || !email) {
            return res.status(400).json({
                error: 'Datos incompletos. Se requiere username, password y email'
            });
        }
        
        // En registro público, no permitir crear admins
        let userRole = role;
        if (role === 'admin') {
            userRole = 'usuario';
        }
        
        // Crear nuevo usuario
        const newUser = new User({
            username,
            password, // Se encriptará automáticamente gracias al middleware
            email,
            role: userRole
        });
        
        await newUser.save();
        
        // Responder sin incluir la contraseña
        const userResponse = {
            user_id: newUser._id,
            username: newUser.username,
            email: newUser.email,
            role: newUser.role
        };
        
        return res.status(201).json(userResponse);
    } catch (error) {
        next(error);
    }
});

// Login
router.post('/auth/login', async (req, res, next) => {
    try {
        const { username, password } = req.body;
        
        // Validar datos requeridos
        if (!username || !password) {
            return res.status(400).json({
                error: 'Se requiere username y password'
            });
        }
        
        // Buscar usuario
        const user = await User.findOne({ username, is_active: true });
        
        // Si no se encuentra el usuario
        if (!user) {
            return res.status(404).json({
                error: 'Usuario no encontrado o inactivo'
            });
        }
        
        // Verificar contraseña
        const validPassword = await user.validatePassword(password);
        
        if (!validPassword) {
            return res.status(401).json({
                error: 'Contraseña incorrecta'
            });
        }
        
        // Generar token JWT
        const token = jwt.sign(
            {
                user_id: user._id,
                username: user.username,
                role: user.role
            },
            process.env.JWT_SECRET_KEY || 'clave_secreta_predeterminada',
            { expiresIn: '24h' }
        );
        
        // Responder con token y datos del usuario
        return res.status(200).json({
            token,
            user: {
                user_id: user._id,
                username: user.username,
                email: user.email,
                role: user.role
            }
        });
        
    } catch (error) {
        next(error);
    }
});

// Verificar token
router.get('/auth/verify', authenticateToken, (req, res) => {
    return res.status(200).json({
        message: 'Token válido',
        user: {
            user_id: req.user.user_id,
            username: req.user.username,
            role: req.user.role
        }
    });
});

module.exports = router;