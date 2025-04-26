const express = require('express');
const router = express.Router();
const Genero = require('../models/genero_model');
const Libro = require('../models/libro_model');
const { authenticateToken, isAdmin } = require('../middlewares/auth_middleware');

// Obtener todos los géneros
router.get('/generos', async (req, res, next) => {
    try {
        const generos = await Genero.find().sort({ genero_nombre: 1 });
        return res.status(200).json(generos);
    } catch (error) {
        next(error);
    }
});

// Obtener un género por ID
router.get('/genero/:id', async (req, res, next) => {
    try {
        const genero = await Genero.findById(req.params.id);
        
        if (!genero) {
            return res.status(404).json({ error: "Género no encontrado" });
        }
        
        return res.status(200).json(genero);
    } catch (error) {
        next(error);
    }
});

// Crear un nuevo género
router.post('/genero', authenticateToken, isAdmin, async (req, res, next) => {
    try {
        const { nombre, descripcion } = req.body;
        
        // Validar datos requeridos
        if (!nombre || !nombre.trim()) {
            return res.status(400).json({ error: "El nombre del género es obligatorio" });
        }
        
        // Verificar si ya existe un género con el mismo nombre
        const generoExistente = await Genero.findOne({
            genero_nombre: nombre
        });
        
        if (generoExistente) {
            return res.status(409).json({ error: "Ya existe un género con ese nombre" });
        }
        
        // Crear nuevo género
        const nuevoGenero = new Genero({
            genero_nombre: nombre,
            descripcion
        });
        
        await nuevoGenero.save();
        
        return res.status(201).json(nuevoGenero);
    } catch (error) {
        next(error);
    }
});

// Actualizar un género
router.put('/genero/:id', authenticateToken, isAdmin, async (req, res, next) => {
    try {
        const { id } = req.params;
        const { nombre, descripcion } = req.body;
        
        // Verificar si el género existe
        const genero = await Genero.findById(id);
        
        if (!genero) {
            return res.status(404).json({ error: "Género no encontrado" });
        }
        
        // Validar datos requeridos
        if (!nombre || !nombre.trim()) {
            return res.status(400).json({ error: "El nombre del género es obligatorio" });
        }
        
        // Verificar si ya existe otro género con el mismo nombre
        const generoExistente = await Genero.findOne({
            genero_nombre: nombre,
            _id: { $ne: id }
        });
        
        if (generoExistente) {
            return res.status(409).json({ error: "Ya existe otro género con ese nombre" });
        }
        
        // Actualizar género
        genero.genero_nombre = nombre;
        genero.descripcion = descripcion;
        
        await genero.save();
        
        return res.status(200).json(genero);
    } catch (error) {
        next(error);
    }
});

// Eliminar un género
router.delete('/genero/:id', authenticateToken, isAdmin, async (req, res, next) => {
    try {
        const { id } = req.params;
        
        // Verificar si el género existe
        const genero = await Genero.findById(id);
        
        if (!genero) {
            return res.status(404).json({ error: "Género no encontrado" });
        }
        
        // Verificar si tiene libros asociados
        const librosCount = await Libro.countDocuments({ genero: id });
        
        if (librosCount > 0) {
            return res.status(400).json({ error: "No se puede eliminar el género porque tiene libros asociados" });
        }
        
        // Eliminar género
        await Genero.findByIdAndDelete(id);
        
        return res.status(200).json({ mensaje: "Género eliminado correctamente" });
    } catch (error) {
        next(error);
    }
});

module.exports = router;