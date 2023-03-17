

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
var db = fire.database();

  
  // Initialize Firebase

hilangkan("realtime");
hilangkan("form");
hilangkan("edit");
hilangkan("notAvailable");
resetButton();

munculkan("controller");

function munculkan(id){
    var elem = document.getElementById(id);
    if (elem.style.display === "none") {
        elem.style.display = "block";
    } else {
        elem.style.display = "none";
    }
}

function hilangkan(){
    var controller = document.getElementById("controller");
    // var form = document.getElementById("form");
    // var edit = document.getElementById("edit");
    var notAvailable = document.getElementById("notAvailable");
    var realtime = document.getElementById("realtime");

    controller.style.display = "none";
    // form.style.display = "none";
    // edit.style.display = "none";
    notAvailable.style.display = "none";
    realtime.style.display = "none";
}

function updateRules() {
    munculkan("edit");
    munculkan("form");
    munculkan("rules");

    var capacity = document.getElementById("capacity").value;
    var max_tmp = document.getElementById("max_tmp").value;

    firebase.database().ref("/").child("rules").update({
        Capacity: capacity,
        MaxTemp : max_tmp
    })

    document.getElementById("capacity2").innerHTML = capacity;
    document.getElementById("max_tmp2").innerHTML = max_tmp;
}
setInterval(function getData(){
    // firebase.database().ref("/Dashboard").once('value').then(function (snapshot) {
        // var ActiveGate = snapshot.val().ActiveGate;
        // var NoMask = snapshot.val().NoMask;
        // var OverTemperature = snapshot.val().OverTemperature;
        // var People = snapshot.val().People;
        // var PeopleEntered = snapshot.val().PeopleEntered;
        // var PeopleOut = snapshot.val().PeopleOut;
    var Temperature;
    var Moisture;
    var pH;
    var npk;
    var sensor = db.ref('sensor');
    sensor.on("value",showData,showError);
    function showData(item){
        Temperature = item.val().Temperature;
        Moisture = item.val().Moisture;
        pH = item.val().pH;
        npk = item.val().NPK;
    }
    function showError(err){
        console.log(err);
    }
    
    document.getElementById("Moisture").innerHTML = Moisture.toString();
    document.getElementById("Temperature").innerHTML = Temperature.toString();
    document.getElementById("pH").innerHTML = pH.toString();
    document.getElementById("NPK").innerHTML = npk;
}, 1000);
function resetButton(){
    var cmd = db.ref('cmd');
    cmd.child('button').set(0);
}
function sendData(id){
    var cmd = db.ref('cmd');
    cmd.child('button').set(id);
}
