const mongoose = require('mongoose');

const { Schema } = mongoose;

const FileSchema = new Schema({
    owner: { type: Schema.Types.ObjectId, ref: 'User' },
    content: { type: String, required: true },
    parsed: { type: String, required: true },
    name: { type: String, required: true },
}, {
    timestamps: true
});

const FileModel = mongoose.model('File', FileSchema);

module.exports = {
    FileModel,
    FileSchema
}
