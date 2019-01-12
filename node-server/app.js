const express = require('express');
const path = require('path');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const multer = require('multer');
const session = require("express-session");
const flash = require("connect-flash");
const mongoose = require('mongoose');
const cors = require("cors");
const router = require('./routes');

const port = process.env.PORT || 3000;
const databaseURL = process.env.DATABASE || "mongodb://localhost:27017/paytm-hackathon";

// const fileStorage = multer.diskStorage({
// 	destination: (req, file, callback) => {
// 		callback(null, path.resolve(__dirname, 'uploads'));
// 	},
// 	filename: (req, file, callback) => {
// 		callback(null, new Date().toISOString() + '-' + file.originalname);
// 	}
// });

const fileStorage = multer.diskStorage({
	destination: './uploads/',
	filename: (req, file, callback) => {
		callback(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
	}
});

const fileFilter = (req, file, callback) => {
	if (
		file.mimetype === 'image/png' ||
		file.mimetype === 'image/jpg' ||
		file.mimetype === 'image/jpeg'
	) {
		callback(null, true);
	} else {
		callback(null, false);
	}
};

const app = express();
app.use(morgan("dev"));
app.use(cors());
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(cookieParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(multer({
	storage: fileStorage,
	fileFilter: fileFilter
}).single('image'));

app.use(express.static(path.join(__dirname, "public")));
app.use("/images", express.static(path.join(__dirname, "images")));
app.use("/uploads", express.static(path.join(__dirname, "uploads")));

mongoose.connect(databaseURL, { useNewUrlParser: true });
let database = mongoose.connection;
database.on('error', console.error.bind(console, "Could not connect to database"));
database.once('open', () => {
	console.log('connected to database.');
});

app.use(flash());

app.use(session({
		secret: "Session Secret",
		saveUninitialized: false,
		resave: false
	})
);

app.use((req, res, next) => {
	res.locals.success = req.flash('success');
	res.locals.error = req.flash('error');
	next();
})

app.use('/', router);

app.listen(port, () => {
	console.log(`Server running on port ${port}`);
})