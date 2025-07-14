// Модуль для переключения секций
class SectionSwitcher {
    constructor(usersTab, profileTab, usersSection, profileSection) {
        this.usersTab = usersTab;
        this.profileTab = profileTab;
        this.usersSection = usersSection;
        this.profileSection = profileSection;

        this.init();
    }

    init() {
        this.usersTab.addEventListener('click', () => {
            this.showSection('users');
        });

        this.profileTab.addEventListener('click', () => {
            this.showSection('profile');
        });
    }

    showSection(section) {
        this.usersSection.style.display = section === 'users' ? 'block' : 'none';
        this.profileSection.style.display = section === 'profile' ? 'block' : 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log("index.js загружен");

    const usersTab = document.getElementById('usersTab');
    const profileTab = document.getElementById('profileTab');
    const usersSection = document.getElementById('usersSection');
    const profileSection = document.getElementById('profileSection');

    new SectionSwitcher(usersTab, profileTab, usersSection, profileSection);

    // Обработка кнопки "Добавить пользователя"
    const addUserButton = document.getElementById('addUserButton');
    if (addUserButton) {
        addUserButton.addEventListener('click', () => {
            window.location.href = '/path/to/your/add/user/form'; // Замените на вашу ссылку
        });
    }

    // Обработка формы удаления пользователя
    const deleteUserForms = document.querySelectorAll('.deleteUserForm');
    deleteUserForms.forEach(form => {
        form.addEventListener('submit', (event) => {
            const confirmation = confirm("Вы уверены, что хотите удалить этого пользователя?");
            if (!confirmation) {
                event.preventDefault(); // Отменяем отправку формы, если пользователь не подтвердил
            }
        });
    });
});
