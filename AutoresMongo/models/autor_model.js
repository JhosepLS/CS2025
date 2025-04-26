const mongoose = require('mongoose');

const autorSchema = new mongoose.Schema({
    autor_nombre: {
        type: String,
        required: true
    },
    autor_pais: {
        type: String
    },
    anio_nacimiento: {
        type: Number,
        validate: {
            validator: function(value) {
                return !value || (value >= 0 && value <= 2100);
            },
            message: "El año de nacimiento debe estar entre 0 y 2100"
        }
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

// Validación para nombres duplicados
autorSchema.path('autor_nombre').validate(async function(value) {
    const count = await this.constructor.countDocuments({
        autor_nombre: value,
        _id: { $ne: this._id },
        is_active: true
    });
    return count === 0;
}, 'Ya existe un autor con ese nombre');

const Autor = mongoose.model('Autor', autorSchema);

module.exports = Autor;