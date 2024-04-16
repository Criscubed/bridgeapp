const express = require('express')
const app = express()
const sqlite3 = require('sqlite3')

const port = 5500

// you need to run: 
// npm run dev 
// to get this working

// index.ejs file needs an ejs view engine to render
app.set('view engine', 'ejs')
// express.js serves the files in the public folder to user
app.use(express.static('public'));

// any text sent as a parameter to the base url gets turned into a database query 
// to-do: stop users from sending too many database requests
app.get('/:id', (req, res) => {
    querydb(req.params.id, getResponse, res);
})

app.listen(port, () => console.log(`server has started on port: ${port}`));

// callback method used so that res.render() gets called after the database query
function getResponse(res, pt_information) {
    //json in the response should have data from the database
    res.render("index", pt_information)
}


function querydb(pt_number, callback, res) {
    // open the database
    let obj = { null: null };
    let db = new sqlite3.Database('./bridge.db', sqlite3.OPEN_READONLY, (err) => {
        if (err) {
            console.error(err.message);
        }
        console.log('Connected to the bridge database.');
    });

    // input pt_number -> output row which gets assigned to obj
    db.serialize(() => {
        db.each('SELECT * FROM bridge WHERE pt_number = "' + pt_number + '"', (err, row) => {
            if (err) {
                console.error(err.message);
            }
            //row contains information from the database
            obj = row;
        });
    });

    // close connection and call the callback function
    db.close((err) => {
        if (err) {
            console.error(err.message);
        }
        console.log('Closed the database connection.');
        //calback should be getResponse(res, obj)
        callback(res, obj);
    });

}