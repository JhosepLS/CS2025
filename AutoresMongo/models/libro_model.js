const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const libroSchema = new mongoose.Schema({
    libro_titulo: {
        type: String,
        required: true
    },
    anio_publicacion: {
        type: Number,
        validate: {
            validator: function(value) {
                return !value || (value >= 0 && value <= 2100);
            },
            message: "El año de publicación debe estar entre 0 y 2100"
        }
    },
    genero: {
        type: Schema.Types.ObjectId,
        ref: 'Genero',
        required: true
    },
    autores: [{
        type: Schema.Types.ObjectId,
        ref: 'Autor'
    }],
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

// Validación para títulos duplicados
libroSchema.path('libro_titulo').validate(async function(value) {
    const count = await this.constructor.countDocuments({
        libro_titulo: value,
        _id: { $ne: this._id },
        is_active: true
    });
    return count === 0;
}, 'Ya existe un libro con ese título');

const Libro = mongoose.model('Libro', libroSchema);

module.exports = Libro;