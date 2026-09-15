// Populates the shared delete-sculpture modal with the correct sculpture name and delete URL,
// since one modal serves every sculpture. Bootstrap's show.bs.modal event fires just before the
// modal opens; event.relatedTarget gives the specific button that
// triggered it, so its data-* attributes can be read and used to
// fill in the modal before the user sees it
document.getElementById('deleteSculptureModal').addEventListener('show.bs.modal', function(event) {
    const button = event.relatedTarget;
    document.getElementById('deleteSculptureName').textContent = button.getAttribute('data-sculpture-title');
    document.getElementById('deleteSculptureForm').action = button.getAttribute('data-delete-url');
});

document.addEventListener('hide.bs.modal', function () {
    if (document.activeElement) {
        document.activeElement.blur();
    }
});