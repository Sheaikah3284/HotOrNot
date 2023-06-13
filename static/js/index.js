let headersList = {
	Accept: "*/*",
	"User-Agent": "Thunder Client (https://www.thunderclient.com)",
};

const leftPic = document.querySelector("#leftPic");
console.log(leftPic);
const rightPic = document.querySelector("#rightPic");

fetch("http://localhost:5000/startRating", {
	method: "POST",
	headers: headersList,
}).then((res) => {
	res.json().then((data) => {
		console.log(data);
		leftPic.src = data.girl1Img;
		rightPic.src = data.girl2Img;
		leftPic.alt = data.girl1ID;
		rightPic.alt = data.girl2ID;
	});
});

const leftButton = document.querySelector("#leftBtn");
const rightButton = document.querySelector("#rightBtn");

leftButton.addEventListener("click", () => {
	updateRating(leftPic.alt, rightPic.alt);
});

rightButton.addEventListener("click", () => {
	updateRating(rightPic.alt, leftPic.alt);
});

function updateRating(winner, loser) {
	let headersList = {
		Accept: "*/*",
		"User-Agent": "Thunder Client (https://www.thunderclient.com)",
		"Content-Type": "application/json",
	};

	let bodyContent = JSON.stringify({
		winner: winner,
		loser: loser,
	});

	fetch("http://localhost:5000/rate", {
		method: "POST",
		body: bodyContent,
		headers: headersList,
	}).then((res) => {
		res.json().then((data) => {
			leftPic.src = data.girl1Img;
			rightPic.src = data.girl2Img;
			leftPic.alt = data.girl1ID;
			rightPic.alt = data.girl2ID;
		});
	});
}
