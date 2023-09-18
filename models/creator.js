const mongoose = require('mongoose')
const path = require('path')

const creatorSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    birthday: {
        type: String,
        required: true
    },
    dateCreateAcc: {
        type: Date,
        default: Date.now()
    },
    password: {
        type: String,
        required: true
    },
    avatar:{
        type: Buffer,
        default: null
    },
    avatarType: {
        type: String,
        default: "image/png"
    }
})

creatorSchema.virtual('creatorAvatar').get(function() {
    if(this.avatarType != null && this.avatar != null){
        return `data: ${this.avatarType};charset=utf-8;base64, ${this.avatar.toString('base64')}`
    }
})

module.exports = mongoose.model('Creator', creatorSchema)