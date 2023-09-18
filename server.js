if (process.env.NODE_ENV !== 'production'){
    require('dotenv').config()
}

const express = require('express')
const expressLayout = require('express-ejs-layouts')
const path = require('path')
const indexRoutes = require('./routes/index')
const creatorRoutes = require('./routes/creators')
const gameRoutes = require('./routes/games')
const bodyParser = require('body-parser')
const cookieParser = require("cookie-parser")
const flash = require('express-flash')
const session = require('express-session')
const expressZip = require('express-zip')
const methodOverride = require('method-override')
const passport = require('passport')
const app = express()

app.set('view engine', 'ejs')
app.set('views', __dirname + '/views')
app.set('layout', 'layouts/layout.ejs')
app.use(expressLayout)
app.use(express.static(__dirname + '/public'));
app.use(methodOverride('_method'))
app.use('/public', express.static('public'))
app.use(express.urlencoded({ extended: false })) // let us get the information from the form
app.use(bodyParser.urlencoded({ limit: '10mb', extended: false}))
app.use(session({ // allow the user to persist across the page
    secret: process.env.SESSION_SECRET,
    resave: false, // should we resave our section variable? if nothing has changed then false
    saveUninitialized: false // should we save an empty value in the session? if no value then dont save
}))
app.use(flash())
app.use(cookieParser())
app.use(passport.session())
app.use(passport.initialize())

const mongoose = require('mongoose')
const { required } = require('joi')
mongoose.connect(process.env.DATABASE_URL, { useNewUrlParser: true })
// when making web with non deploy then just connect with local MongoDB else then it will be the server on the web somewhere
const db = mongoose.connection
db.on('error',  error => console.error(error))
db.once('open',  () => console.log('Connected to mongoose'))

const Game = require('./models/games')

app.get('/download/:id', checkAuth, async (req, res) => {
    try{
        files = []
        const game = await Game.findById(req.params.id)
        game.listOfFiles.forEach(file => {
            files.push({ path: path.join(__dirname, file.path), name: file.originalname })
        })
        res.zip(files)
    } catch(e){
        console.log(e)
        res.redirect(`games/${req.params.id}`)
    }
})

app.get('/logout', checkAuth,(req,res) => {
    req.session.destroy();
    res.redirect('/login');
});

function checkAuth(req, res, next) {
    if (req.isAuthenticated()) {
        return next()
    }
    res.redirect('/login')
}

app.use('/', indexRoutes)
app.use('/creators', creatorRoutes)
app.use('/games', gameRoutes)

app.listen(process.env.PORT || 3000, () => console.log('Listening'))