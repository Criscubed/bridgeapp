const express = require('express')
const app = express()
const port = 5500
const sqlite3 = require('sqlite3')

app.use(express.static('public'));

app.get('/b', (req,res) => {
    const {x} = req.query
    querydb(x, getResponse, res);
})



app.listen(port, () => console.log(`server has started on port: ${port}`));

function getResponse(res, pt_information){
    res.status(200).json(pt_information)
}

function querydb(pt_number, callback, res){
    // open the database
    let obj = "HECK";
    let db = new sqlite3.Database('./bridge.db', sqlite3.OPEN_READONLY, (err) => {
        if (err) {
        console.error(err.message);
        }
        console.log('Connected to the bridge database.');
    });

    db.serialize(() => {
        db.each('SELECT * FROM bridge WHERE pt_number = "' + pt_number + '"', (err, row) => {
            if (err) {
            console.error(err.message);
            }
            obj = row;
        });
    });
    db.close((err) => {
        if (err) {
        console.error(err.message);
        }
        console.log('Closed the database connection.');
        callback(res, obj);
    });
    
}