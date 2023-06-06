// Supprimer un fichier
function deleteFile(filename) {
    if (confirm("Voulez-vous vraiment supprimer ce fichier ?")) {
      fetch(`/delete/${filename}`, { method: 'POST' })
        .then(() => {
          location.reload();
        })
        .catch((error) => {
          console.error('Une erreur s\'est produite lors de la suppression du fichier:', error);
        });
    }
  }
  
  // Ajouter un gestionnaire d'événement aux boutons de suppression
  const deleteButtons = document.getElementsByClassName('delete-button');
  for (let i = 0; i < deleteButtons.length; i++) {
    const button = deleteButtons[i];
    const filename = button.getAttribute('data-filename');
    button.addEventListener('click', () => deleteFile(filename));
  }
  