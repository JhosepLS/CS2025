const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const dotenv = require('dotenv');

// Modelos
const User = require('./models/user_model');
const Autor = require('./models/autor_model');
const Genero = require('./models/genero_model');
const Libro = require('./models/libro_model');

// Cargar variables de entorno
dotenv.config();

// URI de MongoDB
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/biblioteca_db';

// Función para insertar datos de ejemplo
async function insertarDatosEjemplo() {
    try {
        // Verificar si ya hay géneros
        const generosCount = await Genero.countDocuments();
        
        let generos = [];
        if (generosCount === 0) {
            // Crear géneros
            const generosData = [
                { genero_nombre: 'Novela', descripcion: 'Narración en prosa de considerable extensión' },
                { genero_nombre: 'Poesía', descripcion: 'Composición literaria que se concibe como expresión artística' },
                { genero_nombre: 'Ciencia Ficción', descripcion: 'Género basado en elementos imaginarios' },
                { genero_nombre: 'Fantasía', descripcion: 'Género que incluye elementos mágicos y sobrenaturales' },
                { genero_nombre: 'Historia', descripcion: 'Obras basadas en hechos reales del pasado' }
            ];
            
            generos = await Genero.insertMany(generosData);
            console.log('Géneros de ejemplo creados.');
        } else {
            generos = await Genero.find();
        }
        
        // Verificar si ya hay autores
        const autoresCount = await Autor.countDocuments();
        
        let autores = [];
        if (autoresCount === 0) {
            // Crear autores
            const autoresData = [
                { autor_nombre: 'Gabriel García Márquez', autor_pais: 'Colombia', anio_nacimiento: 1927 },
                { autor_nombre: 'J.K. Rowling', autor_pais: 'Reino Unido', anio_nacimiento: 1965 },
                { autor_nombre: 'Haruki Murakami', autor_pais: 'Japón', anio_nacimiento: 1949 },
                { autor_nombre: 'Isabel Allende', autor_pais: 'Chile', anio_nacimiento: 1942 },
                { autor_nombre: 'Julio Cortázar', autor_pais: 'Argentina', anio_nacimiento: 1914 }
            ];
            
            autores = await Autor.insertMany(autoresData);
            console.log('Autores de ejemplo creados.');
        } else {
            autores = await Autor.find();
        }
        
        // Verificar si ya hay libros
        const librosCount = await Libro.countDocuments();
        
        if (librosCount === 0) {
            // Buscar IDs de géneros
            const novelaId = generos.find(g => g.genero_nombre === 'Novela')._id;
            const fantasiaId = generos.find(g => g.genero_nombre === 'Fantasía')._id;
            
            // Crear libros
            const librosData = [
                { 
                    libro_titulo: 'Cien años de soledad', 
                    anio_publicacion: 1967, 
                    genero: novelaId,
                    autores: [autores[0]._id] // García Márquez
                },
                { 
                    libro_titulo: 'Harry Potter y la piedra filosofal', 
                    anio_publicacion: 1997, 
                    genero: fantasiaId,
                    autores: [autores[1]._id] // Rowling
                },
                { 
                    libro_titulo: 'Tokio blues', 
                    anio_publicacion: 1987, 
                    genero: novelaId,
                    autores: [autores[2]._id] // Murakami
                },
                { 
                    libro_titulo: 'La casa de los espíritus', 
                    anio_publicacion: 1982, 
                    genero: novelaId,
                    autores: [autores[3]._id] // Allende
                },
                { 
                    libro_titulo: 'Rayuela', 
                    anio_publicacion: 1963, 
                    genero: novelaId,
                    autores: [autores[4]._id] // Cortázar
                }
            ];
            
            await Libro.insertMany(librosData);
            console.log('Libros de ejemplo creados con sus relaciones.');
        }
        
        console.log('Datos de ejemplo insertados correctamente.');
        
    } catch (error) {
        console.error('Error al insertar datos de ejemplo:', error);
    }
}

// Conectar a MongoDB e insertar datos
async function inicializarBaseDatos() {
    try {
        await mongoose.connect(MONGODB_URI);
        console.log('Conectado a MongoDB');
        
        // Eliminar la base de datos si existe
        console.log('Eliminando base de datos existente...');
        await mongoose.connection.dropDatabase();
        console.log('Base de datos eliminada correctamente.');
        
        await insertarDatosEjemplo();
        
        console.log('Configuración de la base de datos completada.');
        process.exit(0);
    } catch (error) {
        console.error('Error al configurar la base de datos:', error);
        process.exit(1);
    }
}

// Ejecutar inicialización
inicializarBaseDatos();