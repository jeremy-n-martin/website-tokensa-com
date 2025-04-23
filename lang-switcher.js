document.addEventListener('DOMContentLoaded', () => {
    const langFrBtn = document.getElementById('lang-fr-btn');
    const langEnBtn = document.getElementById('lang-en-btn');
    const frContent = document.getElementById('fr-content');
    const enContent = document.getElementById('en-content');
    const languageSections = document.querySelectorAll('.language-section');

    function switchToFrench() {
        languageSections.forEach(section => section.classList.remove('active'));
        frContent.classList.add('active');
        document.documentElement.lang = 'fr'; // Met à jour l'attribut lang de la balise html
    }

    function switchToEnglish() {
        languageSections.forEach(section => section.classList.remove('active'));
        enContent.classList.add('active');
        document.documentElement.lang = 'en'; // Met à jour l'attribut lang de la balise html
    }

    langFrBtn.addEventListener('click', switchToFrench);
    langEnBtn.addEventListener('click', switchToEnglish);

    // Optionnel : Détecter la langue du navigateur et afficher la section correspondante
    // const userLang = navigator.language || navigator.userLanguage;
    // if (userLang.startsWith('fr')) {
    //     switchToFrench();
    // } else {
    //     switchToEnglish(); // Par défaut en anglais si non français
    // }
}); 