const express = require('express');
const router = express.Router();
const Libro = require('../models/libro_model');
const Autor = require('../models/autor_model');
const Genero = require('../models/genero_model');
const { authenticateToken, isAdmin } = require('../middlewares/auth_middleware');

// Obtener todos los libros
router.get('/libros', async (req, res, next) => {
    try {
        const libros = await Libro.find({ is_active: true })
            .populate('genero', 'genero_nombre')
            .populate('autores', 'autor_nombre')
            .sort({ libro_titulo: 1 });
        
        return res.status(200).json(libros);
    } catch (error) {
        next(error);
    }
});

// Obtener un libro por ID
router.get('/libro/:id', async (req, res, next) => {
    try {
        const libro = await Libro.findOne({ _id: req.params.id, is_active: true })
            .populate('genero', 'genero_nombre')
            .populate('autores', 'autor_nombre autor_pais anio_nacimiento');
        
        if (!libro) {
            return res.status(404).json({ error: "Libro no encontrado o ha sido eliminado" });
        }
        
        return res.status(200).json(libro);
    } catch (error) {
        next(error);
    }
});

// Crear un nuevo libro
router.post('/libro', authenticateToken, async (req, res, next) => {
    try {
        const { titulo, anio, genero_id, autores_ids } = req.body;
        
        // Validar datos requeridos
        if (!titulo || !titulo.trim()) {
            return res.status(400).json({ error: "El título del libro es obligatorio" });
        }
        
        if (!genero_id) {
            return res.status(400).json({ error: "El género es obligatorio" });
        }
        
        if (!autores_ids || !Array.isArray(autores_ids) || autores_ids.length === 0) {
            return res.status(400).json({ error: "Debe especificar al menos un autor" });
        }
        
        // Validar año de publicación
        if (anio && (anio < 0 || anio > 2100)) {
            return res.status(400).json({ error: "El año de publicación debe estar entre 0 y 2100" });
        }
        
        // Verificar si ya existe un libro con el mismo título
        const libroExistente = await Libro.findOne({
            libro_titulo: titulo,
            is_active: true
        });
        
        if (libroExistente) {
            return res.status(409).json({ error: "Ya existe un libro con ese título" });
        }
        
        // Verificar si el género existe
        const genero = await Genero.findById(genero_id);
        
        if (!genero) {
            return res.status(404).json({ error: `El género con ID ${genero_id} no existe` });
        }
        
        // Verificar si todos los autores existen y están activos
        for (const autorId of autores_ids) {
            const autor = await Autor.findOne({ _id: autorId, is_active: true });
            
            if (!autor) {
                return res.status(404).json({ error: `El autor con ID ${autorId} no existe o ha sido eliminado` });
            }
        }
        
        // Crear nuevo libro
        const nuevoLibro = new Libro({
            libro_titulo: titulo,
            anio_publicacion: anio,
            genero: genero_id,
            autores: autores_ids
        });
        
        await nuevoLibro.save();
        
        // Obtener libro con relaciones
        const libroCreado = await Libro.findById(nuevoLibro._id)
            .populate('genero')
            .populate('autores');
        
        return res.status(201).json(libroCreado);
    } catch (error) {
        next(error);
    }
});

// Actualizar un libro
router.put('/libro/:id', authenticateToken, async (req, res, next) => {
    try {
        const { id } = req.params;
        const { titulo, anio, genero_id, autores_ids } = req.body;
        
        // Verificar si el libro existe y está activo
        const libro = await Libro.findOne({ _id: id, is_active: true });
        
        if (!libro) {
            return res.status(404).json({ error: "Libro no encontrado o ha sido eliminado" });
        }
        
        // Validar datos requeridos
        if (!titulo || !titulo.trim()) {
            return res.status(400).json({ error: "El título del libro es obligatorio" });
        }
        
        if (!genero_id) {
            return res.status(400).json({ error: "El género es obligatorio" });
        }
        
        if (!autores_ids || !Array.isArray(autores_ids) || autores_ids.length === 0) {
            return res.status(400).json({ error: "Debe especificar al menos un autor" });
        }
        
        // Validar año de publicación
        if (anio && (anio < 0 || anio > 2100)) {
            return res.status(400).json({ error: "El año de publicación debe estar entre 0 y 2100" });
        }
        
        // Verificar si ya existe otro libro con el mismo título
        const libroExistente = await Libro.findOne({
            libro_titulo: titulo,
            _id: { $ne: id },
            is_active: true
        });
        
        if (libroExistente) {
            return res.status(409).json({ error: "Ya existe otro libro con ese título" });
        }
        
        // Verificar si el género existe
        const genero = await Genero.findById(genero_id);
        
        if (!genero) {
            return res.status(404).json({ error: `El género con ID ${genero_id} no existe` });
        }
        
        // Verificar si todos los autores existen y están activos
        for (const autorId of autores_ids) {
            const autor = await Autor.findOne({ _id: autorId, is_active: true });
            
            if (!autor) {
                return res.status(404).json({ error: `El autor con ID ${autorId} no existe o ha sido eliminado` });
            }
        }
        
        // Actualizar libro
        libro.libro_titulo = titulo;
        libro.anio_publicacion = anio;
        libro.genero = genero_id;
        libro.autores = autores_ids;
        
        await libro.save();
        
        // Obtener libro actualizado con relaciones
        const libroActualizado = await Libro.findById(id)
            .populate('genero')
            .populate('autores');
        
        return res.status(200).json(libroActualizado);
    } catch (error) {
        next(error);
    }
});

// Eliminar un libro (borrado lógico)
router.delete('/libro/:id', authenticateToken, isAdmin, async (req, res, next) => {
    try {
        const { id } = req.params;
        
        // Verificar si el libro existe y está activo
        const libro = await Libro.findOne({ _id: id, is_active: true });
        
        if (!libro) {
            return res.status(404).json({ error: "Libro no encontrado o ya ha sido eliminado" });
        }
        
        // Borrado lógico
        libro.is_active = false;
        await libro.save();
        
        return res.status(200).json({ mensaje: "Libro marcado como eliminado" });
    } catch (error) {
        next(error);
    }
});

// Obtener autores de un libro
router.get('/libro/:id/autores', async (req, res, next) => {
    try {
        const { id } = req.params;
        
        // Verificar si el libro existe y está activo
        const libro = await Libro.findOne({ _id: id, is_active: true });
        
        if (!libro) {
            return res.status(404).json({ error: "Libro no encontrado o ha sido eliminado" });
        }
        
        // Obtener información completa del libro
        const libroConAutores = await Libro.findById(id)
            .populate({
                path: 'autores',
                match: { is_active: true }
            });
        
        return res.status(200).json({
            libro: {
                libro_id: libroConAutores._id,
                libro_titulo: libroConAutores.libro_titulo,
                anio_publicacion: libroConAutores.anio_publicacion
            },
            autores: libroConAutores.autores
        });
    } catch (error) {
        next(error);
    }
});

module.exports = router;