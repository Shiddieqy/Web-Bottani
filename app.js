var express = require('express')
var bodyParser = require('body-parser')
var cors = require('cors')
var routeSaya = require('./models/route')
const homeController = require('./controllers/homeController')

var app = express()
app.use(cors())
app.use(bodyParser.json())
app.use(routeSaya)
app.set('view-engine','html');
app.engine('html',require('ejs').renderFile);

app.use(express.static('public'));
app.get('/',homeController.index);

app.listen(3000,()=>{
    console.log('port 3000');
})



