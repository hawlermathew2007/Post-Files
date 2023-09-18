const { object } = require('joi')
const mongoose = require('mongoose')

const fileStorage = 'uploads/files'

const gameSchema = new mongoose.Schema({
    title: {
        type: String,
        require: true,
        maxLength: 3
    },
    description: {
        type: String
    },
    createdDate: {
        type: Date,
        default: Date.now()
    },
    coverImageType: {
        type: String,
        require: true
    },
    coverImage: {
        type: Buffer,
        require: true
    },
    creator: {
        type: mongoose.Schema.Types.ObjectId,
        require: true,
        ref: 'Creator'
    },
    listOfFiles: {
        type: Object,
        require: true
    }
})

gameSchema.virtual('coverImgPath').get(function() {
    if(this.coverImage != null && this.coverImageType != null){
        return `data:${this.coverImageType};charset=utf-8;base64, ${this.coverImage.toString('base64')}`
    }
})

module.exports = mongoose.model('Game', gameSchema)
module.exports.fileStorage = fileStorage