const mongoose = require('mongoose');

const generoSchema = new mongoose.Schema({
    genero_nombre: {
        type: String,
        required: true,
        unique: true
    },
    descripcion: {
        type: String
    }
}, {
    timestamps: {
        createdAt: 'created_at',
        updatedAt: 'updated_at'
    }
});

const Genero = mongoose.model('Genero', generoSchema);

module.exports = Genero;