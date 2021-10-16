var slider1 = document.getElementById('amount');
var slider2 = document.getElementById('interest');
var slider3 = document.getElementById('year');
var output1 = document.getElementById('amount1');
var output2 = document.getElementById('interest1');
var output3 = document.getElementById('year1');

output1.innerHTML = slider1.value;
output2.innerHTML = slider2.value;
output3.innerHTML = slider3.value;

slider1.oninput = function () {
	output1.innerHTML = this.value;
	var out1 = output1;
	computeResults();
};
slider2.oninput = function () {
	output2.innerHTML = this.value;
	var out2 = output2;
	computeResults();
};
slider3.oninput = function () {
	output3.innerHTML = this.value;
	var out3 = output3;
	computeResults();
};

computeResults();

function computeResults(e) {
	const UIamount = slider1.value;
	const UIinterest = slider2.value;
	const UIyears = slider3.value;

	const principal = parseFloat(UIamount);
	const CalculateInterest = parseFloat(UIinterest) / 100 / 12;
	const calculatedPayments = parseFloat(UIyears) * 12;

	//Compute monthly Payment

	const x = Math.pow(1 + CalculateInterest, calculatedPayments);
	const monthly = (principal * x * CalculateInterest) / (x - 1);
	const monthlyPayment = monthly.toFixed(2);

	//Compute Interest
	const totalInterest = (monthly * calculatedPayments - principal).toFixed(2);

	//Compute Total Payment
	const totalPayment = (monthly * calculatedPayments).toFixed(2);

	//Show results
	document.getElementById('monthlyPayment').innerHTML = '$ ' + monthlyPayment;
	document.getElementById('totalInterest').innerHTML = '$ ' + totalInterest;
	document.getElementById('totalPayment').innerHTML = '$ ' + totalPayment;
}
