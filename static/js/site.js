// Comportements facultatifs : le site reste utilisable sans JavaScript.
(function () {
  // Menu repliable sur mobile.
  var bouton = document.querySelector('.menu__bouton');
  var nav = document.getElementById('navigation');
  if (bouton && nav) {
    bouton.addEventListener('click', function () {
      var ouvert = nav.classList.toggle('nav--ouverte');
      bouton.setAttribute('aria-expanded', ouvert ? 'true' : 'false');
    });
  }

  // Fiche produit : met à jour le prix affiché quand on change de contenance.
  var prix = document.getElementById('prix-affiche');
  var choix = document.querySelectorAll('input[name="variante"][data-prix]');
  choix.forEach(function (radio) {
    radio.addEventListener('change', function () {
      if (prix && radio.checked) {
        prix.textContent = radio.getAttribute('data-prix') + ' ' + (prix.getAttribute('data-devise') || '');
      }
    });
  });
})();
