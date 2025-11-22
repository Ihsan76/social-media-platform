// تطبيق إدارة الوسائط الاجتماعية - الإصدار 2.1
class SocialMediaManager {
    constructor() {
        this.apiBase = '/api';
        this.currentUser = null;
        this.sessionId = localStorage.getItem('sessionId');
        this.init();
    }

    init() {
        this.checkSystemStatus();
        this.loadCurrentUser();
        this.setupEventListeners();
        
        if (this.sessionId) {
            this.loadUserData();
        }
    }

    setupEventListeners() {
        setInterval(() => {
            if (this.sessionId) {
                this.loadSocialAccounts();
            }
        }, 30000);

        // إضافة مستمعي الأحداث للأزرار
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
            if (data.status === 'صحي') {
                statusElement.innerHTML = '✅ النظام يعمل بشكل طبيعي';
                statusElement.style.background = 'rgba(40, 167, 69, 0.2)';
            } else {
                statusElement.innerHTML = '⚠️ هناك مشكلة في النظام';
                statusElement.style.background = 'rgba(255, 193, 7, 0.2)';
            }
        } catch (error) {
            console.error('خطأ في فحص حالة النظام:', error);
            document.getElementById('systemStatus').innerHTML = '❌ تعذر الاتصال بالنظام';
        }
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
                error: 'تعذر الاتصال بالخادم',
                status: 0
            };
        }
    }

    // التسجيل بالبريد الإلكتروني
    async registerWithEmail() {
        const username = document.getElementById('regUsername').value;
        const email = document.getElementById('regEmail').value;
        const password = document.getElementById('regPassword').value;

        if (!username || !email || !password) {
            this.showMessage('registerMessage', 'جميع الحقول مطلوبة', 'error');
            return;
        }

        if (password.length < 6) {
            this.showMessage('registerMessage', 'كلمة المرور يجب أن تكون 6 أحرف على الأقل', 'error');
            return;
        }

        const result = await this.apiCall('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password })
        });

        this.handleAuthResponse(result, 'registerMessage', 'profile');
    }

    // تسجيل الدخول بالبريد الإلكتروني
    async loginWithEmail() {
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        if (!email || !password) {
            this.showMessage('loginMessage', 'البريد الإلكتروني وكلمة المرور مطلوبان', 'error');
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
        // في التطبيق الحقيقي، هنا نفتح نافذة OAuth
        // لكن للتجربة سنستخدم محاكاة
        const socialId = this.generateMockSocialId(platform);
        const email = `${socialId}@${platform}.com`;
        const username = `${platform}_user_${socialId.substr(0, 6)}`;

        const result = await this.apiCall('/auth/social-login', {
            method: 'POST',
            body: JSON.stringify({
                platform: platform,
                social_id: socialId,
                email: email,
                username: username
            })
        });

        this.handleAuthResponse(result, 'loginMessage', 'profile', platform);
    }

    // ربط حساب اجتماعي بحساب موجود
    async linkSocialAccount() {
        const platform = document.getElementById('linkPlatform').value;
        const socialId = document.getElementById('linkSocialId').value;

        if (!platform || !socialId) {
            this.showMessage('linkMessage', 'المنصة والمعرف الاجتماعي مطلوبان', 'error');
            return;
        }

        const result = await this.apiCall('/auth/link-social', {
            method: 'POST',
            body: JSON.stringify({ platform, social_id: socialId })
        });

        if (result.success) {
            this.showMessage('linkMessage', result.data.message, 'success');
            this.getProfile(); // تحديث الملف الشخصي
            document.getElementById('linkSocialId').value = ''; // مسح الحقل
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
            
            const action = result.data.action === 'register' ? 'إنشاء' : 'تسجيل الدخول';
            const method = platform ? `باستخدام ${this.getPlatformName(platform)}` : '';
            
            this.showMessage(messageElementId, `تم ${action} الحساب ${method} بنجاح!`, 'success');
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

    // باقي الدوال تبقى كما هي (getProfile, connectSocialAccount, loadSocialAccounts, etc.)
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
            this.showMessage('accountsList', 'جميع الحقول مطلوبة', 'error');
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
            this.showMessage('accountsList', 'تعذر تحميل الحسابات', 'error');
        }
    }

    displayUserProfile(user) {
        const profileElement = document.getElementById('profileInfo');
        const socialLogins = user.social_logins_count > 0 ? 
            ` (${user.social_logins_count} حساب اجتماعي مرتبط)` : '';
        
        profileElement.innerHTML = `
            <div class="profile-header">
                <h3>معلومات المستخدم</h3>
            </div>
            <div class="profile-details">
                <p><strong>اسم المستخدم:</strong> ${user.username}</p>
                <p><strong>البريد الإلكتروني:</strong> ${user.email}</p>
                <p><strong>طريقة التسجيل:</strong> ${this.getAuthMethodName(user.auth_method)}${socialLogins}</p>
                <p><strong>تاريخ الإنشاء:</strong> ${new Date(user.created_at).toLocaleDateString('ar-SA')}</p>
                <p><strong>اللغة:</strong> ${user.preferences.language === 'ar' ? 'العربية' : user.preferences.language}</p>
                <p><strong>الحالة:</strong> ${user.is_active ? 'نشط' : 'غير نشط'}</p>
            </div>
            <button class="btn btn-secondary" onclick="app.logout()">تسجيل الخروج</button>
        `;
        profileElement.classList.add('active');
    }

    displaySocialAccounts(accounts) {
        const accountsElement = document.getElementById('accountsList');
        
        if (accounts.length === 0) {
            accountsElement.innerHTML = '<p class="no-accounts">لا توجد حسابات مربوطة بعد</p>';
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
                        <small>متابعون: ${account.stats.followers} | منشورات: ${account.stats.posts}</small>
                    </div>
                </div>
                <div class="account-status active">
                    نشط
                </div>
            </div>
        `).join('');
    }

    getAuthMethodName(method) {
        const methods = {
            'email': 'البريد الإلكتروني',
            'google': 'Google',
            'twitter': 'Twitter',
            'facebook': 'Facebook',
            'instagram': 'Instagram',
            'github': 'GitHub'
        };
        return methods[method] || method;
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
            'twitter': 'تويتر (X)',
            'facebook': 'فيسبوك',
            'instagram': 'إنستغرام',
            'linkedin': 'لينكدإن',
            'google': 'Google',
            'github': 'GitHub'
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
        this.showMessage('loginMessage', 'تم تسجيل الخروج بنجاح', 'success');
    }
}

// تهيئة التطبيق
const app = new SocialMediaManager();

// الدوال العامة للاستدعاء من HTML
function switchTab(tabName) {
    app.switchTab(tabName);
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
