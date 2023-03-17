var firebase = require('firebase')

const firebaseConfig = {
    apiKey: "AIzaSyDsccWUW75IWCHSC1XDPPv9ui8uMM7W1iE",
    authDomain: "robot-bottani.firebaseapp.com",
    databaseURL: "https://robot-bottani-default-rtdb.firebaseio.com",
    projectId: "robot-bottani",
    storageBucket: "robot-bottani.appspot.com",
    messagingSenderId: "428137751050",
    appId: "1:428137751050:web:5fb60391f7ff8dfd65f5f3",
    measurementId: "G-6DQE95F2MD"
  };
const fire = firebase.initializeApp(firebaseConfig);
var router = require('express').Router()

var body= require('body-parser');
var db = fire.database()
router.use(body.json())

router.get('/data', (req, res)=>{
    // db.settings({
    //     timestampsInSnapshots: true
    // })
    var allData = []
    db.collection('karyawan')
    .orderBy('waktu', 'desc').get()
    .then(snapshot => {
        snapshot.forEach((hasil)=>{
            allData.push(hasil.data())
        })
        console.log(allData)
        res.send(allData)
    }).catch((error)=>{
        console.log(error)
    })
})

router.post('/data', (req, res)=>{
    // db.settings({
    //     timestampsInSnapshots: true
    // })
    var data = db.ref('sensor');
    data.child('temperatur').set(200);
    data.on("value",showData,showError);
    function showData(item){
        res.send((item.val().temperatur).toString());
    }
    function showError(err){
        console.log(err);
    }
})

module.exports = router