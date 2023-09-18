const express = require('express')
const router = express.Router()
const bcrypt = require('bcrypt')
const passport = require('passport')
const path = require('path')
const Game = require('../models/games')
const localStrategy = require('passport-local').Strategy
const Creator = require('../models/creator.js')
const multer = require('multer')
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
global.document = new JSDOM('../views/layouts/layout.ejs').window.document


async function getUserById(id) {
    return await Creator.findById(id)
}

// when ever the client submit data though method POST form the func will ca called though passport.authenticate('local')
// usernameField by the default is 'username' if in the input that will get name value doesnt have the same name as username
// then it must be { usernameField: 'the name u named in that input' } in para 1
// the secpara is a callback func that will accept 3 args which username, passwaord and done func
// username in here will be req.body.name and password will be req.body.password which the same with data get from form
// done function will be called when client done authenticating
// done: para1: error || null, para2: user || false (no user is given), para3: message will be send to the client though flash

passport.use(new localStrategy( {usernameField: 'name'},
    async function(username, password, done) {
        const user = await Creator.findOne({ name: username })
        if (user == null) { return done(null, false, { message: 'No user with that name' }); }
        try {
            if (await bcrypt.compare(password, user.password)) {
                return done(null, user)
            } else if (user.name.length < 5){
                return done(null, false, { message: 'Your name must have above 5 characters' })
            } else{
                return done(null, false, { message: 'Password incorrect!' })
            }
        } catch(e) {
            return done(e)
        }
    }
));
passport.serializeUser( (user, done) => done(null, user.id) )   // add the user id to the session
passport.deserializeUser( (id, done) => {
    return done(null, getUserById(id))  // get the full information about the user from session and pass it to req.user
})  

router.get('/', checkAuth, async (req, res) =>{
    console.log(req.session)
    let searchOptions = {}
    if(req.query.name != '' && req.query.name != null){
        searchOptions.title = new RegExp(req.query.name, 'i')
    }
    const user = await Creator.findById(req.session.passport.user)
    const games = await Game.find(searchOptions)
    res.render('index.ejs', {
        user: user,
        games: games,
        sectionPath: './indexPartial/searchSection.ejs',
        searchOptions: req.body
    })
})

router.get('/login', checkNotAuth, async (req, res) => {
    res.render('authentication/login.ejs')
})

router.get('/register', checkNotAuth,(req, res) => {
    res.render('authentication/register.ejs')
    console.log('2007-08-24'.split('-'))
})

router.post('/register', checkNotAuth,async (req, res) => {
    try{
        const hashedPassword = await bcrypt.hash(req.body.password, 10)
        const creator = new Creator({
            name: req.body.name,
            birthday: req.body.date,
            password: hashedPassword
        })
        const creators = await Creator.find({})
        creators.forEach(creator => {
            if (creator.name == req.body.name){
                res.render('authentication/register.ejs', { errorMessage: 'Sorry, this name is already taken.' })
                return
            }
        })
        const newCreator = await creator.save()
        const upload = multer({
            storage: multer.diskStorage({
                destination: path.join('public', Game.fileStorage, newCreator.id),
                filename: (req, file, cb) => {
                    cb(null, file.originalname)
                }
            })
        })
        res.redirect('/login')
    } catch (e) {
        res.render('authentication/register.ejs', { errorMessage: 'Error Registing' })
        console.log(e)
    }
})

router.post('/login', checkNotAuth, passport.authenticate('local', {
    successRedirect: '/',
    failureRedirect: '/login',
    failureFlash: true
}))


function checkAuth(req, res, next) {
    if (req.isAuthenticated()) {
        return next()
    }
    res.redirect('/login')
}

function checkNotAuth(req, res, next) {
    if (req.isAuthenticated()) {
        res.redirect('/')
    }
    next()
}

module.exports = router