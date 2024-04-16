const express = require('express')
const app = express()
const port = 5500
const sqlite3 = require('sqlite3')

app.set('view engine', 'ejs')
// run npm run dev to get this working
app.use(express.static('public'));

app.get('/:id', (req, res) => {
    querydb(req.params.id, getResponse, res);
})

app.listen(port, () => console.log(`server has started on port: ${port}`));

function getResponse(res, pt_information){
    //json in the response should have data from the database
    res.render("index", pt_information)
}

function querydb(pt_number, callback, res){
    // open the database
    let obj = {null: null};
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
            //row contains information from the database
            obj = row;
        });
    });
    db.close((err) => {
        if (err) {
        console.error(err.message);
        }
        console.log('Closed the database connection.');
        //calback should be getResponse(res, obj)
        callback(res, obj);
    });
    
}