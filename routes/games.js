const express = require('express')
const path = require('path')
const fs = require('fs')
const router = express.Router()
const Game = require('../models/games')
const Creator = require('../models/creator')
const multer = require('multer')
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, path.join('public', Game.fileStorage, req.session.passport.user))
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname)
    }
})
const upload = multer({ storage: storage, limits: { fieldSize: 25 * 1024 * 1024 } })


router.get('/:id', checkAuth,async (req, res) => {
    try{
        const games = await Game.find({})
        games.forEach(async (game) => {
            if(game.id === req.params.id){
                const creator = await Creator.findById(game.creator)
                res.render('games/gameIndv.ejs' , { 
                    game: game,
                    creator: creator
                })
                return
            }
        })
    } catch{
        res.status(404).send('id not found dumbass')
    }
})

router.post('/', checkAuth, upload.array('game'), async (req, res) => {
    const cover = JSON.parse(req.body.image)
    if (cover != null && ['image/png', 'image/jpg', 'image/svg'].includes(cover.type)) {
        coverImage = new Buffer.from(cover.data, 'base64')
        coverImageType = cover.type
    } else{
        res.redirect(`/creators/${req.session.passport.user}`)
        unlinkFile(req.files, req.session.passport.user)
        return
    }
    const game = new Game({
        title: req.body.title,
        description: req.body.description,
        creator: req.session.passport.user,
        listOfFiles: req.files,
        coverImage: coverImage,
        coverImageType: coverImageType
    })
    try{
        const newGame = await game.save()
        res.redirect('/')
    } catch(e){
        console.log(e)
        unlinkFile(req.files, req.session.passport.user)
        res.redirect(`/creators/${req.session.passport.user}`)
    }
})

function unlinkFile(arrayFiles, directoryId) {
    if(arrayFiles != null){
        for(var i=0; i < arrayFiles.length; i+=1){
            fs.unlink(path.join('public', Game.fileStorage, directoryId, arrayFiles[i].originalname), err => {
                if (err) console.error(err)
            })
        }
    }
}

function checkAuth(req, res, next) {
    if (req.isAuthenticated()) {
        return next()
    }
    res.redirect('/login')
}


module.exports = router