function main(params) {

    secret = {
        "COUCH_URL": "",
        "IAM_API_KEY": "",
        "COUCH_USERNAME": ""
    };

    return new Promise(function (resolve, reject) {
        const Cloudant = require('@cloudant/cloudant');
        const cloudant = Cloudant({
            url: secret.COUCH_URL,
            plugins: { iamauth: { iamApiKey: secret.IAM_API_KEY } }
        });

        const dealershipDb = cloudant.use('dealerships');

        if (params.state) {
            // return dealership with this state 
            dealershipDb.find({
                "selector": {
                    "st": {
                        "$eq": params.state
                    }
                }
            }, function (err, result) {
                if (err) {
                    console.log("🚀 ~ file: index.js ~ line 20 ~ err", err)
                    reject(err);
                }

                let code = 200;
                if (result.docs.length == 0) {
                    code = 404;
                }

                resolve({
                    statusCode: code,
                    headers: { 'Content-Type': 'application/json' },
                    body: result.docs
                });
            });
        } else if (params.id) {
            id = parseInt(params.dealerId)
            // return dealership with this id 
            dealershipDb.find({ selector: { id: parseInt(params.id) } }, function (err, result) {
                if (err) {
                    console.log("🚀 ~ file: index.js ~ line 20 ~ err", err)
                    reject(err);
                }

                let code = 200;
                if (result.docs.length == 0) {
                    code = 404;
                }

                resolve({
                    statusCode: code,
                    headers: { 'Content-Type': 'application/json' },
                    body: result.docs[0]
                });
            });

        } else {
            // return all documents 
            dealershipDb.list({include_docs:true}, function (err, result) {

                if (err) {
                    console.log("🚀 ~ file: index.js ~ line 35 ~ err", err)
                    reject(err);
                }

                formatted_results = result.rows.map((row) => {
                    row_doc = row.doc;
                    item = {
                        'id': row_doc.id,
                        'city': row.doc.city,
                        'state': row_doc.state,
                        'st': row_doc.st,
                        'address': row_doc.address,
                        'zip': row_doc.zip,
                        'lat': row_doc.lat,
                        'long': row_doc.long,
                        'short_name': row_doc.short_name,
                        'full_name': row_doc.full_name
                    };
                    return item;
                })

                resolve({
                    statusCode: 200,
                    headers: { 'Content-Type': 'application/json' },
                    body: formatted_results
                });
            });
        }
    });
}