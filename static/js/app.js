// تطبيق إدارة الوسائط الاجتماعية - الإصدار 2.2
class SocialMediaManager {
    constructor() {
        this.apiBase = '/api';
        this.currentUser = null;
        this.sessionId = localStorage.getItem('sessionId');
        this.currentLang = window.CURRENT_LANG || 'en';
        this.languages = window.LANGUAGES || {};
        this.translations = window.TRANSLATIONS || {};
        this.init();
    }

    init() {
        this.applyLanguageDirection();
        this.checkSystemStatus();
        this.loadCurrentUser();
        this.setupEventListeners();
        
        if (this.sessionId) {
            this.loadUserData();
        }
    }

    applyLanguageDirection() {
        // تطبيق اتجاه الصفحة بناءً على اللغة
        const direction = this.languages[this.currentLang]?.dir || 'ltr';
        document.documentElement.dir = direction;
    }

    setupEventListeners() {
        setInterval(() => {
            if (this.sessionId) {
                this.loadSocialAccounts();
            }
        }, 30000);

        this.addEnterKeyListeners();
    }

    addEnterKeyListeners() {
        // التسجيل
        document.getElementById('regPassword')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.registerWithEmail();
        });

        // تسجيل الدخول
        document.getElementById('loginPassword')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.loginWithEmail();
        });

        // ربط الحسابات
        document.getElementById('linkSocialId')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.linkSocialAccount();
        });

        document.getElementById('socialToken')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.connectSocialAccount();
        });
    }

    async checkSystemStatus() {
        try {
            const response = await fetch(`${this.apiBase}/health`);
            const data = await response.json();
            
            const statusElement = document.getElementById('systemStatus');
            if (data.status === this.t('healthy') || data.status === 'صحي' || data.status === 'Sain') {
                statusElement.innerHTML = '✅ ' + this.t('system_working');
                statusElement.style.background = 'rgba(40, 167, 69, 0.2)';
            } else {
                statusElement.innerHTML = '⚠️ ' + this.t('system_issue');
                statusElement.style.background = 'rgba(255, 193, 7, 0.2)';
            }
        } catch (error) {
            console.error('Error checking system status:', error);
            document.getElementById('systemStatus').innerHTML = '❌ ' + this.t('cannot_connect');
        }
    }

    t(key) {
        // دالة الترجمة
        return this.translations[key] || key;
    }

    async apiCall(endpoint, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (this.sessionId) {
            defaultOptions.headers['Authorization'] = `Bearer ${this.sessionId}`;
        }

        const finalOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(`${this.apiBase}${endpoint}`, finalOptions);
            const data = await response.json();
            
            return {
                success: response.ok,
                data: data,
                status: response.status
            };
        } catch (error) {
            return {
                success: false,
                error: this.t('cannot_connect'),
                status: 0
            };
        }
    }

    // تغيير لغة الواجهة
    changeLanguage(lang) {
        window.location.href = `/?lang=${lang}`;
    }

    // تغيير لغة المستخدم
    async changeUserLanguage() {
        const newLanguage = document.getElementById('profileLanguage').value;

        const result = await this.apiCall('/auth/change-language', {
            method: 'POST',
            body: JSON.stringify({ language: newLanguage })
        });

        if (result.success) {
            this.showMessage('languageMessage', this.t('profile_loaded'), 'success');
            this.currentLang = newLanguage;
            this.translations = result.data.translations || this.translations;
            // إعادة تحميل الصفحة لتطبيق اللغة الجديدة
            setTimeout(() => {
                this.changeLanguage(newLanguage);
            }, 1000);
        } else {
            this.showMessage('languageMessage', result.data.error, 'error');
        }
    }

    // التسجيل بالبريد الإلكتروني
    async registerWithEmail() {
        const username = document.getElementById('regUsername').value;
        const email = document.getElementById('regEmail').value;
        const password = document.getElementById('regPassword').value;
        const language = document.getElementById('regLanguage').value;

        if (!username || !email || !password) {
            this.showMessage('registerMessage', this.t('all_fields_required'), 'error');
            return;
        }

        if (password.length < 6) {
            this.showMessage('registerMessage', this.t('password_min_length'), 'error');
            return;
        }

        const result = await this.apiCall('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password, language })
        });

        this.handleAuthResponse(result, 'registerMessage', 'profile');
    }

    // تسجيل الدخول بالبريد الإلكتروني
    async loginWithEmail() {
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        if (!email || !password) {
            this.showMessage('loginMessage', this.t('all_fields_required'), 'error');
            return;
        }

        const result = await this.apiCall('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });

        this.handleAuthResponse(result, 'loginMessage', 'profile');
    }

    // التسجيل/الدخول بالحسابات الاجتماعية
    async socialLogin(platform) {
        const socialId = this.generateMockSocialId(platform);
        const email = `${socialId}@${platform}.com`;
        const username = `${platform}_user_${socialId.substr(0, 6)}`;
        const language = this.currentLang;

        const result = await this.apiCall('/auth/social-login', {
            method: 'POST',
            body: JSON.stringify({
                platform: platform,
                social_id: socialId,
                email: email,
                username: username,
                language: language
            })
        });

        this.handleAuthResponse(result, 'loginMessage', 'profile', platform);
    }

    // ربط حساب اجتماعي بحساب موجود
    async linkSocialAccount() {
        const platform = document.getElementById('linkPlatform').value;
        const socialId = document.getElementById('linkSocialId').value;

        if (!platform || !socialId) {
            this.showMessage('linkMessage', this.t('all_fields_required'), 'error');
            return;
        }

        const result = await this.apiCall('/auth/link-social', {
            method: 'POST',
            body: JSON.stringify({ platform, social_id: socialId })
        });

        if (result.success) {
            this.showMessage('linkMessage', result.data.message, 'success');
            this.getProfile();
            document.getElementById('linkSocialId').value = '';
        } else {
            this.showMessage('linkMessage', result.data.error, 'error');
        }
    }

    // معالجة استجابة المصادقة
    handleAuthResponse(result, messageElementId, nextTab, platform = null) {
        if (result.success) {
            this.sessionId = result.data.session_id;
            this.currentUser = result.data.user;
            localStorage.setItem('sessionId', this.sessionId);
            
            const action = result.data.action === 'register' ? this.t('account_created') : this.t('login_success');
            const method = platform ? ` ${this.t('using')} ${this.t(platform)}` : '';
            
            this.showMessage(messageElementId, `${action}${method}`, 'success');
            this.switchTab(nextTab);
            this.loadUserData();
        } else {
            this.showMessage(messageElementId, result.data.error, 'error');
        }
    }

    // توليد معرف اجتماعي تجريبي
    generateMockSocialId(platform) {
        const prefixes = {
            google: 'google',
            twitter: 'twitter', 
            facebook: 'fb',
            instagram: 'ig',
            github: 'gh'
        };
        return `${prefixes[platform]}_${Math.random().toString(36).substr(2, 9)}`;
    }

    // باقي الدوال تبقى كما هي مع إضافة الترجمة
    async getProfile() {
        const result = await this.apiCall('/auth/profile');
        
        if (result.success) {
            this.currentUser = result.data.user;
            this.displayUserProfile(result.data.user);
        } else {
            this.showMessage('profileInfo', result.data.error, 'error');
            this.logout();
        }
    }

    async connectSocialAccount() {
        const platform = document.getElementById('socialPlatform').value;
        const username = document.getElementById('socialUsername').value;
        const accessToken = document.getElementById('socialToken').value;

        if (!platform || !username || !accessToken) {
            this.showMessage('accountsList', this.t('all_fields_required'), 'error');
            return;
        }

        const result = await this.apiCall('/social/connect', {
            method: 'POST',
            body: JSON.stringify({ platform, username, access_token: accessToken })
        });

        if (result.success) {
            this.showMessage('accountsList', result.data.message, 'success');
            this.loadSocialAccounts();
            document.getElementById('socialUsername').value = '';
            document.getElementById('socialToken').value = '';
        } else {
            this.showMessage('accountsList', result.data.error, 'error');
        }
    }

    async loadSocialAccounts() {
        const result = await this.apiCall('/social/accounts');
        
        if (result.success) {
            this.displaySocialAccounts(result.data.accounts);
        } else {
            this.showMessage('accountsList', this.t('cannot_connect'), 'error');
        }
    }

    displayUserProfile(user) {
        const profileElement = document.getElementById('profileInfo');
        const socialLogins = user.social_logins_count > 0 ? 
            ` (${user.social_logins_count} ${this.t('linked_social_accounts')})` : '';
        
        profileElement.innerHTML = `
            <div class="profile-header">
                <h3>${this.t('user_information')}</h3>
            </div>
            <div class="profile-details">
                <p><strong>${this.t('username')}:</strong> ${user.username}</p>
                <p><strong>${this.t('email')}:</strong> ${user.email}</p>
                <p><strong>${this.t('auth_method')}:</strong> ${user.auth_method}${socialLogins}</p>
                <p><strong>${this.t('creation_date')}:</strong> ${new Date(user.created_at).toLocaleDateString(this.currentLang)}</p>
                <p><strong>${this.t('language')}:</strong> ${this.languages[user.language]?.name || user.language}</p>
                <p><strong>${this.t('timezone')}:</strong> ${user.preferences.timezone}</p>
                <p><strong>${this.t('status')}:</strong> ${user.is_active ? this.t('active') : this.t('inactive')}</p>
            </div>
            <button class="btn btn-secondary" onclick="app.logout()">${this.t('logout')}</button>
        `;
        profileElement.classList.add('active');
    }

    displaySocialAccounts(accounts) {
        const accountsElement = document.getElementById('accountsList');
        
        if (accounts.length === 0) {
            accountsElement.innerHTML = `<p class="no-accounts">${this.t('no_accounts')}</p>`;
            return;
        }

        accountsElement.innerHTML = accounts.map(account => `
            <div class="account-card">
                <div class="account-icon">
                    ${this.getPlatformIcon(account.platform)}
                </div>
                <div class="account-info">
                    <div class="account-platform">${this.getPlatformName(account.platform)}</div>
                    <div class="account-username">@${account.username}</div>
                    <div class="account-stats">
                        <small>${this.t('followers')}: ${account.stats.followers} | ${this.t('posts')}: ${account.stats.posts}</small>
                    </div>
                </div>
                <div class="account-status active">
                    ${this.t('active')}
                </div>
            </div>
        `).join('');
    }

    getPlatformIcon(platform) {
        const icons = {
            'twitter': '🐦',
            'facebook': '📘',
            'instagram': '📷',
            'linkedin': '💼',
            'google': '🔍',
            'github': '💻'
        };
        return icons[platform] || '🔗';
    }

    getPlatformName(platform) {
        const names = {
            'twitter': this.t('twitter'),
            'facebook': this.t('facebook'),
            'instagram': this.t('instagram'),
            'linkedin': this.t('linkedin'),
            'google': this.t('google'),
            'github': this.t('github')
        };
        return names[platform] || platform;
    }

    showMessage(elementId, message, type) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = message;
            element.className = `message ${type}`;
            element.style.display = 'block';

            setTimeout(() => {
                element.style.display = 'none';
            }, 5000);
        }
    }

    switchTab(tabName) {
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });
        
        document.getElementById(tabName).classList.add('active');
        document.querySelector(`.tab[onclick="switchTab('${tabName}')"]`).classList.add('active');

        if (tabName === 'profile' && this.sessionId) {
            this.getProfile();
        } else if (tabName === 'social' && this.sessionId) {
            this.loadSocialAccounts();
        }
    }

    loadCurrentUser() {
        if (this.sessionId) {
            this.getProfile();
        }
    }

    loadUserData() {
        this.getProfile();
        this.loadSocialAccounts();
    }

    logout() {
        this.sessionId = null;
        this.currentUser = null;
        localStorage.removeItem('sessionId');
        
        document.getElementById('profileInfo').innerHTML = '';
        document.getElementById('profileInfo').classList.remove('active');
        document.getElementById('accountsList').innerHTML = '';
        
        this.switchTab('login');
        this.showMessage('loginMessage', this.t('disconnected'), 'success');
    }
}

// تهيئة التطبيق
const app = new SocialMediaManager();

// الدوال العامة للاستدعاء من HTML
function switchTab(tabName) {
    app.switchTab(tabName);
}

function changeLanguage(lang) {
    app.changeLanguage(lang);
}

function changeUserLanguage() {
    app.changeUserLanguage();
}

function registerWithEmail() {
    app.registerWithEmail();
}

function loginWithEmail() {
    app.loginWithEmail();
}

function socialLogin(platform) {
    app.socialLogin(platform);
}

function linkSocialAccount() {
    app.linkSocialAccount();
}

function getProfile() {
    app.getProfile();
}

function connectSocialAccount() {
    app.connectSocialAccount();
}

function loadSocialAccounts() {
    app.loadSocialAccounts();
}
