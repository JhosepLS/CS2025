const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const dotenv = require('dotenv');
dotenv.config();

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/biblioteca_db';

// Esquema de usuario para este script
const userSchema = new mongoose.Schema({
    username: {
        type: String,
        required: true,
        unique: true
    },
    password: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true,
        unique: true
    },
    role: {
        type: String,
        enum: ['usuario', 'admin'],
        default: 'usuario'
    },
    is_active: {
        type: Boolean,
        default: true
    }
}, {
    timestamps: {
        createdAt: 'created_at',
        updatedAt: 'updated_at'
    }
});

const User = mongoose.model('User', userSchema);

async function createAdmin() {
    try {
        await mongoose.connect(MONGODB_URI);
        console.log('Conectado a MongoDB');
        
        // Verificar si ya existe un usuario admin
        const existingAdmin = await User.findOne({ username: 'admin' });
        
        if (existingAdmin) {
            console.log('Eliminando usuario admin existente...');
            await User.deleteOne({ username: 'admin' });
        }
        
        // Crear nueva contraseña hasheada
        const password = 'admin123';
        const hashedPassword = await bcrypt.hash(password, 10);
        
        // Crear usuario admin
        const admin = new User({
            username: 'admin',
            password: hashedPassword,
            email: 'admin@biblioteca.com',
            role: 'admin',
            is_active: true
        });
        
        await admin.save();
        
        console.log(`
Usuario administrador creado con éxito:
Username: admin
Password: admin123
Role: ${admin.role}
Email: ${admin.email}
        `);
        
        // Cerrar conexión
        await mongoose.connection.close();
        console.log('Conexión cerrada');
        
    } catch (error) {
        console.error('Error al crear usuario admin:', error);
    }
}

createAdmin();