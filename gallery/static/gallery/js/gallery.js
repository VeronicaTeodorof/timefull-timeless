// written with Clade AI
// Populates the shared edit-theme modal with the correct data for
// the theme's edit button that was clicked, since one modal serves
// all theme cards. Bootstrap's show.bs.modal event fires just before
// the modal opens; event.relatedTarget gives the specific button
// that triggered it, so that theme's name, slug, and sculptures
// (passed as data-* attributes) can be read, and fill in the form
// accordingly before the user sees it.
document.getElementById('editThemeModal').addEventListener('show.bs.modal', function(event) {
    const button = event.relatedTarget;

    // Fill in the theme name field
    document.getElementById('editThemeName').value = button.getAttribute('data-theme-name');

    // Point the form at the correct theme's edit URL
    document.getElementById('editThemeForm').action = `/gallery/theme/${button.getAttribute('data-theme-slug')}/edit/`;

    // Parse the sculptures JSON string back into a usable array
    const raw = button.getAttribute('data-sculptures');
    const sculptures = JSON.parse(button.getAttribute('data-sculptures'));

    // Rebuild the representative-image dropdown's options
    const select = document.getElementById('editThemeImageSelect');
    select.innerHTML = '';
    sculptures.forEach(s => {
        const option = document.createElement('option');
        option.value = s.pk;
        option.textContent = s.title;
        select.appendChild(option);
    });
});


