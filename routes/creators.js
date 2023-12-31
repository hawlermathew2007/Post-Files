const express = require('express')
const Game = require('../models/games')
const Creator = require('../models/creator')
const router = express.Router()

router.get('/', checkAuth, async (req, res) => {
    searchOptions = {}
    console.log(req.session)
    if(req.query.name != '' && req.query.name != null){
        searchOptions.name = new RegExp(req.query.name, 'i')
    }
    try{
        const users = await Creator.find(searchOptions)
        const user = await Creator.findById(req.session.passport.user)
        res.render('index.ejs', {
            users: users,
            user: user,
            searchOptions: req.query,
            sectionPath: './indexPartial/userSection.ejs'
        })
    } catch{
        res.redirect('/')
    }
})

router.get('/:id', checkAuth, async (req, res) => {
    try{
        const creators = await Creator.find({})
        const games = await Game.find({})
        creators.forEach(creator => {
            if(creator.id === req.params.id){
                if(creator.id === req.session.passport.user){
                    res.render('creators/mainCreator.ejs', { creator: creator, games: games })
                } else{
                    res.render('creators/otherCreator.ejs', { creator: creator, games: games })
                }
                return
            }
        })
    } catch{
        res.status(404).send("id not found dumbass")
    }
})

router.get('/:id/edit', checkAuth,async (req,res) => {
    const creator = await Creator.findById(req.params.id)
    if(creator == null) {
        res.status(404).send('id not found dumbass')
        return
    }
    try{
        res.render('creators/edit.ejs', { creator: creator, useBack: {}})
    } catch{
        res.redirect(`/creators/${req.params.id}`)
    }
})

router.put('/:id', async (req, res) => {
    let creator;
    try{
        creator = await Creator.findById(req.params.id)
        console.log(req.body)
        if (req.body.newName != '' && req.body.newName != null){
            creator.name = req.body.newName
        }
        if (req.body.newBd != ''  && req.body.newBd != null){
            creator.birthday = req.body.newBd
        }
        if (req.body.image != ''  && req.body.image != null){
            const cover = JSON.parse(req.body.image)
            if (cover != null && ['image/png', 'image/jpg', 'image/svg'].includes(cover.type)) {
                creator.avatar = new Buffer.from(cover.data, 'base64') 
                creator.avatarType = cover.type
            }
        }
        if (req.body.fb != '' && req.body.fb != null){
            if(req.body.fb.includes('https://') && req.body.instaLink.includes('facebook.com')){
                creator.fbLink = req.body.fb
            } else{
                res.render('creators/edit.ejs', { errorMessage: 'Please enter a Facebook link' ,useBack: req.body, creator: creator })
                return
            }
        }
        if (req.body.insta != '' && req.body.insta != null){
            if(req.body.insta.includes('https://') && req.body.instaLink.includes('instagram.com')){
                creator.instaLink = req.body.insta
            }else{
                res.render('creators/edit.ejs', { errorMessage: 'Please enter a Instagram link' ,useBack: req.body, creator: creator })
                return
            }
        }
        if (req.body.git != '' && req.body.git != null){
            if(req.body.git.includes('https://') && req.body.instaLink.includes('github.com')){
                creator.githubLink = req.body.git
            } else{
                res.render('creators/edit.ejs', { errorMessage: 'Please enter a github link' ,useBack: req.body, creator: creator })
                return
            }
        }
        if (req.body.decription != '' && req.body.decription != null){
            creator.creatorDescription = req.body.decription
            console.log('success', creator.creatorDescription)
        }
        await creator.save()
        console.log('success', creator)
        res.redirect(`/creators/${req.params.id}`)
    } catch{
        res.redirect(`/creators/${req.params.id}/edit`)
    }
})

function checkAuth(req, res, next) {
    if (req.isAuthenticated()) {
        return next()
    }
    res.redirect('/login')
}


module.exports = router