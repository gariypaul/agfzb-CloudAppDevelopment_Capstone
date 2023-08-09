const express = require('express');

const app = express();
const port = 3000;
const Cloudant = require('@cloudant/cloudant');



// Initialize Cloudant connection
function dbCloudantConnect() {

    secret = {
        "COUCH_URL": "https://52c0d074-8afe-4d63-87f8-bd5e6d7e8ad8-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY":"klGbAyO_sHmbvPfn5x0eh4isZw0dR7Yms-Bcn6ko7kfv",
        "COUCH_USERNAME": "52c0d074-8afe-4d63-87f8-bd5e6d7e8ad8-bluemix"
        };
    return new Promise((resolve, reject) => {
        Cloudant({  // eslint-disable-line
            url: secret.COUCH_URL, //please enter your url here
            plugins: {iamauth: {iamApiKey:secret.IAM_API_KEY}}
        }, ((err, cloudant) => {
            if (err) {
                console.error('Connect failure: ' + err.message + ' for Cloudant DB');
                reject(err);
            } else {
                let db = cloudant.use("dealerships");
                console.info('Connect success! Connected to DB');
                resolve(db);
            }
        }));
    });
}

let db;

dbCloudantConnect().then((database) => {
    db = database;
}).catch((err) => {
    throw err;
});


app.use(express.json());


// Define a route to get all dealerships with optional state and ID filters
app.get('/dealerships/get', (req, res) => {
    const { state, id } = req.query;
    
    // Create a selector object based on query parameters
    const selector = {};
    if (state) {
      selector.state = state;
    }
    if (id) {
      selector._id = id;
    }
    
    const queryOptions = {
      selector,
      limit: 10, // Limit the number of documents returned to 10
    };
    
    db.find(queryOptions, (err, body) => {
      if (err) {
        console.error('Error fetching dealerships:', err);
        res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
      } else {
        const dealerships = body.docs;
        res.json(dealerships);
      }
    });
  });
  
  const PORT = process.env.PORT || 3000;
  
  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
  });