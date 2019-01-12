const path = require('path');
const fs = require('fs');
const request = require('request-promise');
const FormData = require('form-data');
const fileHelper = require('../utils/file');

const cleanInput = (input) => {
	let cleanInput = '';
	for(let i = 0; i < input.length; i++) {
		if(input[i] == ' ') {
			cleanInput += '-';
		} else {
			cleanInput += input[i];
		}
	}
	return cleanInput;
}

module.exports = homeController = {
	getHome: (req, res, next) => {
		console.log(path.resolve(__dirname, '..', 'uploads'));
		res.render('home', {path: '/', hasError: false, errorMessage: ''});
	},

	postImage: async (req, res, next) => {
		const image = req.file;
		console.log(image);
		if (!image) {
			return res.status(422).render('home', {
				path: '/',
				hasError: true,
				errorMessage: 'Attached file is not an image.',
			});
		}
		
		const imageUrl = image.path;
		const url = 'http://localhost:33507';
		const imagePath = `${__dirname}/../${imageUrl}`
		console.log("imagePath", imagePath);
		// res.redirect('/Apple/Apple-Scab');
		request.post({
			url: "https://agrilearning-api.herokuapp.com/", formData: {
		    file: fs.createReadStream(imagePath),
		}})
		    .then(data => {
					console.log(typeof data);
					data = JSON.parse(data);
					let arr = data.response.split("-");
					let crop = arr[0].trim();
					let disease = arr[1].trim();
					fileHelper.deleteFile(imagePath);
					if (disease === 'Health') {
						req.flash("success", "Your crop has no disease!");
						res.redirect('/');
					} else {
						let cleanCrop = cleanInput(crop);
						let cleanDisease = cleanInput(disease);
						res.redirect(`/${cleanCrop}/${cleanDisease}`);
					}
		    }).catch(err => {
					console.log("error");
					next(new Error("Could Not Get response from ML api"));
		    });
		// let pyScriptPath = path.join(__dirname, "../pyScript/app.py");
		// console.log("py", pyScriptPath);
		// const pyProg = spawn("python", [pyScriptPath, JSON.stringify({ imageUrl })]);
  // 		pyProg.stdout.on("data", data => {
  // 			console.log(data.toString());
  //   		res.json(data.toString());
  // 		});

  // 		pyProg.stderr.on("data", data => {
  //   		console.log(`stderr: ${data}`);
  // 		});
	},
}

// image object:
// { fieldname: 'image',
//   originalname: 'insect.jpg',
//   encoding: '7bit',
//   mimetype: 'image/jpeg',
//   destination: './uploads',
//   filename: '2019-01-11T08:00:31.859Z-insect.jpg',
//   path: 'uploads/2019-01-11T08:00:31.859Z-insect.jpg',
// 	size: 173814 }
	
// imageURL:
// uploads/2019-01-11T08:00:31.859Z-insect.jpg