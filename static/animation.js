function animateScore(targetScore) {
    let scoreElement = document.getElementById("anomaly-score");
    let riskElement = document.getElementById("risk-level");
    let currentScore = 0;
    let step = targetScore / 100;

    // Function to determine color and risk level
    function getScoreColor(score) {
        if (score <= 20) {
            return { color: 'green', risk: 'Low Risk' };
        } else if (score <= 50) {
            return { color: 'yellow', risk: 'Medium Risk' };
        } else if (score >50) {
            return { color: 'red', risk: 'High Risk' };
        } else {
			return { color: 'grey', risk: 'Not Defined' }
		}
    }

    function updateScore() {
        currentScore += step;
        if (currentScore >= targetScore) {
            scoreElement.innerText = targetScore.toFixed(2); // Final score
            let { color, risk } = getScoreColor(targetScore);
            scoreElement.style.color = color;
            riskElement.innerText = risk;
        } else {
            scoreElement.innerText = currentScore.toFixed(2);
            let { color, risk } = getScoreColor(currentScore);
            scoreElement.style.color = color;
            riskElement.innerText = risk;
            requestAnimationFrame(updateScore);
        }
    }
    updateScore();
}
