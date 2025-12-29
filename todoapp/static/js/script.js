function showTab(tabName) {
    document.querySelectorAll('.task-section').forEach(section => {
        section.classList.add('hidden');
    });

    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });

    document.getElementById(tabName).classList.remove('hidden');
    event.target.classList.add('active');
}
