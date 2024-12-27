const timerDisplay = document.getElementById("timer");
let timeLeft = 120; // 2 minutes in seconds

const countdown = setInterval(() => {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    timerDisplay.textContent = `Time Remaining: ${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    
    if (timeLeft <= 0) {
        clearInterval(countdown);
        timerDisplay.textContent = "Time Expired. Please Resend OTP.";
    }

    timeLeft--;
}, 1000);