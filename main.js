// const DB = require('.model.SQL.js');
// const API = require('.model.CPAPI.js');


// const fromEntries = (array) = {
//     return array.reduce((a, c) = { a[c[0]] = c[1]; return a }, {});
// };


const express = require('express');
const bodyParser = require('body-parser');
// const { get_DOC_IDS } = require('.model.SQL.js');
var etags = {
    "quz": 1
}
const app = express(), app_etag = (etag) => app.set('etag', (body, encoding) => etag);
app
    .use(function (req, res, next) {
        console.log(req.headers["if-none-match"]);
        if (etags[req.headers["if-none-match"]])next();
        app_etag('bar');
        res.sendFile('signup.html', { root: __dirname })
    })

    .use(function (req, res, next) {
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Headers', 'content-type');
        next();
    })
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json())

    .get('', (req, res) => {
        app.set('etag', function (body, encoding) {
            //  return etags[]"foo" })
            // console.log({body: body.toString()});
            return "quz";
        })
        return res.send('foo')
    })
    .get('', (req, res) => {

    })
app.listen(8080, () => console.log(`REST services started!`));
