const fetch = require("node-fetch");
var inpt = { msg: "hi" };

fetch("http://127.0.0.1:5000/response", {
  method: "POST",
  body: JSON.stringify(inpt), // string or object
  headers: {
    "Content-Type": "application/json",
  },
}).then(data=>{return data.json()})
  .then(res=>(console.log(res)))
  .catch((err) => {
    console.log(err);
  });;
