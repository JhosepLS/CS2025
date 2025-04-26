const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');

// Cargar variables de entorno
dotenv.config();

// Importar rutas
const authRoutes = require('./routes/auth_routes');
const autorRoutes = require('./routes/autor_routes');
const libroRoutes = require('./routes/libro_routes');
const generoRoutes = require('./routes/genero_routes');

// Importar middleware de errores
const errorHandler = require('./middlewares/error_middleware');

// Inicializar Express
const app = express();

// Middlewares
app.use(cors());
app.use(express.json());

// Registrar rutas
app.use(authRoutes);
app.use(autorRoutes);
app.use(libroRoutes);
app.use(generoRoutes);

// Ruta raíz
app.get('/', (req, res) => {
    res.json({ mensaje: '¡Bienvenido a la API de Biblioteca con MongoDB!' });
});

// Ruta para verificar estado
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', version: '1.0.0' });
});

// Middleware de manejo de errores
app.use(errorHandler);

// Conectar a MongoDB y arrancar servidor
const PORT = process.env.PORT || 5000;
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/biblioteca_db')
    .then(() => {
        console.log('Conectado a MongoDB');
        app.listen(PORT, () => {
            console.log(`Servidor en ejecución en el puerto ${PORT}`);
        });
    })
    .catch(err => {
        console.error('Error al conectar a MongoDB:', err);
        process.exit(1);
    });