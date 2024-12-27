function combineOtp() {
    const otp = [
        document.getElementById('otp1').value,
        document.getElementById('otp2').value,
        document.getElementById('otp3').value,
        document.getElementById('otp4').value,
        document.getElementById('otp5').value,
        document.getElementById('otp6').value
    ].join('');
    document.getElementById('otp_combined').value = otp;
    console.log(otp);
}

function moveToNext(current, nextFieldId) {
    // Check if the current input has a value
    if (current.value.length === current.maxLength) {
        // Move focus to the next field if it exists
        const nextField = document.getElementById(nextFieldId);
        if (nextField) {
            nextField.focus();
        }
    }
}

function allowOnlyNumbers(event) {
    // Remove any non-numeric characters
    event.target.value = event.target.value.replace(/[^0-9]/g, '');
}