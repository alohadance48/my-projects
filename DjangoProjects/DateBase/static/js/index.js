// Модуль для переключения секций
class SectionSwitcher {
    constructor(filesTab, profileTab, filesSection, profileSection) {
        this.filesTab = filesTab;
        this.profileTab = profileTab;
        this.filesSection = filesSection;
        this.profileSection = profileSection;

        this.init();
    }

    init() {
        this.filesTab.addEventListener('click', () => {
            this.showSection('files');
        });

        this.profileTab.addEventListener('click', () => {
            this.showSection('profile');
        });
    }

    showSection(section) {
        this.filesSection.style.display = section === 'files' ? 'block' : 'none';
        this.profileSection.style.display = section === 'profile' ? 'block' : 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log("index.js загружен");

    const filesTab = document.getElementById('filesTab');
    const profileTab = document.getElementById('profileTab');
    const filesSection = document.getElementById('filesSection');
    const profileSection = document.getElementById('profileSection');

    new SectionSwitcher(filesTab, profileTab, filesSection, profileSection);

    // Функция для обработки загрузки файла остается прежней
    document.getElementById('uploadForm').addEventListener('submit', (event) => {
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];

        if (!file) {
            alert("Пожалуйста, выберите файл для загрузки.");
            event.preventDefault(); // Отменяем отправку формы, если файл не выбран
            return;
        }

        // Здесь можно добавить дополнительные проверки, если нужно
        // Например, проверка типа файла или размера

        // Если файл выбран, форма будет отправлена автоматически
    });

    // Функция для получения CSRF-токена остается прежней
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
