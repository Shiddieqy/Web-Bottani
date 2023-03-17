const homeController = {};

homeController.index = (req,res)=>{
    res.render('index.html');
}

module.exports = homeController;
