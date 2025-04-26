const express = require('express');
const router = express.Router();
const Autor = require('../models/autor_model');
const Libro = require('../models/libro_model');
const { authenticateToken, isAdmin } = require('../middlewares/auth_middleware');

// Obtener todos los autores
router.get('/autores', async (req, res, next) => {
    try {
        const autores = await Autor.find({ is_active: true }).sort({ autor_nombre: 1 });
        return res.status(200).json(autores);
    } catch (error) {
        next(error);
    }
});

// Obtener un autor por ID
router.get('/autor/:id', async (req, res, next) => {
    try {
        const autor = await Autor.findOne({ _id: req.params.id, is_active: true });
        
        if (!autor) {
            return res.status(404).json({ error: "Autor no encontrado o ha sido eliminado" });
        }
        
        return res.status(200).json(autor);
    } catch (error) {
        next(error);
    }
});

// Crear un nuevo autor
router.post('/autor', authenticateToken, async (req, res, next) => {
    try {
        const { nombre, pais, anio } = req.body;
        
        // Validar datos requeridos
        if (!nombre || !nombre.trim()) {
            return res.status(400).json({ error: "El nombre del autor es obligatorio" });
        }
        
        // Validar año de nacimiento
        if (anio && (anio < 0 || anio > 2100)) {
            return res.status(400).json({ error: "El año de nacimiento debe estar entre 0 y 2100" });
        }
        
        // Verificar si ya existe un autor con el mismo nombre
        const autorExistente = await Autor.findOne({
            autor_nombre: nombre,
            is_active: true
        });
        
        if (autorExistente) {
            return res.status(409).json({ error: "Ya existe un autor con ese nombre" });
        }
        
        // Crear nuevo autor
        const nuevoAutor = new Autor({
            autor_nombre: nombre,
            autor_pais: pais,
            anio_nacimiento: anio
        });
        
        await nuevoAutor.save();
        
        return res.status(201).json(nuevoAutor);
    } catch (error) {
        next(error);
    }
});

// Actualizar un autor
router.put('/autor/:id', authenticateToken, async (req, res, next) => {
    try {
        const { id } = req.params;
        const { nombre, pais, anio } = req.body;
        
        // Verificar si el autor existe y está activo
        const autor = await Autor.findOne({ _id: id, is_active: true });
        
        if (!autor) {
            return res.status(404).json({ error: "Autor no encontrado o ha sido eliminado" });
        }
        
        // Validar datos requeridos
        if (!nombre || !nombre.trim()) {
            return res.status(400).json({ error: "El nombre del autor es obligatorio" });
        }
        
        // Validar año de nacimiento
        if (anio && (anio < 0 || anio > 2100)) {
            return res.status(400).json({ error: "El año de nacimiento debe estar entre 0 y 2100" });
        }
        
        // Verificar si ya existe otro autor con el mismo nombre
        const autorExistente = await Autor.findOne({
            autor_nombre: nombre,
            _id: { $ne: id },
            is_active: true
        });
        
        if (autorExistente) {
            return res.status(409).json({ error: "Ya existe otro autor con ese nombre" });
        }
        
        // Actualizar autor
        autor.autor_nombre = nombre;
        autor.autor_pais = pais;
        autor.anio_nacimiento = anio;
        
        await autor.save();
        
        return res.status(200).json(autor);
    } catch (error) {
        next(error);
    }
});

// Eliminar un autor (borrado lógico)
router.delete('/autor/:id', authenticateToken, isAdmin, async (req, res, next) => {
    try {
        const { id } = req.params;
        
        // Verificar si el autor existe y está activo
        const autor = await Autor.findOne({ _id: id, is_active: true });
        
        if (!autor) {
            return res.status(404).json({ error: "Autor no encontrado o ya ha sido eliminado" });
        }
        
        // Verificar si tiene libros asociados
        const librosCount = await Libro.countDocuments({
            autores: id,
            is_active: true
        });
        
        if (librosCount > 0) {
            // Borrado lógico
            autor.is_active = false;
            await autor.save();
            
            return res.status(200).json({ mensaje: "Autor marcado como eliminado" });
        } else {
            // Borrado físico si no tiene libros
            await Autor.findByIdAndDelete(id);
            
            return res.status(200).json({ mensaje: "Autor eliminado completamente" });
        }
    } catch (error) {
        next(error);
    }
});

// Obtener libros de un autor
router.get('/autor/:id/libros', async (req, res, next) => {
    try {
        const { id } = req.params;
        
        // Verificar si el autor existe y está activo
        const autor = await Autor.findOne({ _id: id, is_active: true });
        
        if (!autor) {
            return res.status(404).json({ error: "Autor no encontrado o ha sido eliminado" });
        }
        
        // Obtener los libros del autor
        const libros = await Libro.find({
            autores: id,
            is_active: true
        }).populate('genero', 'genero_nombre')
          .sort({ anio_publicacion: -1 });
        
        return res.status(200).json({
            autor,
            libros
        });
    } catch (error) {
        next(error);
    }
});

module.exports = router;