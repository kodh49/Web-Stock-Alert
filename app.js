const express = require("express");
const path = require("path");
const app = express();
const spawn = require("child_process").spawn;
const bodyParser = require("body-parser");
const schedule = require("node-schedule");

app.use(bodyParser());

// Set interval
var rule = new schedule.RecurrenceRule();
rule.minute = 30;

// Endpoint at localhost:3000/
app.get("/", (req, res) => {
  res.send("<h1>Main Page</h1>");
});

// Endpoint at localhost:3000/add
app.get("/add", function (req, res) {
  res.send("<h1>Add Page</h1>");
});

app.post("/add", function (req, res) {
  console.log(
    "/add    Request | ",
    "UID: ",
    req.body.user_id,
    "USERNAME: ",
    req.body.user_name,
    "VALUE: ",
    req.body.text
  );
  const user_id = req.body.user_id;
  const user_name = req.body.user_name;
  const stockName = req.body.text;
  // Run Python Code in JS
  const result = spawn("python3", [
    "./pysrc/database/add.py",
    user_id,
    user_name,
    stockName,
  ]);
  result.stdout.on("data", function (data) {
    console.log(data.toString());
  });
  const msg =
    req.body.user_name +
    "님, 관심종목에" +
    req.body.text +
    "이(가) 추가되었습니다.";
  res.send(msg);
});

// Endpoint at localhost:3000/delete
app.get("/delete", function (req, res) {
  res.send("<h1>Delete Page</h1>");
});

app.post("/delete", function (req, res) {
  console.log(
    "/delete Request | ",
    "UID: ",
    req.body.user_id,
    "USERNAME: ",
    req.body.user_name,
    "VALUE: ",
    req.body.text
  );
  const user_id = req.body.user_id;
  const user_name = req.body.user_name;
  const stockName = req.body.text;
  // Run Python Code in JS
  const result = spawn("python3", [
    "./pysrc/database/delete.py",
    user_id,
    user_name,
    stockName,
  ]);
  result.stdout.on("data", function (data) {
    console.log(data.toString());
  });
  const msg =
    req.body.user_name +
    "님, 등록하신 관심종목" +
    req.body.text +
    "이(가) 삭제되었습니다.";
  res.send(msg);
});

// Endpoint at localhost:3000/max
app.get("/max", function (req, res) {
  res.send("<h1>Max Page</h1>");
});

app.post("/max", function (req, res) {
  console.log(
    "/max    Request | ",
    "UID: ",
    req.body.user_id,
    "USERNAME: ",
    req.body.user_name,
    "VALUE: ",
    req.body.text
  );
  const user_id = req.body.user_id;
  const user_name = req.body.user_name;
  const stockName = req.body.text;
  // Run Python Code in JS
  const result = spawn("python3", [
    "./pysrc/database/setMax.py",
    user_id,
    user_name,
    stockName,
  ]);
  result.stdout.on("data", function (data) {
    console.log(data.toString());
  });
  const msg =
    req.body.user_name +
    "님, " +
    req.body.text +
    "%보다 상승할 시 알림이 전송됩니다.";
  res.send(msg);
});

// Endpoint at localhost:3000/min
app.get("/min", function (req, res) {
  res.send("<h1> Page</h1>");
});

app.post("/min", function (req, res) {
  console.log(
    "/min    Request | ",
    "UID: ",
    req.body.user_id,
    "USERNAME: ",
    req.body.user_name,
    "VALUE: ",
    req.body.text
  );
  const user_id = req.body.user_id;
  const user_name = req.body.user_name;
  const stockName = req.body.text;
  // Run Python Code in JS
  const result = spawn("python3", [
    "./pysrc/database/setMin.py",
    user_id,
    user_name,
    stockName,
  ]);
  result.stdout.on("data", function (data) {
    console.log(data.toString());
  });
  const msg =
    req.body.user_name +
    "님, " +
    req.body.text +
    "%보다 하락할 시 알림이 전송됩니다.";
  res.send(msg);
});

// Endpoint at localhost:3000/show
app.get("/show", function (req, res) {
  res.send("<h1>Show List Page</h1>");
});

app.post("/show", function (req, res) {
  console.log(
    "/show   Request | ",
    "UID: ",
    req.body.user_id,
    "USERNAME: ",
    req.body.user_name
  );
  const user_id = req.body.user_id;
  const user_name = req.body.user_name;
  // Run Python Code in JS
  const result = spawn("python3", [
    "./pysrc/database/showStr.py",
    user_id,
    user_name,
  ]);
  let msg = "등록하신 관심종목입니다\n";
  result.stdout.on("data", function (data) {
    msg += data.toString();
  });
  result.on("close", (code) => {
    res.send(msg);
  });
});

app.listen(process.env.PORT || 3000, () => {
  console.log("Express.js Server has launched");
});

// Define regularSchedule child process here: No Parameter Passed
function regularAlert() {
  const result = spawn("python3", ["regularSchedule.py"]);
  result.stdout.on("data", (data) => {
    console.log(data.toString());
  });
}

const regularJ = schedule.scheduleJob(rule, regularAlert);

/*
Define specialSchedule child process here
Use setTiemout(func) << to add schedule on every possible sec
*/

function specialAlert() {
  const result = spawn("python3", ["specialSchedule.py"]);
  result.stdout.on("data", (data) => {
    console.log(data.toString());
  });
}

setInterval(specialAlert, 15000);
