// get_doctor_id.js
document.getElementById('check-availabilities-btn').addEventListener('click', function() {
    var selectedDoctor = document.getElementById('doctor-select').value;
    
    // Retirer les antislash et les guillemets
    var selectedDoctorId = selectedDoctor.replace(/\\/g, '').replace(/"/g, '');

    // Rediriger vers la vue get_availabilities avec l'ID du docteur
    window.location.href = '/get_availabilities/?doctor_id=' + encodeURIComponent(selectedDoctorId);
});

document.getElementById('discard-btn').addEventListener('click', function() {
    // Réinitialiser la liste déroulante des départements
    document.getElementById('department-select').value = '';
    
    // Réinitialiser la liste déroulante des docteurs
    var doctorSelect = document.getElementById('doctor-select');
    doctorSelect.innerHTML = '<option selected disabled>Choose a doctor</option>';
    doctorSelect.disabled = true;
});