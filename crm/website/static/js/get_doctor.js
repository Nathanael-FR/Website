// get_doctor.js
document.getElementById('department-select').addEventListener('change', function() {
    var selectedDepartment = this.value;
    var doctorSelect = document.getElementById('doctor-select');
    
    // Réinitialiser la liste déroulante des docteurs
    doctorSelect.innerHTML = '<option selected disabled>Choose a doctor</option>';
    doctorSelect.disabled = true;

    // Si la spécialité sélectionnée n'est pas "Choose a department", effectuer la requête AJAX
    if (selectedDepartment !== '') {
        // Envoyer une requête AJAX pour récupérer les docteurs avec la spécialité sélectionnée
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                // Mettre à jour la liste déroulante des docteurs
                doctorSelect.innerHTML = xhr.responseText;
                doctorSelect.disabled = false;

                // Simulation de l'événement "change" sur la liste déroulante des docteurs
                var event = new Event('change');
                doctorSelect.dispatchEvent(event);
            }
        };
        xhr.open('GET', '/get_doctors/?speciality=' + selectedDepartment, true);
        xhr.send();
    }
});
    
